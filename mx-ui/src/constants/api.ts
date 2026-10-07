export const AUTH_STORAGE_KEYS = {
  ACCESS_TOKEN: "mx_access_token",
  REFRESH_TOKEN: "mx_refresh_token",
  USER: "mx_user",
} as const;

export const AUTH_ROUTES = {
  REGISTER: "/auth/register",
  LOGIN: "/auth/login",
  REFRESH: "/auth/refresh",
  ME: "/auth/me",
} as const;
