import { useAuth as useClerkAuth, useUser, useClerk } from "@clerk/react";

export function useAuth() {
  const { isSignedIn, isLoaded } = useClerkAuth();
  const { user } = useUser();
  const { signOut } = useClerk();

  const logout = () => signOut();

  return {
    isAuthenticated: !!isSignedIn,
    isLoading: !isLoaded,
    user: user
      ? {
          id: user.id,
          name: user.fullName ?? user.username ?? "User",
          email:
            user.primaryEmailAddress?.emailAddress ??
            user.emailAddresses[0]?.emailAddress ??
            "",
        }
      : null,
    logout,
    error: null as string | null,
    resetError: () => {},
  };
}

