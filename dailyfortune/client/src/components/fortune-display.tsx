import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Fortune, ZodiacAnimal } from "@shared/schema";

interface FortuneDisplayProps {
  zodiac: ZodiacAnimal;
  fortune: Fortune;
  currentDate: string;
}

export function FortuneDisplay({ zodiac, fortune, currentDate }: FortuneDisplayProps) {
  const renderStars = (score: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <span key={i} className={`text-2xl ${i < score ? "text-yellow-400" : "text-gray-300"}`}>
        ★
      </span>
    ));
  };

  return (
    <section className="mb-8">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 sm:w-20 sm:h-20 bg-red-600 dark:bg-red-700 rounded-full mb-4">
          <span className="text-3xl sm:text-4xl">{zodiac.emoji}</span>
        </div>
        <h2 className="text-xl sm:text-2xl font-bold text-gray-800 dark:text-gray-200 mb-2">{zodiac.name}띠의 오늘 운세</h2>
        <p className="text-gray-600 dark:text-gray-400 text-sm sm:text-base">{currentDate}</p>
      </div>

      {/* Overall Fortune Summary */}
      <div className="traditional-border fortune-gradient dark:bg-gradient-to-br dark:from-yellow-900 dark:to-yellow-800 p-6 md:p-8 mb-8">
        <div className="text-center">
          <h3 className="text-lg sm:text-xl font-bold text-red-800 dark:text-red-300 mb-4">오늘의 종합운</h3>
          <div className="flex justify-center mb-4">
            <div className="flex space-x-1">
              {renderStars(fortune.overallScore)}
            </div>
          </div>
          <p className="text-base sm:text-lg text-gray-700 dark:text-gray-200 leading-relaxed">
            {fortune.overall}
          </p>
        </div>
      </div>

      {/* Detailed Fortune Categories */}
      <div className="grid sm:grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
        {/* Love Fortune */}
        <Card className="shadow-lg border-l-4 border-red-400 dark:border-red-500 dark:bg-gray-800">
          <CardContent className="p-4 sm:p-6">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-base sm:text-lg font-bold text-gray-800 dark:text-gray-200 flex items-center">
                💕 애정운
              </h4>
              <div className="flex space-x-1">
                {renderStars(fortune.loveScore)}
              </div>
            </div>
            <p className="text-gray-600 dark:text-gray-300 mb-3 text-sm sm:text-base">
              {fortune.love}
            </p>
            <div className="bg-red-50 dark:bg-red-900/30 p-3 rounded-lg">
              <p className="text-xs sm:text-sm text-red-700 dark:text-red-300 font-medium">💡 조언: {fortune.loveAdvice}</p>
            </div>
          </CardContent>
        </Card>

        {/* Money Fortune */}
        <Card className="shadow-lg border-l-4 border-green-400 dark:border-green-500 dark:bg-gray-800">
          <CardContent className="p-4 sm:p-6">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-base sm:text-lg font-bold text-gray-800 dark:text-gray-200 flex items-center">
                💰 금전운
              </h4>
              <div className="flex space-x-1">
                {renderStars(fortune.moneyScore)}
              </div>
            </div>
            <p className="text-gray-600 dark:text-gray-300 mb-3 text-sm sm:text-base">
              {fortune.money}
            </p>
            <div className="bg-green-50 dark:bg-green-900/30 p-3 rounded-lg">
              <p className="text-xs sm:text-sm text-green-700 dark:text-green-300 font-medium">💡 조언: {fortune.moneyAdvice}</p>
            </div>
          </CardContent>
        </Card>

        {/* Health Fortune */}
        <Card className="shadow-lg border-l-4 border-blue-400 dark:border-blue-500 dark:bg-gray-800">
          <CardContent className="p-4 sm:p-6">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-base sm:text-lg font-bold text-gray-800 dark:text-gray-200 flex items-center">
                🏥 건강운
              </h4>
              <div className="flex space-x-1">
                {renderStars(fortune.healthScore)}
              </div>
            </div>
            <p className="text-gray-600 dark:text-gray-300 mb-3 text-sm sm:text-base">
              {fortune.health}
            </p>
            <div className="bg-blue-50 dark:bg-blue-900/30 p-3 rounded-lg">
              <p className="text-xs sm:text-sm text-blue-700 dark:text-blue-300 font-medium">💡 조언: {fortune.healthAdvice}</p>
            </div>
          </CardContent>
        </Card>

        {/* Career Fortune */}
        <Card className="shadow-lg border-l-4 border-purple-400 dark:border-purple-500 dark:bg-gray-800">
          <CardContent className="p-4 sm:p-6">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-base sm:text-lg font-bold text-gray-800 dark:text-gray-200 flex items-center">
                💼 직업운
              </h4>
              <div className="flex space-x-1">
                {renderStars(fortune.careerScore)}
              </div>
            </div>
            <p className="text-gray-600 dark:text-gray-300 mb-3 text-sm sm:text-base">
              {fortune.career}
            </p>
            <div className="bg-purple-50 dark:bg-purple-900/30 p-3 rounded-lg">
              <p className="text-xs sm:text-sm text-purple-700 dark:text-purple-300 font-medium">💡 조언: {fortune.careerAdvice}</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </section>
  );
}
