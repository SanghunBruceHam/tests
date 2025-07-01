import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useToast } from "@/hooks/use-toast";
import { apiRequest } from "@/lib/queryClient";
import { ZodiacSelector } from "@/components/zodiac-selector";
import { FortuneDisplay } from "@/components/fortune-display";
import { LuckyItems } from "@/components/lucky-items";
import { ThemeToggle } from "@/components/theme-toggle";
import { FontSizeToggle } from "@/components/font-size-toggle";
import { AdBanner } from "@/components/ad-banner";
import { CompatibilityChecker } from "@/components/compatibility-checker";
import { PeriodFortuneComponent } from "@/components/period-fortune";
import { DailyQuoteComponent } from "@/components/daily-quote";
import { FortuneHistory } from "@/components/fortune-history";
import { getSessionId } from "@/lib/session";
import type { Fortune, ZodiacAnimal } from "@shared/schema";
import { formatDate } from "@/lib/zodiac";

interface FortuneData {
  zodiac: ZodiacAnimal;
  fortune: Fortune;
}

export default function FortunePage() {
  const [selectedZodiac, setSelectedZodiac] = useState<string>("");
  const [fortuneData, setFortuneData] = useState<FortuneData | null>(null);
  const [sessionId] = useState(getSessionId());
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const { data: zodiacAnimals } = useQuery<ZodiacAnimal[]>({
    queryKey: ["/api/zodiac-animals"],
  });

  const fortuneMutation = useMutation({
    mutationFn: async (zodiac: string) => {
      const response = await apiRequest("GET", `/api/fortune/${zodiac}`);
      return response.json();
    },
    onSuccess: (fortune, zodiac) => {
      // zodiacAnimals에서 해당 띠 정보 찾기
      const zodiacAnimal = zodiacAnimals?.find(animal => animal.name === zodiac);
      if (zodiacAnimal) {
        setFortuneData({
          zodiac: zodiacAnimal,
          fortune
        });
      }
    },
    onError: (error) => {
      toast({
        title: "오류",
        description: error.message || "운세를 가져오는데 실패했습니다",
        variant: "destructive",
      });
    },
  });

  const birthDateMutation = useMutation({
    mutationFn: async (birthDate: string) => {
      const response = await apiRequest("POST", "/api/calculate-zodiac", { birthDate });
      return response.json();
    },
    onSuccess: (data) => {
      setFortuneData(data);
      setSelectedZodiac(data.zodiac.name);
    },
    onError: (error) => {
      toast({
        title: "오류",
        description: error.message || "생년월일 계산에 실패했습니다",
        variant: "destructive",
      });
    },
  });

  const handleZodiacSelect = (zodiac: string) => {
    setSelectedZodiac(zodiac);
    setFortuneData(null);
    // 띠를 선택하면 바로 운세를 가져옴
    fortuneMutation.mutate(zodiac);
  };

  const handleBirthDateSubmit = (birthDate: string) => {
    birthDateMutation.mutate(birthDate);
  };

  const handleShare = () => {
    if (navigator.share && fortuneData) {
      navigator.share({
        title: `${fortuneData.zodiac.name}띠의 오늘 운세`,
        text: fortuneData.fortune.overall,
        url: window.location.href,
      }).catch(() => {
        // Fallback to clipboard
        handleCopyToClipboard();
      });
    } else {
      handleCopyToClipboard();
    }
  };

  const handleCopyToClipboard = () => {
    if (fortuneData) {
      const text = `${fortuneData.zodiac.name}띠의 오늘 운세\n\n${fortuneData.fortune.overall}`;
      navigator.clipboard.writeText(text).then(() => {
        toast({
          title: "복사 완료",
          description: "운세가 클립보드에 복사되었습니다",
        });
      });
    }
  };

  const saveFortuneMutation = useMutation({
    mutationFn: async (data: { sessionId: string; zodiac: string; fortuneDate: string }) => {
      const response = await apiRequest("POST", "/api/save-fortune", data);
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/fortune-history", sessionId] });
      toast({
        title: "저장 완료",
        description: "운세가 저장되었습니다",
      });
    },
    onError: (error) => {
      toast({
        title: "오류",
        description: error.message || "운세 저장에 실패했습니다",
        variant: "destructive",
      });
    },
  });

  const handleSave = () => {
    if (fortuneData) {
      const today = new Date().toISOString().split('T')[0];
      saveFortuneMutation.mutate({
        sessionId,
        zodiac: fortuneData.zodiac.name,
        fortuneDate: today,
      });
    }
  };

  const handleReset = () => {
    setSelectedZodiac("");
    setFortuneData(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const currentDate = formatDate(new Date());

  return (
    <div className="bg-gray-50 dark:bg-gray-900 min-h-screen transition-colors">
      {/* Theme Toggle */}
      <div className="fixed top-4 right-4 z-50 flex gap-2">
        <FontSizeToggle />
        <ThemeToggle />
      </div>
      
      {/* Watermark */}
      <div className="watermark">tests.mahalohana-bruce.com</div>
      
      {/* Header */}
      <header className="header-gradient text-white shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <div className="text-center">
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-2">🔮 오늘의 운세</h1>
            <p className="text-yellow-100 text-base sm:text-lg">전통 한국 운세로 하루를 시작하세요</p>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Daily Quote - Always visible at top */}
        <DailyQuoteComponent />
        
        <Tabs defaultValue="daily" className="mt-8">
          <TabsList className="grid w-full grid-cols-4 dark:bg-gray-700 mb-8">
            <TabsTrigger value="daily" className="dark:data-[state=active]:bg-gray-600">오늘 운세</TabsTrigger>
            <TabsTrigger value="period" className="dark:data-[state=active]:bg-gray-600">주간/월간</TabsTrigger>
            <TabsTrigger value="compatibility" className="dark:data-[state=active]:bg-gray-600">궁합</TabsTrigger>
            <TabsTrigger value="history" className="dark:data-[state=active]:bg-gray-600">기록</TabsTrigger>
          </TabsList>

          <TabsContent value="daily" className="space-y-8">
            {!fortuneData ? (
              <>
                <ZodiacSelector
                  onZodiacSelect={handleZodiacSelect}
                  onBirthDateSubmit={handleBirthDateSubmit}
                />
                
                {/* Top Ad Banner */}
                <AdBanner className="mt-8" />
              </>
            ) : (
              <>
                {fortuneMutation.isPending || birthDateMutation.isPending ? (
                  <div className="text-center py-12">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto mb-4"></div>
                    <p className="text-lg text-gray-600 dark:text-gray-300">운세를 불러오는 중...</p>
                  </div>
                ) : (
                  <>
                    <FortuneDisplay
                      zodiac={fortuneData.zodiac}
                      fortune={fortuneData.fortune}
                      currentDate={currentDate}
                    />
                    
                    {/* Middle Ad Banner */}
                    <AdBanner className="my-8" />
                    
                    <LuckyItems fortune={fortuneData.fortune} />
                    
                    {/* Action Buttons */}
                    <section className="text-center mt-8">
                      <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                        <Button
                          onClick={handleShare}
                          className="w-full sm:w-auto bg-red-600 hover:bg-red-800 text-white px-6 py-3 font-medium shadow-lg text-sm sm:text-base"
                        >
                          📤 운세 공유하기
                        </Button>
                        <Button
                          onClick={handleReset}
                          className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 font-medium shadow-lg text-sm sm:text-base"
                        >
                          🔄 다른 띠 선택하기
                        </Button>
                        <Button
                          onClick={handleSave}
                          disabled={saveFortuneMutation.isPending}
                          variant="outline"
                          className="w-full sm:w-auto border-2 border-yellow-400 text-red-800 dark:text-red-400 hover:bg-yellow-400 hover:text-white px-6 py-3 font-medium text-sm sm:text-base"
                        >
                          {saveFortuneMutation.isPending ? "저장 중..." : "💾 운세 저장하기"}
                        </Button>
                      </div>
                    </section>
                    
                    {/* Bottom Ad Banner */}
                    <AdBanner className="mt-8" />
                  </>
                )}
              </>
            )}
          </TabsContent>

          <TabsContent value="period" className="space-y-8">
            <PeriodFortuneComponent zodiacAnimals={zodiacAnimals} />
            <AdBanner />
          </TabsContent>

          <TabsContent value="compatibility" className="space-y-8">
            <CompatibilityChecker zodiacAnimals={zodiacAnimals} />
            <AdBanner />
          </TabsContent>

          <TabsContent value="history" className="space-y-8">
            <FortuneHistory />
            <AdBanner />
          </TabsContent>
        </Tabs>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 dark:bg-gray-950 text-white py-8 mt-16 transition-colors">
        <div className="container mx-auto px-4 text-center">
          <div className="mb-4">
            <h3 className="text-lg sm:text-xl font-bold mb-2">🔮 오늘의 운세</h3>
            <p className="text-gray-400 text-sm sm:text-base">전통 한국 운세로 매일 새로운 하루를 시작하세요</p>
          </div>
          <div className="border-t border-gray-700 pt-4">
            <p className="text-xs sm:text-sm text-gray-400">
              ⚠️ 운세는 참고용으로만 활용하시고, 중요한 결정은 신중히 내리시기 바랍니다.
            </p>
            <p className="text-xs text-gray-500 mt-2">
              © 2025 오늘의 운세. 모든 권리 보유. | tests.mahalohana-bruce.com
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
