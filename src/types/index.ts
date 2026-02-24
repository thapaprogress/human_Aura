// =============================================================================
// BASE TYPES
// =============================================================================

export interface Timestamped {
  createdAt: Date;
  updatedAt?: Date;
}

// =============================================================================
// AUTHENTICATION TYPES
// =============================================================================

export interface User {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  avatarUrl?: string;
  isActive: boolean;
  emailVerified: boolean;
  subscriptionTier: SubscriptionTier;
  subscriptionStatus: SubscriptionStatus;
  dailySessionsUsed: number;
  dailySessionsResetAt?: Date;
  createdAt: Date;
  updatedAt: Date;
}

export type SubscriptionTier = 'free' | 'weekly' | 'monthly' | 'yearly';
export type SubscriptionStatus = 'active' | 'cancelled' | 'expired' | 'paused' | 'inactive';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
}

export interface AuthResponse {
  user: User;
  token: string;
  refreshToken: string;
  expiresIn: number;
}

// =============================================================================
// SESSION TYPES
// =============================================================================

export type SessionStatus = 'started' | 'capturing' | 'processing' | 'completed' | 'failed';
export type SessionMode = 'selfie' | 'friend';

export interface Session {
  id: string;
  userId: string;
  status: SessionStatus;
  startedAt: Date;
  completedAt?: Date;
  faceDetected: boolean;
  alignmentScore?: number;
  biofeedbackDurationMs?: number;
  mode: SessionMode;
  metadata?: Record<string, unknown>;
  createdAt: Date;
}

export interface SessionWithRelations extends Session {
  biofeedbackReadings?: BiofeedbackReading[];
  photos?: Photo[];
  auraProfiles?: AuraProfile[];
  readings?: Reading[];
}

// =============================================================================
// BIOFEEDBACK TYPES
// =============================================================================

export interface BiofeedbackReading {
  id: string;
  sessionId: string;
  timestamp: Date;
  touchX?: number;
  touchY?: number;
  pressure?: number;
  stability?: number;
  simulatedGsr?: number;
  simulatedHrv?: number;
  stressIndicator?: number;
  calmnessScore?: number;
  rawData?: Record<string, unknown>;
}

export interface BiofeedbackSession {
  sessionId: string;
  userId?: string;
  startTime: Date;
  endTime: Date;
  durationMs: number;
  readings: BiofeedbackReading[];
  averageStability: number;
  stabilityVariance: number;
  touchPattern: TouchPattern;
  simulatedGsr: number;
  simulatedHrv: number;
  stressIndicator: number;
  calmnessScore: number;
}

export type TouchPattern = 'steady' | 'erratic' | 'focused' | 'scattered';

// =============================================================================
// PHOTO TYPES
// =============================================================================

export interface Photo {
  id: string;
  sessionId: string;
  userId: string;
  originalUrl: string;
  processedUrl?: string;
  width?: number;
  height?: number;
  format?: string;
  fileSizeBytes?: number;
  isDeleted: boolean;
  createdAt: Date;
}

// =============================================================================
// AURA TYPES
// =============================================================================

export interface AuraPositioning {
  ascendant: string[];    // Right side - receiving
  descendant: string[];   // Left side - giving
  cathedra: string[];     // Bottom - root
  coronation: string[];   // Top - crown
  etherea: string[];      // All sides
}

export interface AuraProfile {
  id: string;
  sessionId: string;
  userId: string;
  majorityColor: string;
  majorityPercentage: number;
  moderateColors: string[];
  moderatePercentages: number[];
  minorityColors: string[];
  minorityPercentages: number[];
  intensity: number;
  brightness: number;
  saturation: number;
  positioning: AuraPositioning;
  profileData?: Record<string, unknown>;
  createdAt: Date;
}

export interface AuraImage {
  id: string;
  auraProfileId: string;
  sessionId: string;
  userId: string;
  imageUrl: string;
  thumbnailUrl?: string;
  width?: number;
  height?: number;
  format?: string;
  style: AuraStyle;
  fileSizeBytes?: number;
  isDeleted: boolean;
  createdAt: Date;
}

export type AuraStyle = 'soft' | 'medium' | 'strong';

export interface AuraWithReading {
  id: string;
  imageUrl: string;
  thumbnailUrl?: string;
  profile: AuraProfile;
  reading: {
    sections: ReadingSection[];
  };
  createdAt: Date;
}

// =============================================================================
// READING TYPES
// =============================================================================

export type ReadingSectionType = 'color_analysis' | 'alignment' | 'guidance';
export type ReadingGenerator = 'ai' | 'template' | 'hybrid';

export interface Reading {
  id: string;
  auraProfileId: string;
  sessionId: string;
  userId: string;
  section: ReadingSectionType;
  title?: string;
  content: string;
  colorReferences: string[];
  generatedBy: ReadingGenerator;
  createdAt: Date;
}

export interface ReadingSection {
  section: ReadingSectionType;
  title: string;
  content: string;
}

// =============================================================================
// COLOR TYPES
// =============================================================================

export interface ColorDefinition {
  name: string;
  hex: string;
  keywords: string[];
  description: string;
  positive: string[];
  challenges: string[];
  chakras: string[];
  elements: string[];
}

export interface ColorMeaning {
  color: string;
  percentage: number;
  position: 'majority' | 'moderate' | 'minority';
  meaning: ColorDefinition;
}

// =============================================================================
// SUBSCRIPTION TYPES
// =============================================================================

export interface Subscription {
  id: string;
  userId: string;
  planType: SubscriptionTier;
  status: SubscriptionStatus;
  startedAt: Date;
  expiresAt?: Date;
  cancelledAt?: Date;
  paymentProvider?: string;
  paymentProviderSubscriptionId?: string;
  priceCents?: number;
  currency: string;
  metadata?: Record<string, unknown>;
  createdAt: Date;
  updatedAt: Date;
}

export interface SubscriptionPlan {
  id: string;
  name: string;
  description: string;
  priceCents: number;
  currency: string;
  interval: 'weekly' | 'monthly' | 'yearly';
  features: string[];
  sessionsPerDay: number;
  stripePriceId?: string;
}

// =============================================================================
// PAYMENT TYPES
// =============================================================================

export type PaymentStatus = 'pending' | 'completed' | 'failed' | 'refunded';

export interface Payment {
  id: string;
  userId: string;
  subscriptionId?: string;
  amountCents: number;
  currency: string;
  status: PaymentStatus;
  paymentProvider?: string;
  paymentProviderChargeId?: string;
  description?: string;
  metadata?: Record<string, unknown>;
  createdAt: Date;
  completedAt?: Date;
}

// =============================================================================
// API RESPONSE TYPES
// =============================================================================

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: ApiError;
  meta?: ResponseMeta;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, string[]>;
}

export interface ResponseMeta {
  total?: number;
  page?: number;
  limit?: number;
  hasMore?: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    total: number;
    limit: number;
    offset: number;
    hasMore: boolean;
  };
}

// =============================================================================
// FACE DETECTION TYPES
// =============================================================================

export interface FaceLandmark {
  x: number;
  y: number;
  z: number;
  visibility?: number;
}

export interface FaceBoundingBox {
  xMin: number;
  yMin: number;
  xMax: number;
  yMax: number;
  width: number;
  height: number;
}

export interface FacePose {
  pitch: number;
  yaw: number;
  roll: number;
}

export interface FaceDetectionResult {
  found: boolean;
  landmarks?: FaceLandmark[];
  boundingBox?: FaceBoundingBox;
  faceCenter?: { x: number; y: number };
  faceSize?: { width: number; height: number };
  headPose?: FacePose;
  alignmentScore?: number;
}

// =============================================================================
// COMPONENT PROP TYPES
// =============================================================================

export interface CameraCaptureProps {
  onCapture: (imageData: string, faceData: FaceDetectionResult) => void;
  mode?: SessionMode;
}

export interface BiofeedbackCollectorProps {
  sessionId: string;
  onComplete: (data: BiofeedbackSession) => void;
  durationMs?: number;
}

export interface AuraDisplayProps {
  aura: AuraWithReading;
  onDownload: () => void;
  onShare: () => void;
}

// =============================================================================
// STORE TYPES
// =============================================================================

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (credentials: RegisterCredentials) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
}

export interface SessionState {
  currentSession: Session | null;
  sessions: Session[];
  isCreating: boolean;
  createSession: (mode?: SessionMode) => Promise<Session>;
  capturePhoto: (sessionId: string, imageData: string) => Promise<void>;
  submitBiofeedback: (sessionId: string, data: BiofeedbackSession) => Promise<void>;
  generateAura: (sessionId: string, style?: AuraStyle) => Promise<AuraWithReading>;
}

export interface UIState {
  theme: 'light' | 'dark' | 'system';
  isSidebarOpen: boolean;
  toasts: Toast[];
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
  toggleSidebar: () => void;
  addToast: (toast: Omit<Toast, 'id'>) => void;
  removeToast: (id: string) => void;
}

export interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message?: string;
  duration?: number;
}
