import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { 
  zodiacCalculationSchema, 
  compatibilityCheckSchema, 
  periodFortuneSchema, 
  saveFortuneSchema 
} from "@shared/schema";

export async function registerRoutes(app: Express): Promise<Server> {
  // Get all zodiac animals
  app.get("/api/zodiac-animals", async (req, res) => {
    try {
      const animals = await storage.getZodiacAnimals();
      res.json(animals);
    } catch (error) {
      res.status(500).json({ error: "십이지 정보를 가져오는데 실패했습니다" });
    }
  });

  // Get fortune by zodiac name
  app.get("/api/fortune/:zodiac", async (req, res) => {
    try {
      const { zodiac } = req.params;
      const today = new Date().toISOString().split('T')[0];
      
      const fortune = await storage.generateFortune(zodiac, today);
      res.json(fortune);
    } catch (error) {
      res.status(500).json({ error: "운세 정보를 가져오는데 실패했습니다" });
    }
  });

  // Calculate zodiac from birth date
  app.post("/api/calculate-zodiac", async (req, res) => {
    try {
      const validatedData = zodiacCalculationSchema.parse(req.body);
      const { birthDate } = validatedData;
      
      const year = parseInt(birthDate.split('-')[0]);
      const zodiacIndex = (year - 4) % 12; // Chinese zodiac calculation
      
      const animals = await storage.getZodiacAnimals();
      const zodiacAnimal = animals.find(animal => animal.index === zodiacIndex);
      
      if (!zodiacAnimal) {
        return res.status(404).json({ error: "해당 년도의 띠를 찾을 수 없습니다" });
      }

      const today = new Date().toISOString().split('T')[0];
      const fortune = await storage.generateFortune(zodiacAnimal.name, today);
      
      res.json({
        zodiac: zodiacAnimal,
        fortune
      });
    } catch (error) {
      if (error instanceof Error) {
        res.status(400).json({ error: error.message });
      } else {
        res.status(500).json({ error: "생년월일 계산에 실패했습니다" });
      }
    }
  });

  // Get zodiac compatibility
  app.post("/api/compatibility", async (req, res) => {
    try {
      const validatedData = compatibilityCheckSchema.parse(req.body);
      const { zodiac1, zodiac2 } = validatedData;
      
      const compatibility = await storage.generateCompatibility(zodiac1, zodiac2);
      res.json(compatibility);
    } catch (error) {
      if (error instanceof Error) {
        res.status(400).json({ error: error.message });
      } else {
        res.status(500).json({ error: "궁합 확인에 실패했습니다" });
      }
    }
  });

  // Get period fortune (weekly/monthly)
  app.post("/api/period-fortune", async (req, res) => {
    try {
      const validatedData = periodFortuneSchema.parse(req.body);
      const { zodiac, period } = validatedData;
      
      const today = new Date();
      let startDate: string, endDate: string;
      
      if (period === 'weekly') {
        const startOfWeek = new Date(today);
        startOfWeek.setDate(today.getDate() - today.getDay());
        const endOfWeek = new Date(startOfWeek);
        endOfWeek.setDate(startOfWeek.getDate() + 6);
        
        startDate = startOfWeek.toISOString().split('T')[0];
        endDate = endOfWeek.toISOString().split('T')[0];
      } else {
        const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
        const endOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0);
        
        startDate = startOfMonth.toISOString().split('T')[0];
        endDate = endOfMonth.toISOString().split('T')[0];
      }
      
      const periodFortune = await storage.generatePeriodFortune(zodiac, period, startDate, endDate);
      res.json(periodFortune);
    } catch (error) {
      if (error instanceof Error) {
        res.status(400).json({ error: error.message });
      } else {
        res.status(500).json({ error: "기간별 운세를 가져오는데 실패했습니다" });
      }
    }
  });

  // Get daily quote
  app.get("/api/daily-quote", async (req, res) => {
    try {
      const today = new Date().toISOString().split('T')[0];
      const quote = await storage.generateDailyQuote(today);
      res.json(quote);
    } catch (error) {
      res.status(500).json({ error: "오늘의 명언을 가져오는데 실패했습니다" });
    }
  });

  // Save fortune to user history
  app.post("/api/save-fortune", async (req, res) => {
    try {
      const validatedData = saveFortuneSchema.parse(req.body);
      const { sessionId, zodiac, fortuneDate, rating } = validatedData;
      
      const savedFortune = await storage.saveFortune(sessionId, zodiac, fortuneDate, rating);
      res.json(savedFortune);
    } catch (error) {
      if (error instanceof Error) {
        res.status(400).json({ error: error.message });
      } else {
        res.status(500).json({ error: "운세 저장에 실패했습니다" });
      }
    }
  });

  // Get user's fortune history
  app.get("/api/fortune-history/:sessionId", async (req, res) => {
    try {
      const { sessionId } = req.params;
      const history = await storage.getSavedFortunes(sessionId);
      res.json(history);
    } catch (error) {
      res.status(500).json({ error: "운세 기록을 가져오는데 실패했습니다" });
    }
  });

  // Rate a fortune
  app.post("/api/rate-fortune", async (req, res) => {
    try {
      const { sessionId, zodiac, fortuneDate, rating } = req.body;
      
      if (!sessionId || !zodiac || !fortuneDate || !rating) {
        return res.status(400).json({ error: "필수 정보가 누락되었습니다" });
      }
      
      if (rating < 1 || rating > 5) {
        return res.status(400).json({ error: "평점은 1-5 사이여야 합니다" });
      }
      
      await storage.rateFortune(sessionId, zodiac, fortuneDate, rating);
      res.json({ message: "평점이 저장되었습니다" });
    } catch (error) {
      res.status(500).json({ error: "평점 저장에 실패했습니다" });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
