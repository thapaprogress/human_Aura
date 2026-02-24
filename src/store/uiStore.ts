import { create } from 'zustand';
import type { Toast, UIState } from '@/types';
import { generateId } from '@/lib/utils';

interface UIStore extends UIState {
  // Actions
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
  toggleSidebar: () => void;
  setSidebarOpen: (isOpen: boolean) => void;
  addToast: (toast: Omit<Toast, 'id'>) => void;
  removeToast: (id: string) => void;
  clearToasts: () => void;
}

export const useUIStore = create<UIStore>((set, get) => ({
  // State
  theme: 'system',
  isSidebarOpen: false,
  toasts: [],

  // Actions
  setTheme: (theme) => set({ theme }),

  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),

  setSidebarOpen: (isOpen) => set({ isSidebarOpen: isOpen }),

  addToast: (toast) => {
    const id = generateId();
    const newToast: Toast = {
      ...toast,
      id,
      duration: toast.duration || 5000,
    };

    set((state) => ({
      toasts: [...state.toasts, newToast],
    }));

    // Auto-remove toast after duration
    if ((newToast.duration || 0) > 0) {
      setTimeout(() => {
        get().removeToast(id);
      }, newToast.duration);
    }
  },

  removeToast: (id) => {
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    }));
  },

  clearToasts: () => set({ toasts: [] }),
}));

// Helper functions for common toast types
export const toast = {
  success: (title: string, message?: string, duration?: number) => {
    useUIStore.getState().addToast({
      type: 'success',
      title,
      message,
      duration,
    });
  },

  error: (title: string, message?: string, duration?: number) => {
    useUIStore.getState().addToast({
      type: 'error',
      title,
      message,
      duration: duration || 8000,
    });
  },

  warning: (title: string, message?: string, duration?: number) => {
    useUIStore.getState().addToast({
      type: 'warning',
      title,
      message,
      duration,
    });
  },

  info: (title: string, message?: string, duration?: number) => {
    useUIStore.getState().addToast({
      type: 'info',
      title,
      message,
      duration,
    });
  },
};
