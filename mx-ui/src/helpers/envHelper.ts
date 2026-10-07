import { API_BASE_URL } from "@/constants/envCodes";

const getEnvironmentVariable = (key: string): string | null => {
  const value = import.meta.env[key];
  if (!value) {
    return null;
  }
  return value;
};

const getRequiredEnvironmentVariable = (key: string): string => {
  const value = getEnvironmentVariable(key);
  if (!value) {
    throw new Error(
      `Missing required environment variable: ${key}. Add it to your .env file before running the app.`,
    );
  }
  return value;
};

const PRIMARY_SERVER_BASE_URL =
  getEnvironmentVariable(API_BASE_URL) ?? window.location.origin;

export {
  getEnvironmentVariable,
  getRequiredEnvironmentVariable,
  PRIMARY_SERVER_BASE_URL,
};
