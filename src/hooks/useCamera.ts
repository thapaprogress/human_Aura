'use client';

import { useRef, useState, useCallback, useEffect } from 'react';

interface UseCameraOptions {
  width?: number;
  height?: number;
  facingMode?: 'user' | 'environment';
  onError?: (error: Error) => void;
}

interface UseCameraReturn {
  videoRef: React.RefObject<HTMLVideoElement>;
  stream: MediaStream | null;
  isReady: boolean;
  isLoading: boolean;
  error: Error | null;
  start: () => Promise<void>;
  stop: () => void;
  switchCamera: () => Promise<void>;
  takePhoto: () => string | null;
}

export function useCamera(options: UseCameraOptions = {}): UseCameraReturn {
  const {
    width = 1280,
    height = 720,
    facingMode = 'user',
    onError,
  } = options;

  const videoRef = useRef<HTMLVideoElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [isReady, setIsReady] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [currentFacingMode, setCurrentFacingMode] = useState(facingMode);

  const start = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    setIsReady(false);

    try {
      // First attempt with ideal constraints
      const constraints: MediaStreamConstraints = {
        video: {
          width: { ideal: width },
          height: { ideal: height },
          facingMode: { ideal: currentFacingMode },
        },
        audio: false,
      };

      let mediaStream: MediaStream;
      try {
        mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      } catch (firstErr) {
        console.warn("First camera attempt failed, trying fallback...", firstErr);
        // Fallback: simple video constraint
        mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      }
      setStream(mediaStream);

      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        // Try playing immediately
        try {
          await videoRef.current.play();
          setIsReady(true);
          setIsLoading(false);
        } catch (playErr) {
          console.error("Video play error:", playErr);
          // Fallback to metadata listener if play fail (e.g. user interaction required)
          videoRef.current.onloadedmetadata = () => {
            setIsReady(true);
            setIsLoading(false);
          };
        }
      } else {
        // If ref is not available yet, we have the stream anyway
        setIsReady(true);
        setIsLoading(false);
      }
    } catch (err) {
      console.error("Camera start error:", err);
      const error = err instanceof Error ? err : new Error('Failed to access camera');
      setError(error);
      setIsLoading(false);
      setIsReady(false);
      onError?.(error);
    }
  }, [width, height, currentFacingMode, onError]);

  const stop = useCallback(() => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      setStream(null);
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsReady(false);
  }, [stream]);

  const switchCamera = useCallback(async () => {
    stop();
    setCurrentFacingMode((prev) => (prev === 'user' ? 'environment' : 'user'));
    await start();
  }, [stop, start]);

  const takePhoto = useCallback((): string | null => {
    if (!videoRef.current || !isReady) return null;

    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;

    const ctx = canvas.getContext('2d');
    if (!ctx) return null;

    // Flip horizontally if using front camera
    if (currentFacingMode === 'user') {
      ctx.translate(canvas.width, 0);
      ctx.scale(-1, 1);
    }

    ctx.drawImage(videoRef.current, 0, 0);

    return canvas.toDataURL('image/jpeg', 0.95);
  }, [isReady, currentFacingMode]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stop();
    };
  }, [stop]);

  return {
    videoRef,
    stream,
    isReady,
    isLoading,
    error,
    start,
    stop,
    switchCamera,
    takePhoto,
  };
}
