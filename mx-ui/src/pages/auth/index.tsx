import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { SignIn, SignUp, useUser } from "@clerk/react";
import { useState } from "react";
import { cn } from "@/lib/utils";

type AuthMode = "login" | "signup";

const AUTH_CALLBACK_STORAGE_KEY = "mx-card-pending-auth-callback";

export function AuthPage() {
  const [mode, setMode] = useState<AuthMode>("login");
  const navigate = useNavigate();
  const { isSignedIn, user } = useUser();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const callbackUrl = params.get("callback");

    if (callbackUrl) {
      sessionStorage.setItem(AUTH_CALLBACK_STORAGE_KEY, callbackUrl);
    }

    if (isSignedIn && !callbackUrl) {
      navigate("/");
    }
  }, [isSignedIn, navigate]);

  useEffect(() => {
    if (!isSignedIn || !user) return;

    const params = new URLSearchParams(window.location.search);
    const callbackUrl =
      params.get("callback") ??
      sessionStorage.getItem(AUTH_CALLBACK_STORAGE_KEY);
    if (!callbackUrl) return;

    const email =
      user.primaryEmailAddress?.emailAddress ??
      user.emailAddresses[0]?.emailAddress ??
      "unknown@user";

    const url = new URL(callbackUrl);
    url.searchParams.set("status", "success");
    url.searchParams.set("email", email);

    fetch(url.toString(), { method: "GET" })
      .catch(() => undefined)
      .finally(() => {
        sessionStorage.removeItem(AUTH_CALLBACK_STORAGE_KEY);
        window.setTimeout(() => window.close(), 800);
      });
  }, [isSignedIn, user]);

  return (
    <section className="flex min-h-[calc(100vh-4rem)] items-center justify-center py-12 px-4">
      <div className="w-full max-w-md">
        {/* Mode toggle */}
        <div className="flex rounded-lg bg-muted p-1 mb-6">
          {(["login", "signup"] as const).map((m) => (
            <button
              key={m}
              onClick={() => setMode(m)}
              className={cn(
                "flex-1 rounded-md px-3 py-2 text-sm font-medium transition-colors cursor-pointer",
                mode === m
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground",
              )}
            >
              {m === "login" ? "Sign In" : "Sign Up"}
            </button>
          ))}
        </div>

        {/* Clerk embedded components */}
        <div className="flex justify-center">
          {mode === "login" ? (
            <SignIn
              routing="hash"
              signUpUrl="/auth#signup"
              fallbackRedirectUrl="/"
            />
          ) : (
            <SignUp
              routing="hash"
              signInUrl="/auth#login"
              fallbackRedirectUrl="/"
            />
          )}
        </div>
      </div>
    </section>
  );
}
