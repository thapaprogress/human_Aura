import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authApi } from '@/lib/api';
import type { User, LoginCredentials, RegisterCredentials, AuthState } from '@/types';

interface AuthStore extends AuthState {
  setUser: (user: User | null) => void;
  setAuthenticated: (isAuthenticated: boolean) => void;
  setLoading: (isLoading: boolean) => void;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (credentials: RegisterCredentials) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
  updateUser: (data: Partial<User>) => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      // State
      user: {
        id: 'guest-123',
        email: 'guest@auracamera.app',
        firstName: 'Guest',
        lastName: 'User',
        isActive: true,
        emailVerified: true,
        subscriptionTier: 'free',
        subscriptionStatus: 'active',
        dailySessionsUsed: 0,
        createdAt: new Date(),
        updatedAt: new Date(),
      } as User,
      isAuthenticated: true,
      isLoading: false,

      // Actions
      setUser: (user) => set({ user }),

      setAuthenticated: (isAuthenticated) => set({ isAuthenticated }),

      setLoading: (isLoading) => set({ isLoading }),

      login: async (credentials) => {
        set({ isLoading: true });
        try {
          const response = await authApi.login(credentials.email, credentials.password);

          // Store tokens
          localStorage.setItem('token', response.token);
          localStorage.setItem('refreshToken', response.refreshToken);

          set({
            user: response.user,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      register: async (credentials) => {
        set({ isLoading: true });
        try {
          const response = await authApi.register(credentials);

          // Store tokens
          localStorage.setItem('token', response.token);
          localStorage.setItem('refreshToken', response.refreshToken);

          set({
            user: response.user,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      logout: async () => {
        try {
          await authApi.logout();
        } finally {
          // Clear tokens
          localStorage.removeItem('token');
          localStorage.removeItem('refreshToken');

          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
          });
        }
      },

      checkAuth: async () => {
        // Auto-login as guest if no token or error
        const guestUser = {
          id: 'guest-123',
          email: 'guest@auracamera.app',
          firstName: 'Guest',
          lastName: 'User',
          isActive: true,
          emailVerified: true,
          subscriptionTier: 'free',
          subscriptionStatus: 'active',
          dailySessionsUsed: 0,
          createdAt: new Date(),
          updatedAt: new Date(),
        } as User;

        const token = localStorage.getItem('token');

        if (!token) {
          set({
            user: guestUser,
            isAuthenticated: true,
            isLoading: false
          });
          return;
        }

        try {
          const user = await authApi.me();
          set({
            user,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch {
          // Token is invalid, remove it but fallback to guest
          localStorage.removeItem('token');
          localStorage.removeItem('refreshToken');
          set({
            user: guestUser,
            isAuthenticated: true,
            isLoading: false,
          });
        }
      },

      updateUser: (data) => {
        const { user } = get();
        if (user) {
          set({ user: { ...user, ...data } });
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
