import { useQuery } from '@tanstack/react-query';
import { ActivityIndicator, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { fetchHealth } from '@/api/health';
import { API_BASE_URL } from '@/constants/config';
import { colors, spacing } from '@/constants/theme';

export default function HomeScreen() {
  const health = useQuery({
    queryKey: ['health'],
    queryFn: fetchHealth,
    retry: false,
  });

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Hello World 👋</Text>
      <Text style={styles.subtitle}>촌스테이 · Comma</Text>

      <View style={styles.card}>
        <Text style={styles.cardLabel}>백엔드 상태</Text>
        {health.isLoading ? (
          <ActivityIndicator color={colors.primary} />
        ) : health.isError ? (
          <Text style={styles.error}>연결 실패 — 서버가 켜져 있나요?</Text>
        ) : (
          <Text style={styles.ok}>정상 ({health.data?.status})</Text>
        )}
        <Text style={styles.endpoint}>{API_BASE_URL}</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.bg,
    padding: spacing.lg,
    gap: spacing.sm,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: colors.text,
  },
  subtitle: {
    fontSize: 15,
    color: colors.textMuted,
    marginBottom: spacing.lg,
  },
  card: {
    width: '100%',
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 12,
    padding: spacing.md,
    alignItems: 'center',
    gap: spacing.xs,
  },
  cardLabel: {
    fontSize: 13,
    color: colors.textMuted,
  },
  ok: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.primary,
  },
  error: {
    fontSize: 15,
    fontWeight: '600',
    color: colors.danger,
    textAlign: 'center',
  },
  endpoint: {
    fontSize: 11,
    color: colors.textMuted,
  },
});
