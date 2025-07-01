export interface ZodiacAnimal {
  id: number;
  name: string;
  emoji: string;
  index: number;
}

export function calculateZodiacFromDate(birthDate: string): number {
  const year = parseInt(birthDate.split('-')[0]);
  return (year - 4) % 12;
}

export function formatDate(date: Date): string {
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

export function renderStars(score: number): string {
  return '★'.repeat(score) + '☆'.repeat(5 - score);
}
