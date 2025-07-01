import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useToast } from "@/hooks/use-toast";
import { apiRequest } from "@/lib/queryClient";
import { getSessionId } from "@/lib/session";
import { Calendar } from "lucide-react";
import type { SavedFortune } from "@shared/schema";

export function FortuneHistory() {
  const [sessionId] = useState(getSessionId());
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const { data: history, isLoading } = useQuery<SavedFortune[]>({
    queryKey: ["/api/fortune-history", sessionId],
    enabled: !!sessionId,
  });

  const rateFortuneMutation = useMutation({
    mutationFn: async (data: { sessionId: string; zodiac: string; fortuneDate: string; rating: number }) => {
      const response = await apiRequest("POST", "/api/rate-fortune", data);
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/fortune-history", sessionId] });
      toast({
        title: "완료",
        description: "평점이 저장되었습니다",
      });
    },
    onError: (error) => {
      toast({
        title: "오류",
        description: error.message || "평점 저장에 실패했습니다",
        variant: "destructive",
      });
    },
  });

  const handleRating = (zodiac: string, fortuneDate: string, rating: number) => {
    rateFortuneMutation.mutate({ sessionId, zodiac, fortuneDate, rating });
  };

  const renderStars = (currentRating: number | null, isInteractive: boolean, onRate?: (rating: number) => void) => {
    return Array.from({ length: 5 }, (_, i) => (
      <button
        key={i}
        className={`text-lg ${
          i < (currentRating || 0) ? "text-yellow-400" : "text-gray-300 dark:text-gray-600"
        } ${isInteractive ? "hover:text-yellow-300 cursor-pointer" : "cursor-default"}`}
        onClick={() => isInteractive && onRate?.(i + 1)}
        disabled={!isInteractive}
      >
        ★
      </button>
    ));
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (isLoading) {
    return (
      <Card className="shadow-lg dark:bg-gray-800">
        <CardHeader>
          <CardTitle className="text-center text-xl font-bold text-gray-800 dark:text-gray-200">
            📚 운세 기록
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="animate-pulse">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!history || history.length === 0) {
    return (
      <Card className="shadow-lg dark:bg-gray-800">
        <CardHeader>
          <CardTitle className="text-center text-xl font-bold text-gray-800 dark:text-gray-200">
            📚 운세 기록
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <Calendar className="mx-auto h-12 w-12 text-gray-400 dark:text-gray-600 mb-4" />
            <p className="text-gray-500 dark:text-gray-400">아직 저장된 운세가 없습니다.</p>
            <p className="text-sm text-gray-400 dark:text-gray-500 mt-2">
              운세를 확인한 후 저장 버튼을 눌러보세요.
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="shadow-lg dark:bg-gray-800">
      <CardHeader>
        <CardTitle className="text-center text-xl font-bold text-gray-800 dark:text-gray-200">
          📚 운세 기록 ({history.length}개)
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {history.map((fortune) => (
            <div
              key={fortune.id}
              className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900/50"
            >
              <div className="flex items-center justify-between mb-3">
                <div>
                  <h4 className="font-semibold text-gray-800 dark:text-gray-200">
                    {fortune.zodiac}띠 운세
                  </h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {formatDate(fortune.fortuneDate)}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-xs text-gray-400 dark:text-gray-500 mb-1">
                    저장일: {new Date(fortune.savedAt).toLocaleDateString('ko-KR')}
                  </p>
                </div>
              </div>

              <div className="border-t border-gray-200 dark:border-gray-700 pt-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    운세 정확도 평가:
                  </span>
                  <div className="flex space-x-1">
                    {renderStars(
                      fortune.rating,
                      !fortune.rating,
                      (rating) => handleRating(fortune.zodiac, fortune.fortuneDate, rating)
                    )}
                  </div>
                </div>
                {!fortune.rating && (
                  <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                    별점을 클릭하여 운세 정확도를 평가해주세요
                  </p>
                )}
                {fortune.rating && (
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    평가 완료: {fortune.rating}/5점
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}