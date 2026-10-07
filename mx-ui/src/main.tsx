import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { ClerkProvider } from "@clerk/react";
import { getEnvironmentVariable } from "./helpers/envHelper.ts";
import { CLERK_PUBLISHABLE_KEY } from "./constants/envCodes.ts";

const clerkPublishableKey = getEnvironmentVariable(CLERK_PUBLISHABLE_KEY);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ClerkProvider publishableKey={clerkPublishableKey ?? ""}>
      <App />
    </ClerkProvider>
  </StrictMode>,
);
