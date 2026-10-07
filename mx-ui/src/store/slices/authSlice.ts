import {
  createSlice,
  createAsyncThunk,
  type PayloadAction,
} from "@reduxjs/toolkit";
import { authService } from "@/services/authService";
import type { AuthUser, LoginPayload, RegisterPayload } from "@/types/auth";

interface AuthState {
  user: AuthUser | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: authService.getStoredUser(),
  isLoading: false,
  error: null,
};

export const loginThunk = createAsyncThunk(
  "auth/login",
  async (payload: LoginPayload, { rejectWithValue }) => {
    try {
      const res = await authService.login(payload);
      return res.user;
    } catch (err: unknown) {
      const message = (
        err as { response?: { data?: { message?: string | string[] } } }
      )?.response?.data?.message;
      return rejectWithValue(
        Array.isArray(message) ? message[0] : (message ?? "Login failed"),
      );
    }
  },
);

export const registerThunk = createAsyncThunk(
  "auth/register",
  async (payload: RegisterPayload, { rejectWithValue }) => {
    try {
      const res = await authService.register(payload);
      return res.user;
    } catch (err: unknown) {
      const message = (
        err as { response?: { data?: { message?: string | string[] } } }
      )?.response?.data?.message;
      return rejectWithValue(
        Array.isArray(message)
          ? message[0]
          : (message ?? "Registration failed"),
      );
    }
  },
);

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    logout(state) {
      authService.logout();
      state.user = null;
      state.error = null;
    },
    clearError(state) {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginThunk.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(
        loginThunk.fulfilled,
        (state, action: PayloadAction<AuthUser>) => {
          state.isLoading = false;
          state.user = action.payload;
        },
      )
      .addCase(loginThunk.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      .addCase(registerThunk.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(
        registerThunk.fulfilled,
        (state, action: PayloadAction<AuthUser>) => {
          state.isLoading = false;
          state.user = action.payload;
        },
      )
      .addCase(registerThunk.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { logout, clearError } = authSlice.actions;
export default authSlice.reducer;
