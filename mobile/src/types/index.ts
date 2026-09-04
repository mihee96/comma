/** 백엔드 스키마와 대응하는 도메인 타입 (mockup_v2.pdf 플로우 기준) */

export type UserRole = 'user' | 'village';

export interface User {
  id: number;
  email: string;
  displayName: string;
  role: UserRole;
  createdAt: string;
}

export interface Village {
  id: number;
  ownerId: number;
  name: string;
  region: string;
  description: string;
  isVerified: boolean;
  createdAt: string;
}

export type ReservationStatus = 'pending' | 'approved' | 'rejected' | 'completed';

export interface Reservation {
  id: number;
  userId: number;
  villageId: number;
  status: ReservationStatus;
  startDate: string;
  endDate: string;
  partySize: number;
  note: string | null;
  createdAt: string;
}

export interface Review {
  id: number;
  villageId: number;
  userId: number;
  rating: number;
  content: string;
  createdAt: string;
}

export interface Subscription {
  id: number;
  userId: number;
  villageId: number;
  createdAt: string;
}

export interface AuthTokens {
  accessToken: string;
  tokenType: string;
}
