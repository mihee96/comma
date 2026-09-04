# Comma Mobile (React Native + Expo)

## 개발 환경

- **Node.js 20 LTS** (`.nvmrc` 참고). `nvm use` 로 맞추세요.
- Expo Go 앱 (iOS / Android 스토어)

## 설치 / 실행

루트에서 `npm install` 하면 `postinstall` 이 이 폴더 의존성까지 설치합니다.
개별 실행도 가능:

```bash
npm ci            # package-lock.json 기준 정확한 버전 설치 (npm install 아님)
cp .env.example .env
npx expo start
```

보통은 **루트에서 `npm run dev`** (백엔드 + 모바일 동시). 이 폴더만 띄우려면
루트에서 `npm run dev:app`.

Expo Go 로 QR 스캔 → **Hello World 👋** + 백엔드 연결 상태 표시.

> 실기기 / 안드로이드 에뮬레이터에서는 `localhost` 가 PC 를 가리키지 않습니다.
> `.env` 의 `EXPO_PUBLIC_API_URL` 을 PC 의 LAN IP (`http://192.168.x.x:8000/api/v1`) 로 바꾸세요.

## 의존성 버전 관리

- `package.json` 은 정확한 버전으로 고정, **`package-lock.json` 이 실제 잠금파일**입니다.
- 최초 1회: 팀원 중 한 명이 `npm install` → `npx expo install --fix` (Expo SDK 에 맞춰
  네이티브 패키지 정렬) → 바뀐 `package.json` + `package-lock.json` 커밋.
- 이후 모두: `npm ci`.
- 패키지 추가는 `npx expo install <pkg>` (Expo 호환 버전 자동 선택) 후 락파일 커밋.

## 구조

```
src/
├── api/          axios 클라이언트 + 엔드포인트별 함수
├── navigation/   RootNavigator (react-navigation native-stack)
├── screens/      화면. user/ village/ 로 플로우 분리
├── components/   재사용 UI
├── store/        zustand 전역 상태 (useAuthStore)
├── hooks/        커스텀 훅
├── constants/    config(API URL), theme
├── types/        도메인 타입 (백엔드 스키마와 대응)
└── utils/        헬퍼
```

경로 별칭 `@/` → `src/` (Expo Metro 가 `tsconfig.json` paths 를 자동 인식).
