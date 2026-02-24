'use client';

import { useRef, useState, useCallback, useEffect } from 'react';
import type { BiofeedbackReading, BiofeedbackSession, TouchPattern } from '@/types';

interface UseBiofeedbackOptions {
  sampleRate?: number; // samples per second
  minDuration?: number; // milliseconds
  onComplete?: (data: BiofeedbackSession) => void;
}

interface UseBiofeedbackReturn {
  isCollecting: boolean;
  readings: BiofeedbackReading[];
  progress: number;
  stability: number;
  startCollection: () => void;
  stopCollection: () => void;
  updateTouchPosition: (x: number, y: number) => void;
}

export function useBiofeedback(options: UseBiofeedbackOptions = {}): UseBiofeedbackReturn {
  const {
    sampleRate = 30,
    minDuration = 5000,
    onComplete,
  } = options;

  const [isCollecting, setIsCollecting] = useState(false);
  const [readings, setReadings] = useState<BiofeedbackReading[]>([]);
  const [progress, setProgress] = useState(0);
  const [stability, setStability] = useState(0);

  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef<number>(0);
  const touchPositionRef = useRef({ x: 0.5, y: 0.5 });
  const previousPositionsRef = useRef<{ x: number; y: number }[]>([]);

  // Create a unique biological signature for each session to ensure variety
  const sessionSignatureRef = useRef({
    stabilityBias: 0.5,
    calmnessBias: 0.5,
    stressBias: 0.5,
    noiseProfile: 0.1
  });

  const updateTouchPosition = useCallback((x: number, y: number) => {
    touchPositionRef.current = { x, y };
    previousPositionsRef.current.push({ x, y });

    if (previousPositionsRef.current.length > 30) {
      previousPositionsRef.current.shift();
    }
  }, []);

  const calculateStability = useCallback((): number => {
    const positions = previousPositionsRef.current;

    // Base stability from signature + movement variance
    const baseStability = sessionSignatureRef.current.stabilityBias;

    if (positions.length < 2) return baseStability;

    const avgX = positions.reduce((sum, p) => sum + p.x, 0) / positions.length;
    const avgY = positions.reduce((sum, p) => sum + p.y, 0) / positions.length;

    const varianceX = positions.reduce((sum, p) => sum + Math.pow(p.x - avgX, 2), 0) / positions.length;
    const varianceY = positions.reduce((sum, p) => sum + Math.pow(p.y - avgY, 2), 0) / positions.length;

    const totalVariance = varianceX + varianceY;

    // Higher variance reduces stability from the base bias
    return Math.max(0.1, Math.min(0.95, baseStability - totalVariance * 5));
  }, []);

  const collectReading = useCallback((): BiofeedbackReading => {
    const currentStability = calculateStability();
    const sig = sessionSignatureRef.current;

    // Use signature to create diverse energy states
    const pressure = 0.3 + currentStability * 0.7;
    const calmnessScore = Math.max(0.1, Math.min(0.9, sig.calmnessBias + (Math.random() - 0.5) * sig.noiseProfile));
    const stressIndicator = Math.max(0.1, Math.min(0.9, sig.stressBias + (Math.random() - 0.5) * sig.noiseProfile));

    const simulatedGsr = 0.2 + pressure * 0.6 + Math.random() * 0.2;
    const simulatedHrv = 0.3 + currentStability * 0.5 + Math.random() * 0.2;

    return {
      id: Math.random().toString(36).substring(7),
      sessionId: 'current',
      timestamp: new Date(),
      touchX: touchPositionRef.current.x,
      touchY: touchPositionRef.current.y,
      pressure,
      stability: currentStability,
      simulatedGsr,
      simulatedHrv,
      stressIndicator,
      calmnessScore,
    };
  }, [calculateStability]);

  const determineTouchPattern = (readings: BiofeedbackReading[]): TouchPattern => {
    const sig = sessionSignatureRef.current;
    if (sig.stabilityBias > 0.8) return 'steady';
    if (sig.stabilityBias < 0.4) return 'erratic';
    return 'focused';
  };

  const processSession = (readings: BiofeedbackReading[], startTime: number): BiofeedbackSession => {
    const endTime = Date.now();
    const durationMs = endTime - startTime;

    const stabilities = readings.map((r) => r.stability || 0);
    const averageStability = stabilities.reduce((a, b) => a + b, 0) / stabilities.length;

    const calmnesses = readings.map((r) => r.calmnessScore || 0);
    const averageCalmness = calmnesses.reduce((a, b) => a + b, 0) / calmnesses.length;

    const stresses = readings.map((r) => r.stressIndicator || 0);
    const averageStress = stresses.reduce((a, b) => a + b, 0) / stresses.length;

    return {
      sessionId: Math.random().toString(36).substring(2, 11),
      userId: undefined,
      startTime: new Date(startTime),
      endTime: new Date(endTime),
      durationMs,
      readings,
      averageStability,
      stabilityVariance: 0.05,
      touchPattern: determineTouchPattern(readings),
      simulatedGsr: 0.5,
      simulatedHrv: 0.5,
      stressIndicator: averageStress,
      calmnessScore: averageCalmness,
    };
  };

  const readingsRef = useRef<BiofeedbackReading[]>([]);

  const startCollection = useCallback(() => {
    // Randomize biological signature for this specific session
    sessionSignatureRef.current = {
      stabilityBias: Math.random() * 0.7 + 0.2, // 0.2 to 0.9
      calmnessBias: Math.random() * 0.8 + 0.1,  // 0.1 to 0.9
      stressBias: Math.random() * 0.8 + 0.1,    // 0.1 to 0.9
      noiseProfile: Math.random() * 0.2 + 0.05
    };

    setIsCollecting(true);
    setReadings([]);
    readingsRef.current = [];
    setProgress(0);
    startTimeRef.current = Date.now();
    previousPositionsRef.current = [];

    const intervalMs = 1000 / sampleRate;

    intervalRef.current = setInterval(() => {
      const reading = collectReading();
      readingsRef.current.push(reading);
      setReadings([...readingsRef.current]);
      setStability(reading.stability || 0);

      // Update progress
      const elapsed = Date.now() - startTimeRef.current;
      const newProgress = Math.min(100, (elapsed / minDuration) * 100);
      setProgress(newProgress);
    }, intervalMs);

    // Auto-stop after minDuration
    setTimeout(() => {
      stopSession();
    }, minDuration);
  }, [sampleRate, minDuration, collectReading]);

  const stopSession = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    setIsCollecting(false);
    setProgress(100);

    // Process and return session data using the ref to get all readings
    const session = processSession(readingsRef.current, startTimeRef.current);
    onComplete?.(session);
  }, [onComplete]);

  const stopCollection = useCallback(() => {
    stopSession();
  }, [stopSession]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  return {
    isCollecting,
    readings,
    progress,
    stability,
    startCollection,
    stopCollection,
    updateTouchPosition,
  };
}

// Helper function to generate session ID
function generateId(): string {
  return Math.random().toString(36).substring(2, 15);
}
