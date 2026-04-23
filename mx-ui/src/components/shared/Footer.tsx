import { Link } from "react-router-dom";
import { GitFork, MessageCircle, ExternalLink } from "lucide-react";
import {
  SITE_NAME,
  COPYRIGHT_YEAR,
  TRADEMARK_NOTICE,
  FOOTER_SECTIONS,
  SOCIAL_LINKS,
} from "@/constants/site";
import { FeatureLink } from "@/components/shared/FeatureLink";
import { useFeatureFlags } from "@/hooks/useFeatureFlags";
import { ComingSoonModal } from "@/components/shared/ComingSoonModal";

const socialIcons: Record<string, React.ReactNode> = {
  github: <GitFork className="h-5 w-5" />,
  twitter: <ExternalLink className="h-5 w-5" />,
  discord: <MessageCircle className="h-5 w-5" />,
};

export function Footer() {
  const { isEnabled, guard, modalOpen, fallbackContent, closeModal } = useFeatureFlags();

  return (
    <footer className="border-t bg-background">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 gap-8 py-12 md:grid-cols-4">
          <div className="col-span-2 md:col-span-1">
            <Link to="/" className="flex items-center gap-2 font-bold text-lg text-foreground no-underline">
              <span className="inline-flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground text-sm font-bold">
                MX
              </span>
              {SITE_NAME}
            </Link>
            <p className="mt-3 text-sm text-muted-foreground max-w-xs">
              An autonomous AI coding agent that supercharges your development workflow.
            </p>
            <div className="mt-4 flex gap-3">
              {SOCIAL_LINKS.map((social) => {
                const featureKey = `social:${social.icon}`;
                const enabled = isEnabled(featureKey);
                return enabled ? (
                  <a
                    key={social.name}
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-muted-foreground hover:text-foreground transition-colors cursor-pointer"
                    aria-label={social.name}
                  >
                    {socialIcons[social.icon]}
                  </a>
                ) : (
                  <button
                    key={social.name}
                    type="button"
                    onClick={() => guard(featureKey)}
                    className="text-muted-foreground hover:text-foreground transition-colors cursor-pointer bg-transparent border-none p-0"
                    aria-label={social.name}
                  >
                    {socialIcons[social.icon]}
                  </button>
                );
              })}
            </div>
          </div>

          {FOOTER_SECTIONS.map((section) => (
            <div key={section.title}>
              <h4 className="text-sm font-semibold text-foreground">{section.title}</h4>
              <ul className="mt-3 space-y-2">
                {section.links.map((link) => (
                  <li key={link.label}>
                    <FeatureLink
                      to={link.href}
                      featureKey={link.href}
                      className="text-sm text-muted-foreground hover:text-foreground transition-colors no-underline"
                    >
                      {link.label}
                    </FeatureLink>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="border-t py-6 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-muted-foreground">
          <p>© {COPYRIGHT_YEAR} {SITE_NAME}. All rights reserved.</p>
          <p>{TRADEMARK_NOTICE}</p>
        </div>
      </div>

      <ComingSoonModal open={modalOpen} onClose={closeModal}>
        {fallbackContent}
      </ComingSoonModal>
    </footer>
  );
}
