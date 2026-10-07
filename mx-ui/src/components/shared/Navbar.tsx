import { Link, useLocation } from "react-router-dom";
import { Menu, X, Moon, Sun } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { NAV_LINKS, SITE_NAME } from "@/constants/site";
import { useTheme } from "@/hooks/useTheme";
import { FeatureLink } from "@/components/shared/FeatureLink";
import { cn } from "@/lib/utils";
import {
  Show,
  SignInButton,
  SignUpButton,
  UserButton,
} from "@clerk/react";

export function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const { theme, toggleTheme } = useTheme();
  const location = useLocation();

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link
          to="/"
          className="flex items-center gap-2 font-bold text-xl tracking-tight text-foreground no-underline"
        >
          <span className="inline-flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground text-sm font-bold">
            MX
          </span>
          {SITE_NAME}
        </Link>

        <nav className="hidden md:flex items-center gap-4">
          {NAV_LINKS.map((link) => (
            <FeatureLink
              key={link.href}
              to={link.href}
              featureKey={link.href}
              className={cn(
                "px-3 py-2 text-sm font-medium rounded-md transition-colors no-underline",
                location.pathname === link.href
                  ? "text-primary bg-primary/10"
                  : "text-muted-foreground hover:text-foreground hover:bg-accent",
              )}
            >
              {link.label}
            </FeatureLink>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleTheme}
            aria-label="Toggle theme"
          >
            {theme === "dark" ? (
              <Sun className="h-5 w-5" />
            ) : (
              <Moon className="h-5 w-5" />
            )}
          </Button>

          {/* Clerk auth controls — desktop */}
          <div className="hidden md:flex items-center gap-2">
            <Show when="signed-out">
              <SignInButton mode="redirect" fallbackRedirectUrl="/">
                <Button variant="ghost" size="sm">
                  Sign In
                </Button>
              </SignInButton>
              <SignUpButton mode="redirect" fallbackRedirectUrl="/">
                <Button size="sm">Sign Up</Button>
              </SignUpButton>
            </Show>
            <Show when="signed-in">
              <UserButton />
            </Show>
          </div>

          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Toggle menu"
          >
            {mobileOpen ? (
              <X className="h-5 w-5" />
            ) : (
              <Menu className="h-5 w-5" />
            )}
          </Button>
        </div>
      </div>

      {mobileOpen && (
        <div className="md:hidden border-t bg-background">
          <nav className="flex flex-col p-4 gap-1">
            {NAV_LINKS.map((link) => (
              <FeatureLink
                key={link.href}
                to={link.href}
                featureKey={link.href}
                onClick={() => setMobileOpen(false)}
                className={cn(
                  "px-3 py-2 text-sm font-medium rounded-md transition-colors no-underline text-left",
                  location.pathname === link.href
                    ? "text-primary bg-primary/10"
                    : "text-muted-foreground hover:text-foreground hover:bg-accent",
                )}
              >
                {link.label}
              </FeatureLink>
            ))}

            {/* Clerk auth controls — mobile */}
            <div className="mt-2 pt-2 border-t flex flex-col gap-2">
              <Show when="signed-out">
                <SignInButton mode="redirect" fallbackRedirectUrl="/">
                  <Button
                    variant="ghost"
                    className="w-full justify-start"
                    onClick={() => setMobileOpen(false)}
                  >
                    Sign In
                  </Button>
                </SignInButton>
                <SignUpButton mode="redirect" fallbackRedirectUrl="/">
                  <Button
                    className="w-full"
                    onClick={() => setMobileOpen(false)}
                  >
                    Sign Up
                  </Button>
                </SignUpButton>
              </Show>
              <Show when="signed-in">
                <div className="flex items-center gap-3 px-3 py-2">
                  <UserButton />
                  <span className="text-sm text-muted-foreground">
                    My Account
                  </span>
                </div>
              </Show>
            </div>
          </nav>
        </div>
      )}
    </header>
  );
}
