# MX-CARD Agent - Web UI

The official web interface for [MX-CARD Agent](https://github.com/addymistrel/MX-CARD_Agent), an autonomous AI coding agent.

Built with **React 19**, **Vite**, **Tailwind CSS v4**, and **shadcn/ui**-style components.

---

## Features

- **Home Page** - Hero section, feature grid, screenshots, tutorial video, testimonials
- **Pricing Page** - Three-tier pricing cards loaded from JSON data
- **Auth Page** - Login / Signup toggle with form validation (dummy, no backend)
- **Light & Dark Theme** - Toggle with system preference detection and localStorage persistence
- **Mobile-First Responsive** - Hamburger menu, adaptive layouts across all breakpoints
- **Clean Architecture** - No hardcoded content; all data in `/data` and `/constants`

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| [React 19](https://react.dev) | UI framework |
| [Vite 8](https://vite.dev) | Build tool & dev server |
| [Tailwind CSS v4](https://tailwindcss.com) | Utility-first styling |
| [React Router v7](https://reactrouter.com) | Client-side routing |
| [Lucide React](https://lucide.dev) | Icon library |
| [clsx](https://github.com/lukeed/clsx) + [tailwind-merge](https://github.com/dcastil/tailwind-merge) | Class name utilities |

---

## Project Structure

```
src/
+-- components/
|   +-- ui/            # Button, Card, Input, Badge (shadcn-style)
|   +-- shared/        # Navbar, Footer, SectionHeading
|   +-- sections/      # Hero, Features, Screenshots, Tutorial, Testimonials
+-- pages/             # HomePage, PricingPage, AuthPage
+-- data/              # features.json, testimonials.json, pricing.json, screenshots.json
+-- constants/         # site.ts (nav, footer, social links, branding)
+-- types/             # TypeScript interfaces
+-- hooks/             # useTheme (dark mode)
+-- helpers/           # Icon mapping utility
+-- lib/               # cn() class merge utility
+-- App.tsx            # Router layout with Navbar + Footer
+-- main.tsx           # Entry point
+-- index.css          # Tailwind v4 theme (light + dark)
```

---

## Getting Started

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

---

## Architecture Rules

- **No hardcoding** inside components - all static content lives in `/constants` or `/data`
- **Reusable UI** - small, composable components in `/components/ui`
- **Separation of concerns** - data, logic, and presentation are decoupled
- **Type-safe** - all data structures defined in `/types`

---

## License

Part of the [MX-CARD Agent](https://github.com/addymistrel/MX-CARD_Agent) project by [@addymistrel](https://github.com/addymistrel).

