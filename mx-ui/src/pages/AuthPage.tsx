import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardHeader,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { SITE_NAME } from "@/constants/site";
import { cn } from "@/lib/utils";

type AuthMode = "login" | "signup";

export function AuthPage() {
  const [mode, setMode] = useState<AuthMode>("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert(
      mode === "login"
        ? `Logging in with ${email}`
        : `Signing up ${name} with ${email}`
    );
  };

  return (
    <section className="flex min-h-[calc(100vh-4rem)] items-center justify-center py-12 px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="mx-auto mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-primary text-primary-foreground font-bold text-lg">
            MX
          </div>
          <h1 className="text-2xl font-bold">{mode === "login" ? "Welcome back" : `Join ${SITE_NAME}`}</h1>
          <p className="text-sm text-muted-foreground mt-1">
            {mode === "login"
              ? "Sign in to your account to continue"
              : "Create an account to get started"}
          </p>
        </div>

        <Card>
          {/* Toggle tabs */}
          <CardHeader className="pb-4">
            <div className="flex rounded-lg bg-muted p-1">
              {(["login", "signup"] as const).map((m) => (
                <button
                  key={m}
                  onClick={() => setMode(m)}
                  className={cn(
                    "flex-1 rounded-md px-3 py-2 text-sm font-medium transition-colors cursor-pointer",
                    mode === m
                      ? "bg-background text-foreground shadow-sm"
                      : "text-muted-foreground hover:text-foreground"
                  )}
                >
                  {m === "login" ? "Sign In" : "Sign Up"}
                </button>
              ))}
            </div>
          </CardHeader>

          <form onSubmit={handleSubmit}>
            <CardContent className="space-y-4">
              {mode === "signup" && (
                <div className="space-y-2">
                  <label htmlFor="name" className="text-sm font-medium">
                    Full Name
                  </label>
                  <Input
                    id="name"
                    type="text"
                    placeholder="John Doe"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                  />
                </div>
              )}

              <div className="space-y-2">
                <label htmlFor="email" className="text-sm font-medium">
                  Email
                </label>
                <Input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="password" className="text-sm font-medium">
                  Password
                </label>
                <Input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  minLength={6}
                />
              </div>

              {mode === "login" && (
                <div className="flex items-center justify-end">
                  <button type="button" className="text-sm text-primary hover:underline cursor-pointer bg-transparent border-none">
                    Forgot password?
                  </button>
                </div>
              )}
            </CardContent>

            <CardFooter className="flex-col gap-4">
              <Button type="submit" className="w-full">
                {mode === "login" ? "Sign In" : "Create Account"}
              </Button>

              <p className="text-xs text-center text-muted-foreground">
                {mode === "login" ? (
                  <>
                    Don't have an account?{" "}
                    <button type="button" onClick={() => setMode("signup")} className="text-primary hover:underline cursor-pointer bg-transparent border-none text-xs">
                      Sign up
                    </button>
                  </>
                ) : (
                  <>
                    Already have an account?{" "}
                    <button type="button" onClick={() => setMode("login")} className="text-primary hover:underline cursor-pointer bg-transparent border-none text-xs">
                      Sign in
                    </button>
                  </>
                )}
              </p>
            </CardFooter>
          </form>
        </Card>
      </div>
    </section>
  );
}
