import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useToast } from "@/hooks/use-toast";
import { apiRequest } from "@/lib/queryClient";
import type { ZodiacAnimal, ZodiacCompatibility } from "@shared/schema";

interface CompatibilityCheckerProps {
  zodiacAnimals?: ZodiacAnimal[];
}

export function CompatibilityChecker({ zodiacAnimals }: CompatibilityCheckerProps) {
  const [zodiac1, setZodiac1] = useState<string>("");
  const [zodiac2, setZodiac2] = useState<string>("");
  const [compatibility, setCompatibility] = useState<ZodiacCompatibility | null>(null);
  const { toast } = useToast();

  const compatibilityMutation = useMutation({
    mutationFn: async (data: { zodiac1: string; zodiac2: string }) => {
      const response = await apiRequest("POST", "/api/compatibility", data);
      return response.json();
    },
    onSuccess: (data) => {
      setCompatibility(data);
    },
    onError: (error) => {
      toast({
        title: "오류",
        description: error.message || "궁합 확인에 실패했습니다",
        variant: "destructive",
      });
    },
  });

  const handleCheckCompatibility = () => {
    if (!zodiac1 || !zodiac2) {
      toast({
        title: "알림",
        description: "두 띠를 모두 선택해주세요",
        variant: "destructive",
      });
      return;
    }

    if (zodiac1 === zodiac2) {
      toast({
        title: "알림", 
        description: "같은 띠는 선택할 수 없습니다",
        variant: "destructive",
      });
      return;
    }

    compatibilityMutation.mutate({ zodiac1, zodiac2 });
  };

  const renderStars = (score: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <span key={i} className={`text-xl ${i < score ? "text-yellow-400" : "text-gray-300 dark:text-gray-600"}`}>
        ★
      </span>
    ));
  };

  return (
    <Card className="shadow-lg dark:bg-gray-800">
      <CardHeader>
        <CardTitle className="text-center text-xl font-bold text-gray-800 dark:text-gray-200">
          💕 띠별 궁합 확인
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
              첫 번째 띠
            </label>
            <Select value={zodiac1} onValueChange={setZodiac1}>
              <SelectTrigger className="dark:bg-gray-700 dark:border-gray-600">
                <SelectValue placeholder="띠 선택" />
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

          <div>
            <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
              두 번째 띠
            </label>
            <Select value={zodiac2} onValueChange={setZodiac2}>
              <SelectTrigger className="dark:bg-gray-700 dark:border-gray-600">
                <SelectValue placeholder="띠 선택" />
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
        </div>

        <Button
          onClick={handleCheckCompatibility}
          disabled={compatibilityMutation.isPending}
          className="w-full bg-red-600 hover:bg-red-700 dark:bg-red-700 dark:hover:bg-red-800 text-white font-medium py-3"
        >
          {compatibilityMutation.isPending ? "확인 중..." : "궁합 확인하기"}
        </Button>

        {compatibility && (
          <div className="mt-6 p-6 bg-gradient-to-br from-pink-50 to-red-50 dark:from-pink-900/30 dark:to-red-900/30 rounded-lg border border-red-200 dark:border-red-800">
            <div className="text-center mb-4">
              <h3 className="text-lg font-bold text-gray-800 dark:text-gray-200 mb-2">
                {compatibility.zodiac1} ❤️ {compatibility.zodiac2}
              </h3>
              <div className="flex justify-center space-x-1 mb-3">
                {renderStars(compatibility.compatibilityScore)}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                궁합 점수: {compatibility.compatibilityScore}/5
              </div>
            </div>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed text-center">
              {compatibility.description}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}