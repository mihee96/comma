import type { NativeStackScreenProps } from '@react-navigation/native-stack';

/** 앱 전체 네비게이션 파라미터. 화면이 늘어나면 여기에 추가합니다. */
export type RootStackParamList = {
  Home: undefined;
  // 사용자 플로우: Onboarding, VillageMatch, VillageDetail, ReservationRequest, VisitComplete, MyPage
  // 마을 플로우: VillageSignup, VillageProfile, Dashboard, ReservationManage, ReviewBoard, Insights
};

export type RootStackScreenProps<T extends keyof RootStackParamList> =
  NativeStackScreenProps<RootStackParamList, T>;
