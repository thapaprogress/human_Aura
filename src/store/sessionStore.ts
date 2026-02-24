import { create } from 'zustand';
import { sessionsApi } from '@/lib/api';
import type {
  Session,
  SessionMode,
  AuraStyle,
  AuraWithReading,
  BiofeedbackSession,
  FaceDetectionResult,
} from '@/types';

interface SessionState {
  // State
  currentSession: Session | null;
  sessions: Session[];
  isCreating: boolean;
  isCapturing: boolean;
  isProcessing: boolean;
  faceData: FaceDetectionResult | null;
  biofeedbackData: BiofeedbackSession | null;
  generatedAura: AuraWithReading | null;
  error: string | null;

  // Actions
  createSession: (mode?: SessionMode) => Promise<Session>;
  capturePhoto: (sessionId: string, imageData: string) => Promise<void>;
  submitBiofeedback: (sessionId: string, data: BiofeedbackSession) => Promise<void>;
  generateAura: (sessionId: string, style?: AuraStyle) => Promise<AuraWithReading>;
  fetchSessions: (params?: { limit?: number; offset?: number }) => Promise<void>;
  fetchSession: (id: string) => Promise<Session>;
  resetSession: () => void;
  setError: (error: string | null) => void;
}

export const useSessionStore = create<SessionState>((set, get) => ({
  // State
  currentSession: null,
  sessions: [],
  isCreating: false,
  isCapturing: false,
  isProcessing: false,
  faceData: null,
  biofeedbackData: null,
  generatedAura: null,
  error: null,

  // Actions
  createSession: async (mode = 'selfie') => {
    set({ isCreating: true, error: null });
    try {
      const session = await sessionsApi.create(mode);
      set({ currentSession: session, isCreating: false });
      return session;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to create session';
      set({ error: message, isCreating: false });
      throw error;
    }
  },

  capturePhoto: async (sessionId: string, imageData: string) => {
    set({ isCapturing: true, error: null });
    try {
      const response = await sessionsApi.capture(sessionId, imageData);
      set({
        currentSession: response.session,
        faceData: response.faceDetection,
        isCapturing: false,
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to capture photo';
      set({ error: message, isCapturing: false });
      throw error;
    }
  },

  submitBiofeedback: async (sessionId: string, data: BiofeedbackSession) => {
    set({ isProcessing: true, error: null });
    try {
      const response = await sessionsApi.submitBiofeedback(sessionId, {
        readings: data.readings,
        durationMs: data.durationMs,
      });
      set({
        currentSession: response.session,
        biofeedbackData: response.biofeedback,
        isProcessing: false,
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to process biofeedback';
      set({ error: message, isProcessing: false });
      throw error;
    }
  },

  generateAura: async (sessionId: string, style = 'soft') => {
    set({ isProcessing: true, error: null });
    try {
      const response = await sessionsApi.generateAura(sessionId, style);
      set({
        currentSession: response.session,
        generatedAura: response.aura,
        isProcessing: false,
      });
      return response.aura;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to generate aura';
      set({ error: message, isProcessing: false });
      throw error;
    }
  },

  fetchSessions: async (params) => {
    try {
      const response = await sessionsApi.list(params);
      set({ sessions: response.data });
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to fetch sessions';
      set({ error: message });
    }
  },

  fetchSession: async (id: string) => {
    try {
      const session = await sessionsApi.get(id);
      set({ currentSession: session });
      return session;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to fetch session';
      set({ error: message });
      throw error;
    }
  },

  resetSession: () => {
    set({
      currentSession: null,
      faceData: null,
      biofeedbackData: null,
      generatedAura: null,
      error: null,
    });
  },

  setError: (error) => set({ error }),
}));
