# 한국 띠별 운세 웹 서비스

전통 한국식 띠별 운세를 제공하는 웹 애플리케이션입니다.

## 주요 기능

- 🐭 **띠별 오늘의 운세**: 12간지별 상세한 운세 정보 제공
- 📅 **생년월일 계산**: 생년월일 입력으로 자동 띠 계산
- 💕 **궁합 확인**: 두 띠 간의 궁합 분석
- 📊 **주간/월간 운세**: 장기간 운세 예측
- 💬 **오늘의 명언**: 매일 다른 동기부여 메시지
- 📱 **반응형 디자인**: 모바일과 데스크톱 최적화
- 🌙 **다크모드**: 밝기 조절 기능
- 🔤 **글씨 크기 조절**: 접근성을 위한 텍스트 크기 변경
- 💾 **운세 저장**: 개인 운세 기록 관리

## 기술 스택

### Frontend
- React 18 + TypeScript
- Vite (빌드 도구)
- Tailwind CSS + shadcn/ui
- TanStack Query (상태 관리)
- Wouter (라우팅)

### Backend
- Node.js + Express
- TypeScript
- PostgreSQL + Drizzle ORM
- 세션 기반 사용자 관리

## 설치 및 실행

### 1. 의존성 설치
```bash
npm install
```

### 2. 환경 변수 설정
```bash
# PostgreSQL 데이터베이스 URL 필요
DATABASE_URL=your_database_url
```

### 3. 데이터베이스 설정
```bash
npm run db:push
```

### 4. 개발 서버 실행
```bash
npm run dev
```

서버가 http://localhost:5000 에서 실행됩니다.

## 프로젝트 구조

```
├── client/                 # React 프론트엔드
│   ├── src/
│   │   ├── components/     # UI 컴포넌트
│   │   ├── pages/          # 페이지 컴포넌트
│   │   ├── hooks/          # 커스텀 훅
│   │   └── lib/            # 유틸리티 함수
├── server/                 # Express 백엔드
│   ├── index.ts           # 서버 진입점
│   ├── routes.ts          # API 라우트
│   ├── storage.ts         # 데이터 액세스 계층
│   └── db.ts              # 데이터베이스 연결
├── shared/                 # 공유 타입 및 스키마
│   └── schema.ts          # Drizzle 스키마
└── package.json
```

## API 엔드포인트

- `GET /api/zodiac-animals` - 모든 띠 정보 조회
- `GET /api/fortune/:zodiac` - 특정 띠의 오늘 운세
- `POST /api/calculate-zodiac` - 생년월일로 띠 계산
- `POST /api/compatibility` - 궁합 확인
- `POST /api/period-fortune` - 주간/월간 운세
- `GET /api/daily-quote` - 오늘의 명언
- `POST /api/save-fortune` - 운세 저장
- `GET /api/fortune-history` - 운세 기록 조회

## 배포

프로덕션 빌드:
```bash
npm run build
npm start
```

## 라이선스

MIT License

## 기여

이슈나 기능 제안은 GitHub Issues를 통해 제출해주세요.