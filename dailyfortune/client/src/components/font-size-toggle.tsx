import { Button } from "@/components/ui/button"
import { useState, useEffect } from "react"

export function FontSizeToggle() {
  const [fontSize, setFontSize] = useState<'small' | 'medium' | 'large'>('medium')

  useEffect(() => {
    // 로컬 스토리지에서 글씨 크기 설정 로드
    const savedFontSize = localStorage.getItem('fontSize') as 'small' | 'medium' | 'large' || 'medium'
    setFontSize(savedFontSize)
    applyFontSize(savedFontSize)
  }, [])

  const applyFontSize = (size: 'small' | 'medium' | 'large') => {
    const root = document.documentElement
    root.classList.remove('font-small', 'font-medium', 'font-large')
    root.classList.add(`font-${size}`)
  }

  const toggleFontSize = () => {
    const sizes: ('small' | 'medium' | 'large')[] = ['small', 'medium', 'large']
    const currentIndex = sizes.indexOf(fontSize)
    const nextIndex = (currentIndex + 1) % sizes.length
    const newSize = sizes[nextIndex]
    
    console.log('Changing font size from', fontSize, 'to', newSize)
    setFontSize(newSize)
    localStorage.setItem('fontSize', newSize)
    applyFontSize(newSize)
  }

  const getFontSizeDisplay = () => {
    switch (fontSize) {
      case 'small': return { label: '가', class: 'text-xs' }
      case 'medium': return { label: '가', class: 'text-sm' }
      case 'large': return { label: '가', class: 'text-base' }
      default: return { label: '가', class: 'text-sm' }
    }
  }

  const displayInfo = getFontSizeDisplay()
  
  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={toggleFontSize}
      className="h-9 w-9 bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 shadow-sm"
      title={`글씨 크기: ${fontSize === 'small' ? '작게' : fontSize === 'medium' ? '보통' : '크게'}`}
    >
      <span className="font-bold text-sm select-none">
        가
      </span>
    </Button>
  )
}