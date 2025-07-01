import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { useQuery } from "@tanstack/react-query";
import type { ZodiacAnimal } from "@shared/schema";

interface ZodiacSelectorProps {
  onZodiacSelect: (zodiac: string) => void;
  onBirthDateSubmit: (birthDate: string) => void;
}

export function ZodiacSelector({ onZodiacSelect, onBirthDateSubmit }: ZodiacSelectorProps) {
  const [selectedZodiac, setSelectedZodiac] = useState<string>("");
  const [birthDate, setBirthDate] = useState<string>("");

  const { data: zodiacAnimals, isLoading } = useQuery<ZodiacAnimal[]>({
    queryKey: ["/api/zodiac-animals"],
  });

  const handleZodiacClick = (zodiac: string) => {
    setSelectedZodiac(zodiac);
    onZodiacSelect(zodiac);
  };

  const handleBirthDateSubmit = () => {
    if (birthDate) {
      onBirthDateSubmit(birthDate);
    }
  };

  if (isLoading) {
    return <div className="text-center py-8">띠 정보를 불러오는 중...</div>;
  }

  return (
    <section className="mb-12">
      <div className="traditional-border bg-white dark:bg-gray-800 p-6 md:p-8 transition-colors">
        <h2 className="text-xl sm:text-2xl font-bold text-center mb-6 text-gray-800 dark:text-gray-200">띠를 선택해주세요</h2>
        
        {/* Zodiac Grid */}
        <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3 sm:gap-4 mb-6">
          {zodiacAnimals?.map((animal) => (
            <div
              key={animal.id}
              className={`zodiac-card bg-gradient-to-br from-yellow-50 to-white dark:from-gray-700 dark:to-gray-600 p-3 sm:p-4 rounded-xl cursor-pointer border-2 transition-all ${
                selectedZodiac === animal.name
                  ? "border-red-600 border-opacity-50 bg-opacity-80 dark:border-red-400"
                  : "border-transparent hover:border-yellow-400 dark:hover:border-yellow-500"
              } text-center touch-manipulation`}
              onClick={() => handleZodiacClick(animal.name)}
            >
              <div className="text-3xl sm:text-4xl mb-2">{animal.emoji}</div>
              <div className={`font-medium text-sm sm:text-base ${
                selectedZodiac === animal.name ? "text-red-600 dark:text-red-400" : "text-gray-700 dark:text-gray-300"
              }`}>
                {animal.name}
              </div>
            </div>
          ))}
        </div>

        {/* Birth Date Alternative */}
        <div className="border-t dark:border-gray-600 pt-6">
          <h3 className="text-base sm:text-lg font-medium mb-4 text-center text-gray-700 dark:text-gray-300">또는 생년월일로 확인하기</h3>
          <div className="flex flex-col sm:flex-row gap-4 items-center justify-center">
            <Input
              type="date"
              value={birthDate}
              onChange={(e) => setBirthDate(e.target.value)}
              className="w-full sm:w-auto px-4 py-3 border-2 border-yellow-400 focus:border-red-600 dark:border-yellow-500 dark:focus:border-red-400 dark:bg-gray-700 dark:text-white"
            />
            <Button
              onClick={handleBirthDateSubmit}
              className="w-full sm:w-auto bg-red-600 hover:bg-red-800 dark:bg-red-700 dark:hover:bg-red-800 text-white px-6 sm:px-8 py-3 font-medium shadow-lg text-sm sm:text-base"
            >
              운세 보기
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
}
