import type { NavLink, FooterSection, SocialLink } from "@/types";

export const SITE_NAME = "MX-CARD Agent";
export const SITE_TAGLINE = "Your AI-Powered Coding Companion";
export const SITE_DESCRIPTION =
  "An autonomous AI coding agent that reads, writes, edits files, runs shell commands, and manages complex projects - all from your terminal.";
export const COPYRIGHT_YEAR = 2026;
export const TRADEMARK_NOTICE = "MX-CARD Agent is a trademark of addymistrel. All rights reserved.";

export const NAV_LINKS: NavLink[] = [
  { label: "Home", href: "/" },
  { label: "Features", href: "/#features" },
  { label: "Pricing", href: "/pricing" },
  { label: "Docs", href: "/#tutorial" },
];

export const FOOTER_SECTIONS: FooterSection[] = [
  {
    title: "Product",
    links: [
      { label: "Features", href: "/#features" },
      { label: "Pricing", href: "/pricing" },
      { label: "Screenshots", href: "/#screenshots" },
      { label: "Tutorial", href: "/#tutorial" },
    ],
  },
  {
    title: "Resources",
    links: [
      { label: "Documentation", href: "/docs" },
      { label: "API Reference", href: "/api-reference" },
      { label: "Changelog", href: "/changelog" },
      { label: "Roadmap", href: "/roadmap" },
    ],
  },
  {
    title: "Company",
    links: [
      { label: "About", href: "/about" },
      { label: "Blog", href: "/blog" },
      { label: "Careers", href: "/careers" },
      { label: "Contact", href: "/contact" },
    ],
  },
];

export const SOCIAL_LINKS: SocialLink[] = [
  { name: "GitHub", href: "https://github.com/addymistrel/MX-CARD_Agent", icon: "github" },
  { name: "Twitter", href: "https://twitter.com", icon: "twitter" },
  { name: "Discord", href: "https://discord.gg", icon: "discord" },
];
