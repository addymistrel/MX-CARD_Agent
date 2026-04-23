export interface NavLink {
  label: string;
  href: string;
}

export interface Feature {
  icon: string;
  title: string;
  description: string;
}

export interface Testimonial {
  name: string;
  role: string;
  avatar: string;
  content: string;
  rating: number;
}

export interface PricingPlan {
  id: string;
  name: string;
  description: string;
  price: string;
  period: string;
  features: string[];
  cta: string;
  highlighted: boolean;
  badge?: string;
}

export interface FooterSection {
  title: string;
  links: { label: string; href: string }[];
}

export interface SocialLink {
  name: string;
  href: string;
  icon: string;
}

export interface Screenshot {
  src: string;
  alt: string;
  caption: string;
}
