import { Link, type LinkProps } from "react-router-dom";
import { useFeatureFlags } from "@/hooks/useFeatureFlags";
import { ComingSoonModal } from "@/components/shared/ComingSoonModal";
import type { FeatureKey } from "@/constants/features";
import { cn } from "@/lib/utils";

interface FeatureLinkProps extends Omit<LinkProps, "to"> {
  to: string;
  featureKey: FeatureKey | string;
  fallback?: React.ReactNode;
  disabledClassName?: string;
}

export function FeatureLink({
  to,
  featureKey,
  fallback,
  children,
  className,
  disabledClassName,
  onClick,
  ...rest
}: FeatureLinkProps) {
  const { isEnabled, guard, modalOpen, fallbackContent, closeModal } = useFeatureFlags();

  if (!isEnabled(featureKey)) {
    return (
      <>
        <button
          type="button"
          onClick={(e) => {
            guard(featureKey, fallback);
            onClick?.(e as never);
          }}
          className={cn(className, disabledClassName, "cursor-pointer bg-transparent border-none p-0")}
        >
          {children}
        </button>
        <ComingSoonModal open={modalOpen} onClose={closeModal}>
          {fallbackContent}
        </ComingSoonModal>
      </>
    );
  }

  return (
    <Link to={to} className={className} onClick={onClick} {...rest}>
      {children}
    </Link>
  );
}
