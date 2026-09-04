import axios from 'axios';

import { API_BASE_URL, REQUEST_TIMEOUT_MS } from '@/constants/config';
import { useAuthStore } from '@/store/useAuthStore';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: REQUEST_TIMEOUT_MS,
});

// 저장된 토큰이 있으면 Authorization 헤더에 자동 첨부
apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
