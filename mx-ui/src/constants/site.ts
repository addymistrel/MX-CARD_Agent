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
      { label: "Documentation", href: "#" },
      { label: "API Reference", href: "#" },
      { label: "Changelog", href: "#" },
      { label: "Roadmap", href: "#" },
    ],
  },
  {
    title: "Company",
    links: [
      { label: "About", href: "#" },
      { label: "Blog", href: "#" },
      { label: "Careers", href: "#" },
      { label: "Contact", href: "#" },
    ],
  },
];

export const SOCIAL_LINKS: SocialLink[] = [
  { name: "GitHub", href: "https://github.com/addymistrel/MX-CARD_Agent", icon: "github" },
  { name: "Twitter", href: "#", icon: "twitter" },
  { name: "Discord", href: "#", icon: "discord" },
];
