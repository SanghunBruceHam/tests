# Korean Zodiac Fortune Application

## Overview

This is a full-stack web application that provides daily Korean zodiac fortune readings. Users can either select their zodiac animal directly or calculate it by entering their birth date. The application generates personalized fortunes including overall luck, love, money, health, career advice, and lucky items for each day.

## System Architecture

The application follows a modern client-server architecture with the following key design decisions:

### Frontend Architecture
- **React 18** with TypeScript for type safety and modern React features
- **Vite** as the build tool for fast development and optimized production builds
- **Tailwind CSS** with shadcn/ui components for consistent, responsive design
- **TanStack Query** for efficient server state management and caching
- **Wouter** for lightweight client-side routing

### Backend Architecture
- **Express.js** server with TypeScript for robust API development
- **RESTful API** design with clear endpoints for zodiac data and fortune generation
- **Memory-based storage** with interface abstraction for future database migration
- **PostgreSQL-ready** schema using Drizzle ORM for when database persistence is needed

### Styling and UI
- **Korean traditional color scheme** with custom CSS variables
- **Responsive design** optimized for both desktop and mobile devices
- **shadcn/ui component library** configured with "new-york" style
- **Radix UI primitives** for accessible, unstyled components

## Key Components

### Backend Components
1. **Storage Layer** (`server/storage.ts`)
   - Abstract `IStorage` interface for future database implementations
   - `MemStorage` class providing in-memory data persistence
   - Predefined zodiac animals with Korean names and emojis
   - Fortune generation with randomized scores and advice

2. **API Routes** (`server/routes.ts`)
   - `GET /api/zodiac-animals` - Retrieve all zodiac animals
   - `GET /api/fortune/:zodiac` - Get today's fortune for specific zodiac
   - `POST /api/calculate-zodiac` - Calculate zodiac from birth date

3. **Server Configuration** (`server/index.ts`)
   - Express middleware setup with JSON parsing
   - Request logging with response capture
   - Error handling middleware
   - Vite integration for development

### Frontend Components
1. **ZodiacSelector** - Interactive grid for zodiac selection and birth date input
2. **FortuneDisplay** - Comprehensive fortune presentation with star ratings
3. **LuckyItems** - Display of daily lucky colors, numbers, directions, and times
4. **Fortune Page** - Main application logic coordinating user interactions

### Shared Components
1. **Schema Definitions** (`shared/schema.ts`)
   - Drizzle ORM table definitions for zodiac animals and fortunes
   - Zod validation schemas for API request/response types
   - TypeScript type exports for full-stack type safety

## Data Flow

1. **Initial Load**: Application fetches zodiac animals from `/api/zodiac-animals`
2. **Zodiac Selection**: User either selects zodiac directly or inputs birth date
3. **Birth Date Calculation**: If birth date provided, sends POST to `/api/calculate-zodiac`
4. **Fortune Retrieval**: Application fetches fortune data from `/api/fortune/:zodiac`
5. **Display**: Fortune data rendered with interactive UI components
6. **Caching**: TanStack Query handles response caching and background updates

## External Dependencies

### Core Framework Dependencies
- **React ecosystem**: react, react-dom, @vitejs/plugin-react
- **Backend**: express, tsx for TypeScript execution
- **Database**: drizzle-orm, @neondatabase/serverless, connect-pg-simple
- **Validation**: zod, drizzle-zod for schema validation

### UI and Styling
- **Component Library**: Complete shadcn/ui component set with Radix UI primitives
- **Styling**: tailwindcss, postcss, autoprefixer
- **Utilities**: class-variance-authority, clsx, tailwind-merge

### Development Tools
- **TypeScript**: Full TypeScript configuration for client, server, and shared code
- **Build Tools**: esbuild for server bundling, vite for client bundling
- **Replit Integration**: @replit/vite-plugin-runtime-error-modal, @replit/vite-plugin-cartographer

## Deployment Strategy

### Development Environment
- **Concurrent Development**: Server runs with tsx, client with Vite dev server
- **Hot Module Replacement**: Vite HMR for instant client-side updates
- **TypeScript Checking**: Continuous type checking across all modules
- **Replit Integration**: Specialized plugins for Replit development environment

### Production Build
- **Client Build**: Vite builds optimized React application to `dist/public`
- **Server Build**: esbuild bundles Express server to `dist/index.js`
- **Asset Optimization**: Vite handles code splitting, minification, and asset optimization
- **Environment Variables**: DATABASE_URL required for PostgreSQL connection

### Database Strategy
- **Current**: PostgreSQL database with Drizzle ORM (fully implemented)
- **Storage**: DatabaseStorage class with automatic data seeding
- **Tables**: zodiac_animals and fortunes tables deployed
- **Session Management**: connect-pg-simple configured for PostgreSQL sessions

Changelog:
- July 01, 2025. Initial setup
- July 01, 2025. Added Google AdSense integration, dark mode support, mobile optimization, SEO enhancements, and watermark

## Recent Changes
- Google AdSense: Integrated ad banners with client ID ca-pub-5508768187151867
- Dark/Light Mode: Added theme toggle with system preference detection
- Mobile Optimization: Responsive design with touch-friendly interactions
- SEO Enhancement: Meta tags, Open Graph, Twitter Cards, Korean language support
- Watermark: Added tests.mahalohana-bruce.com branding
- Accessibility: Improved contrast and font sizing for mobile devices
- Enhanced Features: Added zodiac compatibility checker, weekly/monthly fortunes, daily quotes, and fortune history tracking
- User Experience: Implemented tabbed navigation with persistent session management
- Database Expansion: Added new tables for compatibility, period fortunes, quotes, and user history

## User Preferences

Preferred communication style: Simple, everyday language.
Domain: tests.mahalohana-bruce.com
AdSense Client ID: ca-pub-5508768187151867