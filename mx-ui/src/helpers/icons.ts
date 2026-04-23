import {
  Terminal,
  FileEdit,
  Brain,
  ShieldCheck,
  Plug,
  GitBranch,
  Search,
  LayoutGrid,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

const iconMap: Record<string, LucideIcon> = {
  terminal: Terminal,
  "file-edit": FileEdit,
  brain: Brain,
  "shield-check": ShieldCheck,
  plug: Plug,
  "git-branch": GitBranch,
  search: Search,
  "layout-grid": LayoutGrid,
};

export function getIcon(name: string): LucideIcon {
  return iconMap[name] || Terminal;
}
