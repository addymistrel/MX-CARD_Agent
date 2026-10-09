import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import { useUser } from "@clerk/react";
import { Provider } from "react-redux";
import { store } from "@/store";
import { Navbar } from "@/components/shared/Navbar";
import { Footer } from "@/components/shared/Footer";
import { HomePage } from "@/pages/home";
import { DocsPage } from "@/pages/docs";
import { ContactPage } from "@/pages/contact";
import { AuthPage } from "@/pages/auth";
import { AuthSuccessPage } from "@/pages/auth/success";
import { ProtectedRoute } from "@/components/shared/ProtectedRoute";
import { useEffect } from "react";

const AUTH_CALLBACK_STORAGE_KEY = "mx-card-pending-auth-callback";

function AuthCallbackBridge() {
  const { isSignedIn, user } = useUser();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isSignedIn || !user) return;

    const callbackUrl = sessionStorage.getItem(AUTH_CALLBACK_STORAGE_KEY);
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
        navigate("/auth/success");
      });
  }, [isSignedIn, user, navigate]);

  return null;
}

export default function App() {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <AuthCallbackBridge />
        <div className="flex min-h-screen flex-col bg-background text-foreground">
          <Navbar />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/docs" element={<DocsPage />} />
              <Route path="/contact" element={<ContactPage />} />
              <Route path="/auth" element={<AuthPage />} />
              <Route path="/auth/success" element={<AuthSuccessPage />} />
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center">
                      <p className="text-muted-foreground">
                        Dashboard is coming soon.
                      </p>
                    </div>
                  </ProtectedRoute>
                }
              />
            </Routes>
          </main>
          <Footer />
        </div>
      </BrowserRouter>
    </Provider>
  );
}
