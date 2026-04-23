export const FEATURES = {
  HOME: "/",
  PRICING: "/pricing",
  AUTH: "/auth",
  FEATURES_SECTION: "/#features",
  TUTORIAL_SECTION: "/#tutorial",
  SCREENSHOTS_SECTION: "/#screenshots",
  DOCS: "/docs",
  API_REFERENCE: "/api-reference",
  CHANGELOG: "/changelog",
  ROADMAP: "/roadmap",
  ABOUT: "/about",
  BLOG: "/blog",
  CAREERS: "/careers",
  CONTACT: "/contact",
  SOCIAL_GITHUB: "social:github",
  SOCIAL_TWITTER: "social:twitter",
  SOCIAL_DISCORD: "social:discord",
  AUTH_SUBMIT: "auth:submit",
  AUTH_FORGOT_PASSWORD: "auth:forgot-password",
  PRICING_CTA: "pricing:cta",
} as const;

export type FeatureKey = (typeof FEATURES)[keyof typeof FEATURES];
