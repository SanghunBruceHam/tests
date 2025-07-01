import { pgTable, text, serial, integer, timestamp, boolean } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";
import { relations } from "drizzle-orm";

export const zodiacAnimals = pgTable("zodiac_animals", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  emoji: text("emoji").notNull(),
  index: integer("index").notNull(),
});

export const fortunes = pgTable("fortunes", {
  id: serial("id").primaryKey(),
  zodiac: text("zodiac").notNull(),
  date: text("date").notNull(),
  overall: text("overall").notNull(),
  overallScore: integer("overall_score").notNull(),
  love: text("love").notNull(),
  loveScore: integer("love_score").notNull(),
  loveAdvice: text("love_advice").notNull(),
  money: text("money").notNull(),
  moneyScore: integer("money_score").notNull(),
  moneyAdvice: text("money_advice").notNull(),
  health: text("health").notNull(),
  healthScore: integer("health_score").notNull(),
  healthAdvice: text("health_advice").notNull(),
  career: text("career").notNull(),
  careerScore: integer("career_score").notNull(),
  careerAdvice: text("career_advice").notNull(),
  luckyColor: text("lucky_color").notNull(),
  luckyNumbers: text("lucky_numbers").notNull(),
  luckyDirection: text("lucky_direction").notNull(),
  luckyTime: text("lucky_time").notNull(),
});

export const insertFortuneSchema = createInsertSchema(fortunes);
export const insertZodiacAnimalSchema = createInsertSchema(zodiacAnimals);

export type Fortune = typeof fortunes.$inferSelect;
export type InsertFortune = z.infer<typeof insertFortuneSchema>;
export type ZodiacAnimal = typeof zodiacAnimals.$inferSelect;
export type InsertZodiacAnimal = z.infer<typeof insertZodiacAnimalSchema>;

// Zodiac calculation types
export const zodiacCalculationSchema = z.object({
  birthDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "생년월일 형식이 올바르지 않습니다"),
});

export type ZodiacCalculation = z.infer<typeof zodiacCalculationSchema>;

// Zodiac compatibility table
export const zodiacCompatibility = pgTable("zodiac_compatibility", {
  id: serial("id").primaryKey(),
  zodiac1: text("zodiac1").notNull(),
  zodiac2: text("zodiac2").notNull(),
  compatibilityScore: integer("compatibility_score").notNull(), // 1-5 stars
  description: text("description").notNull(),
});

// Weekly/Monthly fortune table
export const periodFortunes = pgTable("period_fortunes", {
  id: serial("id").primaryKey(),
  zodiac: text("zodiac").notNull(),
  period: text("period").notNull(), // 'weekly', 'monthly'
  startDate: text("start_date").notNull(),
  endDate: text("end_date").notNull(),
  overall: text("overall").notNull(),
  overallScore: integer("overall_score").notNull(),
  love: text("love").notNull(),
  loveScore: integer("love_score").notNull(),
  money: text("money").notNull(),
  moneyScore: integer("money_score").notNull(),
  health: text("health").notNull(),
  healthScore: integer("health_score").notNull(),
  career: text("career").notNull(),
  careerScore: integer("career_score").notNull(),
  advice: text("advice").notNull(),
});

// Daily quotes table
export const dailyQuotes = pgTable("daily_quotes", {
  id: serial("id").primaryKey(),
  date: text("date").notNull(),
  quote: text("quote").notNull(),
  author: text("author"),
  category: text("category").notNull(), // 'motivation', 'wisdom', 'success', etc.
});

// User saved fortunes (for history)
export const savedFortunes = pgTable("saved_fortunes", {
  id: serial("id").primaryKey(),
  sessionId: text("session_id").notNull(),
  zodiac: text("zodiac").notNull(),
  fortuneDate: text("fortune_date").notNull(),
  savedAt: timestamp("saved_at").defaultNow().notNull(),
  rating: integer("rating"), // User rating of fortune accuracy (1-5)
});

// Relations
export const zodiacCompatibilityRelations = relations(zodiacCompatibility, ({ one }) => ({
  zodiacAnimal1: one(zodiacAnimals, {
    fields: [zodiacCompatibility.zodiac1],
    references: [zodiacAnimals.name],
  }),
  zodiacAnimal2: one(zodiacAnimals, {
    fields: [zodiacCompatibility.zodiac2],
    references: [zodiacAnimals.name],
  }),
}));

// Insert schemas
export const insertZodiacCompatibilitySchema = createInsertSchema(zodiacCompatibility);
export const insertPeriodFortuneSchema = createInsertSchema(periodFortunes);
export const insertDailyQuoteSchema = createInsertSchema(dailyQuotes);
export const insertSavedFortuneSchema = createInsertSchema(savedFortunes);

// Types
export type ZodiacCompatibility = typeof zodiacCompatibility.$inferSelect;
export type InsertZodiacCompatibility = z.infer<typeof insertZodiacCompatibilitySchema>;
export type PeriodFortune = typeof periodFortunes.$inferSelect;
export type InsertPeriodFortune = z.infer<typeof insertPeriodFortuneSchema>;
export type DailyQuote = typeof dailyQuotes.$inferSelect;
export type InsertDailyQuote = z.infer<typeof insertDailyQuoteSchema>;
export type SavedFortune = typeof savedFortunes.$inferSelect;
export type InsertSavedFortune = z.infer<typeof insertSavedFortuneSchema>;

// Validation schemas
export const compatibilityCheckSchema = z.object({
  zodiac1: z.string().min(1, "첫 번째 띠를 선택해주세요"),
  zodiac2: z.string().min(1, "두 번째 띠를 선택해주세요"),
});

export const periodFortuneSchema = z.object({
  zodiac: z.string().min(1, "띠를 선택해주세요"),
  period: z.enum(["weekly", "monthly"], { message: "올바른 기간을 선택해주세요" }),
});

export const saveFortuneSchema = z.object({
  sessionId: z.string().min(1, "세션 ID가 필요합니다"),
  zodiac: z.string().min(1, "띠 정보가 필요합니다"),
  fortuneDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "날짜 형식이 올바르지 않습니다"),
  rating: z.number().min(1).max(5).optional(),
});

export type CompatibilityCheck = z.infer<typeof compatibilityCheckSchema>;
export type PeriodFortuneRequest = z.infer<typeof periodFortuneSchema>;
export type SaveFortuneRequest = z.infer<typeof saveFortuneSchema>;
