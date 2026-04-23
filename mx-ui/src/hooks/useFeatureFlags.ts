import { useState, useCallback } from "react";
import featureFlagsData from "@/data/featureFlags.json";
import type { FeatureKey } from "@/constants/features";

const flags = featureFlagsData as Record<string, boolean>;

function isEnabled(key: FeatureKey | string): boolean {
  return flags[key] ?? true;
}

export function useFeatureFlags() {
  const [modalOpen, setModalOpen] = useState(false);
  const [fallbackContent, setFallbackContent] = useState<React.ReactNode>(null);

  const openModal = useCallback((content?: React.ReactNode) => {
    setFallbackContent(content ?? null);
    setModalOpen(true);
  }, []);

  const closeModal = useCallback(() => {
    setModalOpen(false);
    setFallbackContent(null);
  }, []);

  const guard = useCallback(
    (key: FeatureKey | string, content?: React.ReactNode): boolean => {
      if (!isEnabled(key)) {
        openModal(content);
        return true;
      }
      return false;
    },
    [openModal]
  );

  return {
    isEnabled,
    guard,
    modalOpen,
    fallbackContent,
    openModal,
    closeModal,
  };
}
