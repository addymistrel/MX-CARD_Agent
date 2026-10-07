import axios from "axios";
import { AUTH_ROUTES, AUTH_STORAGE_KEYS } from "@/constants/api";
import { PRIMARY_SERVER_BASE_URL } from "@/helpers/envHelper";
import { getPrimaryServerRoute } from "@/helpers/apiRoutesHelper";

const apiClient = axios.create({
  baseURL: PRIMARY_SERVER_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem(AUTH_STORAGE_KEYS.ACCESS_TOKEN);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refreshToken = localStorage.getItem(
        AUTH_STORAGE_KEYS.REFRESH_TOKEN,
      );
      if (refreshToken) {
        try {
          const { data } = await axios.post(
            getPrimaryServerRoute([AUTH_ROUTES.REFRESH]),
            {
              refreshToken,
            },
          );
          localStorage.setItem(
            AUTH_STORAGE_KEYS.ACCESS_TOKEN,
            data.accessToken,
          );
          localStorage.setItem(
            AUTH_STORAGE_KEYS.REFRESH_TOKEN,
            data.refreshToken,
          );
          original.headers.Authorization = `Bearer ${data.accessToken}`;
          return apiClient(original);
        } catch {
          localStorage.removeItem(AUTH_STORAGE_KEYS.ACCESS_TOKEN);
          localStorage.removeItem(AUTH_STORAGE_KEYS.REFRESH_TOKEN);
          localStorage.removeItem(AUTH_STORAGE_KEYS.USER);
          window.location.href = "/auth";
        }
      }
    }
    return Promise.reject(error);
  },
);

export default apiClient;
