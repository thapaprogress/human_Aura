'use client';

import { useEffect, useRef, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { useBiofeedback } from '@/hooks/useBiofeedback';
import { Camera, RefreshCw, CheckCircle2, Fingerprint } from 'lucide-react';
import { Progress } from '@/components/ui/progress';
import Webcam from 'react-webcam';

export default function CapturePage() {
    const router = useRouter();
    const [step, setStep] = useState<'camera-setup' | 'scanning' | 'complete'>('camera-setup');
    const [isCameraReady, setIsCameraReady] = useState(false);
    const [cameraError, setCameraError] = useState<string | null>(null);

    const webcamRef = useRef<Webcam>(null);

    const {
        isCollecting,
        progress,
        stability,
        startCollection,
    } = useBiofeedback({
        minDuration: 5000,
        onComplete: (session) => {
            setStep('complete');
            handleSessionComplete(session);
        },
    });

    const handleUserMedia = useCallback(() => {
        setIsCameraReady(true);
        setCameraError(null);
    }, []);

    const handleUserMediaError = useCallback((error: string | DOMException) => {
        console.error("Webcam Error:", error);
        setCameraError(typeof error === 'string' ? error : error.message || "Failed to access camera");
        setIsCameraReady(false);
    }, []);

    const handleStartScan = () => {
        if (!isCameraReady) return;
        setStep('scanning');
        startCollection();
    };

    const handleSessionComplete = async (session: any) => {
        // Take photo using react-webcam
        const photoDataUrl = webcamRef.current?.getScreenshot();

        const resultsData = {
            image: photoDataUrl,
            biofeedback: session,
            timestamp: new Date().toISOString(),
        };

        localStorage.setItem('lastSessionResult', JSON.stringify(resultsData));

        setTimeout(() => {
            router.push('/session/results');
        }, 1500);
    };

    return (
        <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-4 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-900/40 via-purple-900/40 to-black z-0" />

            <div className="relative z-10 w-full max-w-2xl bg-black/40 backdrop-blur-xl border border-white/10 rounded-3xl p-6 shadow-2xl">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-400">
                        Aura Scanner
                    </h1>
                    <p className="text-gray-400 mt-2">
                        {step === 'camera-setup' && 'Align your face in the frame'}
                        {step === 'scanning' && 'Scanning your energy field...'}
                        {step === 'complete' && 'Processing results...'}
                    </p>
                </div>

                <div className="relative aspect-video bg-black rounded-2xl overflow-hidden border-2 border-white/20 shadow-inner mb-8 group">
                    <Webcam
                        audio={false}
                        ref={webcamRef}
                        screenshotFormat="image/jpeg"
                        onUserMedia={handleUserMedia}
                        onUserMediaError={handleUserMediaError}
                        className="w-full h-full object-cover transform scale-x-[-1]"
                        videoConstraints={{
                            width: 1280,
                            height: 720,
                            facingMode: "user"
                        }}
                    />

                    <div className="absolute inset-0 grid grid-cols-3 grid-rows-3 opacity-20 pointer-events-none">
                        <div className="border-r border-b border-white/30" />
                        <div className="border-r border-b border-white/30" />
                        <div className="border-b border-white/30" />
                        <div className="border-r border-b border-white/30" />
                        <div className="border-r border-b border-white/30" />
                        <div className="border-b border-white/30" />
                        <div className="border-r border-white/30" />
                        <div className="border-r border-white/30" />
                        <div />
                    </div>

                    {step === 'scanning' && (
                        <motion.div
                            initial={{ top: '0%' }}
                            animate={{ top: '100%' }}
                            transition={{
                                duration: 2,
                                repeat: Infinity,
                                ease: "linear"
                            }}
                            className="absolute left-0 right-0 h-1 bg-gradient-to-r from-transparent via-purple-500 to-transparent shadow-[0_0_15px_rgba(168,85,247,0.8)]"
                        />
                    )}

                    {!isCameraReady && !cameraError && (
                        <div className="absolute inset-0 flex items-center justify-center bg-black/80">
                            <RefreshCw className="w-8 h-8 text-white animate-spin" />
                        </div>
                    )}

                    {cameraError && (
                        <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/80 p-4 text-center">
                            <Camera className="w-12 h-12 text-red-500 mb-4" />
                            <p className="text-red-400 font-medium">Camera Error</p>
                            <p className="text-red-300/80 text-sm mt-1 max-w-xs">{cameraError}</p>
                            <p className="text-gray-400 text-xs mt-4">Please ensure you have granted camera permissions.</p>
                            <Button onClick={() => window.location.reload()} variant="outline" className="mt-6">
                                Try Refreshing
                            </Button>
                        </div>
                    )}
                </div>

                <div className="flex flex-col gap-4">
                    {step === 'camera-setup' && (
                        <Button
                            size="lg"
                            className="w-full h-14 text-lg bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 transition-all font-semibold"
                            onClick={handleStartScan}
                            disabled={!isCameraReady}
                        >
                            <Fingerprint className="w-6 h-6 mr-2" />
                            Start Scan
                        </Button>
                    )}

                    {step === 'scanning' && (
                        <div className="space-y-2">
                            <div className="flex justify-between text-sm text-gray-400">
                                <span>Analyzing biofeedback...</span>
                                <span>{Math.round(progress)}%</span>
                            </div>
                            <Progress value={progress} className="h-3" />
                            <p className="text-xs text-center text-gray-500 mt-2">
                                Stability: {(stability * 100).toFixed(0)}%
                            </p>
                        </div>
                    )}

                    {step === 'complete' && (
                        <motion.div
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            className="flex items-center justify-center gap-2 text-green-400 font-medium py-4"
                        >
                            <CheckCircle2 className="w-6 h-6" />
                            <span>Capture Complete! Redirecting...</span>
                        </motion.div>
                    )}
                </div>
            </div>
        </div>
    );
}
