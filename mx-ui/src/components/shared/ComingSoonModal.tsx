import { Clock } from "lucide-react";
import { Modal } from "@/components/shared/Modal";
import { cn } from "@/lib/utils";

interface ComingSoonModalProps {
  open: boolean;
  onClose: () => void;
  className?: string;
  children?: React.ReactNode;
}

export function ComingSoonModal({ open, onClose, className, children }: ComingSoonModalProps) {
  return (
    <Modal open={open} onClose={onClose} className={cn("text-center", className)}>
      {children ?? (
        <div className="flex flex-col items-center gap-4 py-4">
          <div className="rounded-full bg-primary/10 p-4">
            <Clock className="h-8 w-8 text-primary" />
          </div>
          <h2 className="text-xl font-bold text-foreground">Coming Soon</h2>
          <p className="text-sm text-muted-foreground max-w-xs">
            This feature is currently under development. Please stay tuned for updates!
          </p>
        </div>
      )}
    </Modal>
  );
}
