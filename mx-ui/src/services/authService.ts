import apiClient from "@/lib/apiClient";
import { AUTH_ROUTES, AUTH_STORAGE_KEYS } from "@/constants/api";
import type {
  AuthResponse,
  AuthTokens,
  LoginPayload,
  RegisterPayload,
  AuthUser,
} from "@/types/auth";

export const authService = {
  async register(payload: RegisterPayload): Promise<AuthResponse> {
    const { data } = await apiClient.post<AuthResponse>(
      AUTH_ROUTES.REGISTER,
      payload,
    );
    persistSession(data);
    return data;
  },

  async login(payload: LoginPayload): Promise<AuthResponse> {
    const { data } = await apiClient.post<AuthResponse>(
      AUTH_ROUTES.LOGIN,
      payload,
    );
    persistSession(data);
    return data;
  },

  async refreshTokens(refreshToken: string): Promise<AuthTokens> {
    const { data } = await apiClient.post<AuthTokens>(AUTH_ROUTES.REFRESH, {
      refreshToken,
    });
    localStorage.setItem(AUTH_STORAGE_KEYS.ACCESS_TOKEN, data.accessToken);
    localStorage.setItem(AUTH_STORAGE_KEYS.REFRESH_TOKEN, data.refreshToken);
    return data;
  },

  async getMe(): Promise<AuthUser> {
    const { data } = await apiClient.get<AuthUser>(AUTH_ROUTES.ME);
    return data;
  },

  logout(): void {
    localStorage.removeItem(AUTH_STORAGE_KEYS.ACCESS_TOKEN);
    localStorage.removeItem(AUTH_STORAGE_KEYS.REFRESH_TOKEN);
    localStorage.removeItem(AUTH_STORAGE_KEYS.USER);
  },

  getStoredUser(): AuthUser | null {
    const raw = localStorage.getItem(AUTH_STORAGE_KEYS.USER);
    if (!raw) return null;
    try {
      return JSON.parse(raw) as AuthUser;
    } catch {
      return null;
    }
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem(AUTH_STORAGE_KEYS.ACCESS_TOKEN);
  },
};

function persistSession(data: AuthResponse): void {
  localStorage.setItem(AUTH_STORAGE_KEYS.ACCESS_TOKEN, data.tokens.accessToken);
  localStorage.setItem(
    AUTH_STORAGE_KEYS.REFRESH_TOKEN,
    data.tokens.refreshToken,
  );
  localStorage.setItem(AUTH_STORAGE_KEYS.USER, JSON.stringify(data.user));
}
