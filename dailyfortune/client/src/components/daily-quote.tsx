import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { useQuery } from "@tanstack/react-query";
import type { DailyQuote } from "@shared/schema";

export function DailyQuoteComponent() {
  const { data: quote, isLoading } = useQuery<DailyQuote>({
    queryKey: ["/api/daily-quote"],
    staleTime: 1000 * 60 * 60 * 24, // 24시간 동안 신선하게 유지
  });

  if (isLoading) {
    return (
      <Card className="shadow-lg dark:bg-gray-800 animate-pulse">
        <CardContent className="p-6">
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-4"></div>
          <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
        </CardContent>
      </Card>
    );
  }

  if (!quote) return null;

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'motivation': return '🔥';
      case 'success': return '🏆';
      case 'wisdom': return '🧠';
      default: return '💭';
    }
  };

  const getCategoryName = (category: string) => {
    switch (category) {
      case 'motivation': return '동기부여';
      case 'success': return '성공';
      case 'wisdom': return '지혜';
      default: return '일반';
    }
  };

  return (
    <Card className="shadow-lg bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-900/30 dark:to-orange-900/30 dark:bg-gray-800 border-amber-200 dark:border-amber-800">
      <CardContent className="p-6">
        <div className="text-center">
          <div className="flex items-center justify-center mb-4">
            <span className="text-2xl mr-2">{getCategoryIcon(quote.category)}</span>
            <h3 className="text-lg font-bold text-gray-800 dark:text-gray-200">
              오늘의 명언
            </h3>
            <span className="ml-2 px-2 py-1 bg-amber-100 dark:bg-amber-900/50 text-amber-700 dark:text-amber-300 text-xs rounded-full">
              {getCategoryName(quote.category)}
            </span>
          </div>
          
          <blockquote className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-4 italic font-medium">
            "{quote.quote}"
          </blockquote>
          
          {quote.author && (
            <p className="text-sm text-gray-500 dark:text-gray-400">
              - {quote.author} -
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}