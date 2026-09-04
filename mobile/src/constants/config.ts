/**
 * 앱 전역 설정값. 환경변수는 EXPO_PUBLIC_ 접두사가 있어야 런타임에서 읽힙니다.
 */
export const API_BASE_URL: string =
  process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000/api/v1';

export const REQUEST_TIMEOUT_MS = 10_000;
