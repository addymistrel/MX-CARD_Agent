import type { NavLink, FooterSection, SocialLink } from "@/types";

export const SITE_NAME = "MX-CARD Agent";
export const SITE_TAGLINE = "Open-source AI for the terminal-first workflow";
export const SITE_DESCRIPTION =
  "A lightweight open-source coding agent for developers who want a fast terminal workflow, clear automation, and transparent software built to stay in the loop.";
export const COPYRIGHT_YEAR = 2026;
export const TRADEMARK_NOTICE =
  "MX-CARD Agent is open source and built for the developer community.";

export const NAV_LINKS: NavLink[] = [
  { label: "Home", href: "/" },
  { label: "Docs", href: "/docs" },
  { label: "Contact", href: "/contact" },
];

export const FOOTER_SECTIONS: FooterSection[] = [
  {
    title: "Project",
    links: [
      { label: "Home", href: "/" },
      { label: "Docs", href: "/docs" },
      { label: "Contact", href: "/contact" },
    ],
  },
  {
    title: "Resources",
    links: [
      { label: "GitHub", href: "/docs" },
      { label: "Contributing", href: "/docs" },
      { label: "Roadmap", href: "/docs" },
    ],
  },
  {
    title: "Community",
    links: [
      { label: "Support", href: "/contact" },
      { label: "Feedback", href: "/contact" },
      { label: "Issues", href: "/contact" },
    ],
  },
];

export const SOCIAL_LINKS: SocialLink[] = [
  {
    name: "GitHub",
    href: "https://github.com/addymistrel/MX-CARD_Agent",
    icon: "github",
  },
  { name: "Twitter", href: "https://twitter.com", icon: "twitter" },
  { name: "Discord", href: "https://discord.gg", icon: "discord" },
];
