import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useMutation } from "@tanstack/react-query";
import { useToast } from "@/hooks/use-toast";
import { apiRequest } from "@/lib/queryClient";
import type { ZodiacAnimal, PeriodFortune } from "@shared/schema";

interface PeriodFortuneProps {
  zodiacAnimals?: ZodiacAnimal[];
}

export function PeriodFortuneComponent({ zodiacAnimals }: PeriodFortuneProps) {
  const [selectedZodiac, setSelectedZodiac] = useState<string>("");
  const [weeklyFortune, setWeeklyFortune] = useState<PeriodFortune | null>(null);
  const [monthlyFortune, setMonthlyFortune] = useState<PeriodFortune | null>(null);
  const { toast } = useToast();

  const periodFortuneMutation = useMutation({
    mutationFn: async (data: { zodiac: string; period: 'weekly' | 'monthly' }) => {
      const response = await apiRequest("POST", "/api/period-fortune", data);
      return response.json();
    },
    onSuccess: (data, variables) => {
      if (variables.period === 'weekly') {
        setWeeklyFortune(data);
      } else {
        setMonthlyFortune(data);
      }
    },
    onError: (error) => {
      toast({
        title: "오류",
        description: error.message || "기간별 운세를 가져오는데 실패했습니다",
        variant: "destructive",
      });
    },
  });

  const handleGetPeriodFortune = (period: 'weekly' | 'monthly') => {
    if (!selectedZodiac) {
      toast({
        title: "알림",
        description: "띠를 선택해주세요",
        variant: "destructive",
      });
      return;
    }

    periodFortuneMutation.mutate({ zodiac: selectedZodiac, period });
  };

  const renderStars = (score: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <span key={i} className={`text-lg ${i < score ? "text-yellow-400" : "text-gray-300 dark:text-gray-600"}`}>
        ★
      </span>
    ));
  };

  const FortuneCard = ({ fortune, period }: { fortune: PeriodFortune; period: string }) => (
    <div className="space-y-4">
      {/* Overall Fortune */}
      <Card className="border-l-4 border-purple-400 dark:border-purple-500 dark:bg-gray-800">
        <CardContent className="p-4">
          <div className="flex items-center justify-between mb-3">
            <h4 className="font-bold text-gray-800 dark:text-gray-200">📊 종합운</h4>
            <div className="flex space-x-1">{renderStars(fortune.overallScore)}</div>
          </div>
          <p className="text-gray-600 dark:text-gray-300 text-sm">{fortune.overall}</p>
        </CardContent>
      </Card>

      {/* Category Fortunes */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Card className="border-l-4 border-red-400 dark:border-red-500 dark:bg-gray-800">
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <h5 className="font-semibold text-gray-800 dark:text-gray-200">💕 애정운</h5>
              <div className="flex space-x-1">{renderStars(fortune.loveScore)}</div>
            </div>
            <p className="text-gray-600 dark:text-gray-300 text-sm">{fortune.love}</p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-green-400 dark:border-green-500 dark:bg-gray-800">
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <h5 className="font-semibold text-gray-800 dark:text-gray-200">💰 금전운</h5>
              <div className="flex space-x-1">{renderStars(fortune.moneyScore)}</div>
            </div>
            <p className="text-gray-600 dark:text-gray-300 text-sm">{fortune.money}</p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-blue-400 dark:border-blue-500 dark:bg-gray-800">
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <h5 className="font-semibold text-gray-800 dark:text-gray-200">🏥 건강운</h5>
              <div className="flex space-x-1">{renderStars(fortune.healthScore)}</div>
            </div>
            <p className="text-gray-600 dark:text-gray-300 text-sm">{fortune.health}</p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-orange-400 dark:border-orange-500 dark:bg-gray-800">
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <h5 className="font-semibold text-gray-800 dark:text-gray-200">💼 직업운</h5>
              <div className="flex space-x-1">{renderStars(fortune.careerScore)}</div>
            </div>
            <p className="text-gray-600 dark:text-gray-300 text-sm">{fortune.career}</p>
          </CardContent>
        </Card>
      </div>

      {/* Advice */}
      <Card className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/30 dark:to-purple-900/30 dark:bg-gray-800">
        <CardContent className="p-4">
          <h5 className="font-semibold text-gray-800 dark:text-gray-200 mb-3">💡 {period} 조언</h5>
          <p className="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">{fortune.advice}</p>
        </CardContent>
      </Card>
    </div>
  );

  return (
    <Card className="shadow-lg dark:bg-gray-800">
      <CardHeader>
        <CardTitle className="text-center text-xl font-bold text-gray-800 dark:text-gray-200">
          📅 주간/월간 운세
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
            띠 선택
          </label>
          <Select value={selectedZodiac} onValueChange={setSelectedZodiac}>
            <SelectTrigger className="dark:bg-gray-700 dark:border-gray-600">
              <SelectValue placeholder="띠를 선택해주세요" />
            </SelectTrigger>
            <SelectContent>
              {zodiacAnimals?.map((animal) => (
                <SelectItem key={animal.id} value={animal.name}>
                  {animal.emoji} {animal.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <Tabs defaultValue="weekly" className="w-full">
          <TabsList className="grid w-full grid-cols-2 dark:bg-gray-700">
            <TabsTrigger value="weekly" className="dark:data-[state=active]:bg-gray-600">이번 주</TabsTrigger>
            <TabsTrigger value="monthly" className="dark:data-[state=active]:bg-gray-600">이번 달</TabsTrigger>
          </TabsList>

          <TabsContent value="weekly" className="space-y-4">
            <Button
              onClick={() => handleGetPeriodFortune('weekly')}
              disabled={periodFortuneMutation.isPending || !selectedZodiac}
              className="w-full bg-blue-600 hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-800 text-white font-medium py-3"
            >
              {periodFortuneMutation.isPending ? "확인 중..." : "이번 주 운세 보기"}
            </Button>

            {weeklyFortune && (
              <FortuneCard fortune={weeklyFortune} period="이번 주" />
            )}
          </TabsContent>

          <TabsContent value="monthly" className="space-y-4">
            <Button
              onClick={() => handleGetPeriodFortune('monthly')}
              disabled={periodFortuneMutation.isPending || !selectedZodiac}
              className="w-full bg-purple-600 hover:bg-purple-700 dark:bg-purple-700 dark:hover:bg-purple-800 text-white font-medium py-3"
            >
              {periodFortuneMutation.isPending ? "확인 중..." : "이번 달 운세 보기"}
            </Button>

            {monthlyFortune && (
              <FortuneCard fortune={monthlyFortune} period="이번 달" />
            )}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}