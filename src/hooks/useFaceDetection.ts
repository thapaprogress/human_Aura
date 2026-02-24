'use client';

import { useRef, useState, useCallback, useEffect } from 'react';
import { FaceMesh, Results } from '@mediapipe/face_mesh';
import { Camera } from '@mediapipe/camera_utils';
import type { FaceDetectionResult, FaceLandmark, FaceBoundingBox } from '@/types';

interface UseFaceDetectionOptions {
  videoRef: React.RefObject<HTMLVideoElement>;
  minDetectionConfidence?: number;
  minTrackingConfidence?: number;
  onFaceDetected?: (result: FaceDetectionResult) => void;
  onFaceLost?: () => void;
}

interface UseFaceDetectionReturn {
  isDetecting: boolean;
  faceData: FaceDetectionResult | null;
  alignmentScore: number;
  startDetection: () => void;
  stopDetection: () => void;
}

export function useFaceDetection(options: UseFaceDetectionOptions): UseFaceDetectionReturn {
  const {
    videoRef,
    minDetectionConfidence = 0.5,
    minTrackingConfidence = 0.5,
    onFaceDetected,
    onFaceLost,
  } = options;

  const faceMeshRef = useRef<FaceMesh | null>(null);
  const cameraRef = useRef<Camera | null>(null);
  const [isDetecting, setIsDetecting] = useState(false);
  const [faceData, setFaceData] = useState<FaceDetectionResult | null>(null);
  const [alignmentScore, setAlignmentScore] = useState(0);

  const processResults = useCallback((results: Results) => {
    if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {
      const landmarks = results.multiFaceLandmarks[0];
      
      // Convert landmarks to our format
      const faceLandmarks: FaceLandmark[] = landmarks.map((lm) => ({
        x: lm.x,
        y: lm.y,
        z: lm.z,
        visibility: lm.visibility,
      }));

      // Calculate bounding box
      const xs = faceLandmarks.map((lm) => lm.x);
      const ys = faceLandmarks.map((lm) => lm.y);
      const xMin = Math.min(...xs);
      const xMax = Math.max(...xs);
      const yMin = Math.min(...ys);
      const yMax = Math.max(...ys);

      const boundingBox: FaceBoundingBox = {
        xMin,
        yMin,
        xMax,
        yMax,
        width: xMax - xMin,
        height: yMax - yMin,
      };

      // Calculate face center
      const faceCenter = {
        x: (xMin + xMax) / 2,
        y: (yMin + yMax) / 2,
      };

      // Calculate face size
      const faceSize = {
        width: boundingBox.width,
        height: boundingBox.height,
      };

      // Calculate alignment score
      const score = calculateAlignmentScore(faceCenter, faceSize);
      setAlignmentScore(score);

      const result: FaceDetectionResult = {
        found: true,
        landmarks: faceLandmarks,
        boundingBox,
        faceCenter,
        faceSize,
        alignmentScore: score,
      };

      setFaceData(result);
      onFaceDetected?.(result);
    } else {
      setFaceData({ found: false });
      setAlignmentScore(0);
      onFaceLost?.();
    }
  }, [onFaceDetected, onFaceLost]);

  const startDetection = useCallback(() => {
    if (!videoRef.current) return;

    // Initialize FaceMesh
    const faceMesh = new FaceMesh({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`;
      },
    });

    faceMesh.setOptions({
      maxNumFaces: 1,
      refineLandmarks: true,
      minDetectionConfidence,
      minTrackingConfidence,
    });

    faceMesh.onResults(processResults);
    faceMeshRef.current = faceMesh;

    // Initialize Camera
    const camera = new Camera(videoRef.current, {
      onFrame: async () => {
        await faceMesh.send({ image: videoRef.current! });
      },
      width: 1280,
      height: 720,
    });

    cameraRef.current = camera;
    camera.start();
    setIsDetecting(true);
  }, [videoRef, minDetectionConfidence, minTrackingConfidence, processResults]);

  const stopDetection = useCallback(() => {
    cameraRef.current?.stop();
    faceMeshRef.current?.close();
    setIsDetecting(false);
    setFaceData(null);
    setAlignmentScore(0);
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopDetection();
    };
  }, [stopDetection]);

  return {
    isDetecting,
    faceData,
    alignmentScore,
    startDetection,
    stopDetection,
  };
}

/**
 * Calculate how well-centered the face is
 */
function calculateAlignmentScore(
  faceCenter: { x: number; y: number },
  faceSize: { width: number; height: number }
): number {
  // Ideal center is (0.5, 0.5)
  const idealCenter = { x: 0.5, y: 0.5 };

  // Calculate distance from ideal center
  const distanceFromCenter = Math.sqrt(
    Math.pow(faceCenter.x - idealCenter.x, 2) +
    Math.pow(faceCenter.y - idealCenter.y, 2)
  );

  // Ideal face size ratio (face should take up ~60% of frame)
  const idealSizeRatio = 0.6;
  const actualSizeRatio = Math.max(faceSize.width, faceSize.height);
  const sizeDifference = Math.abs(actualSizeRatio - idealSizeRatio);

  // Calculate scores (0-1)
  const centerScore = Math.max(0, 1 - distanceFromCenter * 2);
  const sizeScore = Math.max(0, 1 - sizeDifference * 2);

  // Combined score
  return (centerScore + sizeScore) / 2;
}
