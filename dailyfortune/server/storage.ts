import { 
  type Fortune, 
  type ZodiacAnimal, 
  type InsertFortune, 
  type InsertZodiacAnimal,
  type ZodiacCompatibility,
  type InsertZodiacCompatibility,
  type PeriodFortune,
  type InsertPeriodFortune,
  type DailyQuote,
  type InsertDailyQuote,
  type SavedFortune,
  type InsertSavedFortune,
  zodiacAnimals, 
  fortunes,
  zodiacCompatibility,
  periodFortunes,
  dailyQuotes,
  savedFortunes
} from "@shared/schema";
import { db } from "./db";
import { eq, and, desc, gte, lte } from "drizzle-orm";

export interface IStorage {
  getZodiacAnimals(): Promise<ZodiacAnimal[]>;
  getFortuneByZodiacAndDate(zodiac: string, date: string): Promise<Fortune | undefined>;
  generateFortune(zodiac: string, date: string): Promise<Fortune>;
  
  // Compatibility features
  getZodiacCompatibility(zodiac1: string, zodiac2: string): Promise<ZodiacCompatibility | undefined>;
  generateCompatibility(zodiac1: string, zodiac2: string): Promise<ZodiacCompatibility>;
  
  // Period fortunes
  getPeriodFortune(zodiac: string, period: 'weekly' | 'monthly', date: string): Promise<PeriodFortune | undefined>;
  generatePeriodFortune(zodiac: string, period: 'weekly' | 'monthly', startDate: string, endDate: string): Promise<PeriodFortune>;
  
  // Daily quotes
  getDailyQuote(date: string): Promise<DailyQuote | undefined>;
  generateDailyQuote(date: string): Promise<DailyQuote>;
  
  // User history
  saveFortune(sessionId: string, zodiac: string, fortuneDate: string, rating?: number): Promise<SavedFortune>;
  getSavedFortunes(sessionId: string): Promise<SavedFortune[]>;
  rateFortune(sessionId: string, zodiac: string, fortuneDate: string, rating: number): Promise<void>;
}



export class DatabaseStorage implements IStorage {
  async getZodiacAnimals(): Promise<ZodiacAnimal[]> {
    try {
      const animals = await db.select().from(zodiacAnimals).orderBy(zodiacAnimals.index);
      
      // If no animals in database, seed with initial data
      if (animals.length === 0) {
        await this.seedZodiacAnimals();
        return await db.select().from(zodiacAnimals).orderBy(zodiacAnimals.index);
      }
      
      return animals;
    } catch (error) {
      console.error('Error fetching zodiac animals:', error);
      throw error;
    }
  }

  async getFortuneByZodiacAndDate(zodiac: string, date: string): Promise<Fortune | undefined> {
    try {
      const [fortune] = await db
        .select()
        .from(fortunes)
        .where(and(eq(fortunes.zodiac, zodiac), eq(fortunes.date, date)));
      return fortune || undefined;
    } catch (error) {
      console.error('Error fetching fortune:', error);
      throw error;
    }
  }

  async generateFortune(zodiac: string, date: string): Promise<Fortune> {
    try {
      // Check if fortune already exists
      const existing = await this.getFortuneByZodiacAndDate(zodiac, date);
      if (existing) {
        return existing;
      }

      // Generate new fortune
      const fortuneTemplates = this.getFortuneTemplates(zodiac);
      const template = fortuneTemplates[Math.floor(Math.random() * fortuneTemplates.length)];

      const fortuneData: InsertFortune = {
        zodiac,
        date,
        overall: template.overall,
        overallScore: this.getRandomScore(),
        love: template.love,
        loveScore: this.getRandomScore(),
        loveAdvice: template.loveAdvice,
        money: template.money,
        moneyScore: this.getRandomScore(),
        moneyAdvice: template.moneyAdvice,
        health: template.health,
        healthScore: this.getRandomScore(),
        healthAdvice: template.healthAdvice,
        career: template.career,
        careerScore: this.getRandomScore(),
        careerAdvice: template.careerAdvice,
        luckyColor: template.luckyColor,
        luckyNumbers: template.luckyNumbers,
        luckyDirection: template.luckyDirection,
        luckyTime: template.luckyTime,
      };

      const [newFortune] = await db.insert(fortunes).values(fortuneData).returning();
      return newFortune;
    } catch (error) {
      console.error('Error generating fortune:', error);
      throw error;
    }
  }

  private async seedZodiacAnimals(): Promise<void> {
    const initialAnimals: InsertZodiacAnimal[] = [
      { name: "쥐", emoji: "🐭", index: 0 },
      { name: "소", emoji: "🐮", index: 1 },
      { name: "호랑이", emoji: "🐯", index: 2 },
      { name: "토끼", emoji: "🐰", index: 3 },
      { name: "용", emoji: "🐲", index: 4 },
      { name: "뱀", emoji: "🐍", index: 5 },
      { name: "말", emoji: "🐴", index: 6 },
      { name: "양", emoji: "🐑", index: 7 },
      { name: "원숭이", emoji: "🐵", index: 8 },
      { name: "닭", emoji: "🐓", index: 9 },
      { name: "개", emoji: "🐕", index: 10 },
      { name: "돼지", emoji: "🐷", index: 11 },
    ];

    await db.insert(zodiacAnimals).values(initialAnimals);
  }

  private getRandomScore(): number {
    return Math.floor(Math.random() * 5) + 1; // 1-5 stars
  }

  private getFortuneTemplates(zodiac: string) {
    const templates = [
      {
        overall: `${zodiac}띠에게 특별히 좋은 기운이 흐르는 날입니다. 새로운 기회가 찾아올 수 있으니 적극적인 자세로 하루를 시작하세요.`,
        love: "연인과의 관계가 더욱 깊어질 수 있는 날입니다. 솔직한 대화를 나누어보세요.",
        loveAdvice: "상대방의 마음을 이해하려 노력하세요",
        money: "무리한 투자는 피하고, 신중한 계획을 세우는 것이 좋겠습니다.",
        moneyAdvice: "가계부 작성으로 지출을 관리하세요",
        health: "전반적으로 좋은 컨디션을 유지할 수 있을 것 같습니다. 가벼운 운동을 추천합니다.",
        healthAdvice: "충분한 수분 섭취를 잊지 마세요",
        career: "새로운 프로젝트나 업무에서 좋은 성과를 거둘 수 있는 날입니다.",
        careerAdvice: "동료들과의 협력을 중시하세요",
        luckyColor: "빨간색",
        luckyNumbers: "7, 14",
        luckyDirection: "동쪽",
        luckyTime: "오후 2-4시"
      },
      {
        overall: `${zodiac}띠에게 평온한 하루가 될 것 같습니다. 작은 변화도 큰 행운을 가져다줄 수 있으니 긍정적인 마음가짐을 유지하세요.`,
        love: "가족이나 친구들과의 시간을 소중히 여기세요. 따뜻한 관계가 더욱 돈독해질 것입니다.",
        loveAdvice: "진심 어린 말 한마디가 큰 힘이 됩니다",
        money: "예상치 못한 수입이 생길 가능성이 있습니다. 하지만 계획적인 소비를 하세요.",
        moneyAdvice: "작은 돈도 모으면 큰 힘이 됩니다",
        health: "스트레스 관리에 신경 쓰세요. 충분한 휴식이 필요한 시기입니다.",
        healthAdvice: "자연 속에서 휴식을 취해보세요",
        career: "인내심이 필요한 시기입니다. 꾸준한 노력이 좋은 결과를 가져다줄 것입니다.",
        careerAdvice: "멘토의 조언을 구해보세요",
        luckyColor: "파란색",
        luckyNumbers: "3, 21",
        luckyDirection: "서쪽",
        luckyTime: "오전 10-12시"
      },
      {
        overall: `${zodiac}띠에게 도전의 기회가 찾아오는 날입니다. 두려워하지 말고 새로운 시도를 해보세요.`,
        love: "솔로라면 새로운 만남의 기회가 있을 수 있습니다. 자신감을 가지고 적극적으로 나서보세요.",
        loveAdvice: "첫인상이 중요합니다. 밝은 미소를 잊지 마세요",
        money: "투자보다는 저축에 집중하는 것이 좋겠습니다. 안정적인 재정 관리가 필요합니다.",
        moneyAdvice: "충동구매를 자제하고 신중하게 결정하세요",
        health: "규칙적인 운동과 식습관 개선이 필요합니다. 건강한 생활 리듬을 만들어보세요.",
        healthAdvice: "금연, 금주가 건강에 도움이 됩니다",
        career: "창의적인 아이디어가 빛을 발할 때입니다. 자신의 능력을 믿고 도전하세요.",
        careerAdvice: "새로운 기술 습득에 투자하세요",
        luckyColor: "초록색",
        luckyNumbers: "5, 18",
        luckyDirection: "남쪽",
        luckyTime: "오후 6-8시"
      }
    ];

    return templates;
  }

  // Compatibility methods
  async getZodiacCompatibility(zodiac1: string, zodiac2: string): Promise<ZodiacCompatibility | undefined> {
    try {
      const [compatibility] = await db
        .select()
        .from(zodiacCompatibility)
        .where(
          and(
            eq(zodiacCompatibility.zodiac1, zodiac1),
            eq(zodiacCompatibility.zodiac2, zodiac2)
          )
        );
      return compatibility || undefined;
    } catch (error) {
      console.error('Error fetching compatibility:', error);
      throw error;
    }
  }

  async generateCompatibility(zodiac1: string, zodiac2: string): Promise<ZodiacCompatibility> {
    try {
      // Check if compatibility already exists
      const existing = await this.getZodiacCompatibility(zodiac1, zodiac2);
      if (existing) {
        return existing;
      }

      // Generate compatibility data
      const compatibilityData = this.getCompatibilityData(zodiac1, zodiac2);
      const newCompatibility: InsertZodiacCompatibility = {
        zodiac1,
        zodiac2,
        compatibilityScore: compatibilityData.score,
        description: compatibilityData.description,
      };

      const [result] = await db.insert(zodiacCompatibility).values(newCompatibility).returning();
      return result;
    } catch (error) {
      console.error('Error generating compatibility:', error);
      throw error;
    }
  }

  // Period fortune methods
  async getPeriodFortune(zodiac: string, period: 'weekly' | 'monthly', date: string): Promise<PeriodFortune | undefined> {
    try {
      const [fortune] = await db
        .select()
        .from(periodFortunes)
        .where(
          and(
            eq(periodFortunes.zodiac, zodiac),
            eq(periodFortunes.period, period),
            lte(periodFortunes.startDate, date),
            gte(periodFortunes.endDate, date)
          )
        );
      return fortune || undefined;
    } catch (error) {
      console.error('Error fetching period fortune:', error);
      throw error;
    }
  }

  async generatePeriodFortune(zodiac: string, period: 'weekly' | 'monthly', startDate: string, endDate: string): Promise<PeriodFortune> {
    try {
      const existing = await this.getPeriodFortune(zodiac, period, startDate);
      if (existing) {
        return existing;
      }

      const fortuneData = this.getPeriodFortuneData(zodiac, period);
      const newFortune: InsertPeriodFortune = {
        zodiac,
        period,
        startDate,
        endDate,
        overall: fortuneData.overall,
        overallScore: this.getRandomScore(),
        love: fortuneData.love,
        loveScore: this.getRandomScore(),
        money: fortuneData.money,
        moneyScore: this.getRandomScore(),
        health: fortuneData.health,
        healthScore: this.getRandomScore(),
        career: fortuneData.career,
        careerScore: this.getRandomScore(),
        advice: fortuneData.advice,
      };

      const [result] = await db.insert(periodFortunes).values(newFortune).returning();
      return result;
    } catch (error) {
      console.error('Error generating period fortune:', error);
      throw error;
    }
  }

  // Daily quote methods
  async getDailyQuote(date: string): Promise<DailyQuote | undefined> {
    try {
      const [quote] = await db
        .select()
        .from(dailyQuotes)
        .where(eq(dailyQuotes.date, date));
      return quote || undefined;
    } catch (error) {
      console.error('Error fetching daily quote:', error);
      throw error;
    }
  }

  async generateDailyQuote(date: string): Promise<DailyQuote> {
    try {
      const existing = await this.getDailyQuote(date);
      if (existing) {
        return existing;
      }

      const quoteData = this.getRandomQuote();
      const newQuote: InsertDailyQuote = {
        date,
        quote: quoteData.quote,
        author: quoteData.author,
        category: quoteData.category,
      };

      const [result] = await db.insert(dailyQuotes).values(newQuote).returning();
      return result;
    } catch (error) {
      console.error('Error generating daily quote:', error);
      throw error;
    }
  }

  // User history methods
  async saveFortune(sessionId: string, zodiac: string, fortuneDate: string, rating?: number): Promise<SavedFortune> {
    try {
      const fortuneData: InsertSavedFortune = {
        sessionId,
        zodiac,
        fortuneDate,
        rating,
      };

      const [result] = await db.insert(savedFortunes).values(fortuneData).returning();
      return result;
    } catch (error) {
      console.error('Error saving fortune:', error);
      throw error;
    }
  }

  async getSavedFortunes(sessionId: string): Promise<SavedFortune[]> {
    try {
      const fortunes = await db
        .select()
        .from(savedFortunes)
        .where(eq(savedFortunes.sessionId, sessionId))
        .orderBy(desc(savedFortunes.savedAt));
      return fortunes;
    } catch (error) {
      console.error('Error fetching saved fortunes:', error);
      throw error;
    }
  }

  async rateFortune(sessionId: string, zodiac: string, fortuneDate: string, rating: number): Promise<void> {
    try {
      await db
        .update(savedFortunes)
        .set({ rating })
        .where(
          and(
            eq(savedFortunes.sessionId, sessionId),
            eq(savedFortunes.zodiac, zodiac),
            eq(savedFortunes.fortuneDate, fortuneDate)
          )
        );
    } catch (error) {
      console.error('Error rating fortune:', error);
      throw error;
    }
  }

  // Helper methods for generating content
  private getCompatibilityData(zodiac1: string, zodiac2: string) {
    const compatibilityMatrix: { [key: string]: { [key: string]: { score: number; description: string } } } = {
      "쥐": {
        "용": { score: 5, description: "쥐와 용은 완벽한 조화를 이룹니다. 서로를 보완하며 큰 성공을 거둘 수 있는 궁합입니다." },
        "원숭이": { score: 4, description: "쥐와 원숭이는 지적인 교감이 깊어 좋은 파트너가 될 수 있습니다." },
        "소": { score: 4, description: "쥐와 소는 안정적이고 신뢰할 수 있는 관계를 만들어갑니다." }
      },
      "소": {
        "뱀": { score: 5, description: "소와 뱀은 서로의 차이점을 인정하며 조화로운 관계를 유지합니다." },
        "닭": { score: 4, description: "소와 닭은 실용적이고 체계적인 관계를 형성합니다." },
        "쥐": { score: 4, description: "소와 쥐는 상호 보완적인 관계로 안정감을 줍니다." }
      },
      "호랑이": {
        "말": { score: 5, description: "호랑이와 말은 역동적이고 열정적인 관계를 만들어갑니다." },
        "개": { score: 4, description: "호랑이와 개는 충성스럽고 진실한 관계를 유지합니다." },
        "돼지": { score: 4, description: "호랑이와 돼지는 서로를 이해하고 배려하는 관계입니다." }
      }
    };

    const defaultCompatibility = { 
      score: Math.floor(Math.random() * 3) + 2, // 2-4 점
      description: `${zodiac1}와 ${zodiac2}는 서로 다른 매력을 가지고 있어 새로운 것을 배울 수 있는 관계입니다.` 
    };

    return compatibilityMatrix[zodiac1]?.[zodiac2] || 
           compatibilityMatrix[zodiac2]?.[zodiac1] || 
           defaultCompatibility;
  }

  private getPeriodFortuneData(zodiac: string, period: 'weekly' | 'monthly') {
    const periodType = period === 'weekly' ? '이번 주' : '이번 달';
    
    const templates = [
      {
        overall: `${zodiac}띠에게 ${periodType}는 새로운 시작의 기회가 많은 시기입니다. 계획했던 일들을 실행에 옮기기 좋은 때입니다.`,
        love: `${periodType}는 관계 개선에 좋은 시기입니다. 솔직한 대화를 통해 더 깊은 유대감을 형성할 수 있습니다.`,
        money: `재정 관리에 신중함이 필요한 시기입니다. 큰 지출보다는 안정적인 투자에 집중하세요.`,
        health: `규칙적인 생활 패턴을 유지하는 것이 중요합니다. 충분한 휴식과 운동을 병행하세요.`,
        career: `업무에서 창의적인 아이디어가 빛을 발할 시기입니다. 적극적으로 의견을 제시해보세요.`,
        advice: `변화를 두려워하지 말고 새로운 도전을 받아들이세요. 작은 변화가 큰 성과로 이어질 수 있습니다.`
      },
      {
        overall: `${zodiac}띠에게 ${periodType}는 안정과 성장이 조화를 이루는 시기입니다. 꾸준함이 성공의 열쇠가 될 것입니다.`,
        love: `가족과 친구들과의 시간을 늘려보세요. 따뜻한 인간관계가 더욱 돈독해질 것입니다.`,
        money: `예상치 못한 수입이 생길 가능성이 있습니다. 하지만 계획적인 소비 습관을 유지하세요.`,
        health: `스트레스 관리에 특별히 신경 쓰세요. 명상이나 취미 활동이 도움이 될 것입니다.`,
        career: `동료들과의 협력이 중요한 시기입니다. 팀워크를 발휘하여 좋은 결과를 얻을 수 있습니다.`,
        advice: `인내심을 갖고 꾸준히 노력하세요. 결과는 늦더라도 반드시 따라올 것입니다.`
      }
    ];

    return templates[Math.floor(Math.random() * templates.length)];
  }

  private getRandomQuote() {
    const quotes = [
      {
        quote: "성공은 준비와 기회가 만나는 지점에서 일어난다.",
        author: "바비 언서",
        category: "success"
      },
      {
        quote: "오늘 할 수 있는 일을 내일로 미루지 마라.",
        author: "벤자민 프랭클린",
        category: "motivation"
      },
      {
        quote: "행복은 습관이다. 그것을 몸에 지녀라.",
        author: "허버드",
        category: "wisdom"
      },
      {
        quote: "변화를 원한다면 자신이 변화가 되어야 한다.",
        author: "마하트마 간디",
        category: "motivation"
      },
      {
        quote: "인생은 10%의 일어나는 일과 90%의 그에 대한 반응이다.",
        author: "찰스 스윈돌",
        category: "wisdom"
      },
      {
        quote: "꿈을 꾸는 것은 계획을 세우는 첫 번째 단계다.",
        author: "미상",
        category: "motivation"
      },
      {
        quote: "실패는 성공을 위한 연습이다.",
        author: "미상",
        category: "success"
      },
      {
        quote: "좋은 하루는 좋은 생각에서 시작된다.",
        author: "미상",
        category: "wisdom"
      }
    ];

    return quotes[Math.floor(Math.random() * quotes.length)];
  }
}

export const storage = new DatabaseStorage();
