import { create } from 'zustand';

import type { UserRole } from '@/types';

interface AuthState {
  token: string | null;
  role: UserRole | null;
  setAuth: (token: string, role: UserRole) => void;
  clear: () => void;
}

/**
 * 인증 상태 (메모리 저장). 영속화가 필요하면 expo-secure-store 로 확장하세요.
 */
export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  role: null,
  setAuth: (token, role) => set({ token, role }),
  clear: () => set({ token: null, role: null }),
}));
