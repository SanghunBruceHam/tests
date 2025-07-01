import { Card, CardContent } from "@/components/ui/card";
import type { Fortune } from "@shared/schema";

interface LuckyItemsProps {
  fortune: Fortune;
}

export function LuckyItems({ fortune }: LuckyItemsProps) {
  return (
    <section className="mb-8">
      <Card className="shadow-lg dark:bg-gray-800">
        <CardContent className="p-4 sm:p-6">
          <h3 className="text-lg sm:text-xl font-bold text-center mb-6 text-gray-800 dark:text-gray-200">오늘의 행운 아이템</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4">
            <div className="text-center p-3 sm:p-4 bg-gradient-to-br from-yellow-50 to-white dark:from-gray-700 dark:to-gray-600 rounded-lg">
              <div className="text-2xl sm:text-3xl mb-2">🔴</div>
              <div className="font-medium text-gray-700 dark:text-gray-300 text-xs sm:text-sm">행운의 색상</div>
              <div className="text-xs sm:text-sm text-red-600 dark:text-red-400 font-bold">{fortune.luckyColor}</div>
            </div>
            <div className="text-center p-3 sm:p-4 bg-gradient-to-br from-yellow-50 to-white dark:from-gray-700 dark:to-gray-600 rounded-lg">
              <div className="text-2xl sm:text-3xl mb-2">🔢</div>
              <div className="font-medium text-gray-700 dark:text-gray-300 text-xs sm:text-sm">행운의 숫자</div>
              <div className="text-xs sm:text-sm text-red-600 dark:text-red-400 font-bold">{fortune.luckyNumbers}</div>
            </div>
            <div className="text-center p-3 sm:p-4 bg-gradient-to-br from-yellow-50 to-white dark:from-gray-700 dark:to-gray-600 rounded-lg">
              <div className="text-2xl sm:text-3xl mb-2">🧿</div>
              <div className="font-medium text-gray-700 dark:text-gray-300 text-xs sm:text-sm">행운의 방향</div>
              <div className="text-xs sm:text-sm text-red-600 dark:text-red-400 font-bold">{fortune.luckyDirection}</div>
            </div>
            <div className="text-center p-3 sm:p-4 bg-gradient-to-br from-yellow-50 to-white dark:from-gray-700 dark:to-gray-600 rounded-lg">
              <div className="text-2xl sm:text-3xl mb-2">⏰</div>
              <div className="font-medium text-gray-700 dark:text-gray-300 text-xs sm:text-sm">행운의 시간</div>
              <div className="text-xs sm:text-sm text-red-600 dark:text-red-400 font-bold">{fortune.luckyTime}</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </section>
  );
}
