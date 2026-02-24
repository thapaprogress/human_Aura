'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import {
    Share2,
    Download,
    RefreshCcw,
    Home,
    Sparkles,
    Zap,
    Shield,
    Heart,
    Compass,
    Activity,
    Info,
    ChevronRight
} from 'lucide-react';
import Image from 'next/image';

export default function ResultsPage() {
    const router = useRouter();
    const [data, setData] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchResults = async () => {
            const stored = localStorage.getItem('lastSessionResult');
            if (!stored) {
                router.push('/dashboard');
                return;
            }

            const sessionData = JSON.parse(stored);

            try {
                // Call actual backend to generate the aura and reading
                const response = await fetch('http://localhost:8000/aura/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        image: sessionData.image,
                        biofeedback_readings: sessionData.biofeedback.readings.map((r: any) => ({
                            timestamp: r.timestamp,
                            touch_x: r.touchX,
                            touch_y: r.touchY,
                            pressure: r.pressure,
                            stability: r.stability,
                            simulated_gsr: r.simulatedGsr,
                            simulated_hrv: r.simulatedHrv,
                            stress_indicator: r.stressIndicator,
                            calmness_score: r.calmnessScore,
                        })),
                        duration_ms: sessionData.biofeedback.durationMs,
                        style: 'medium'
                    })
                });

                if (!response.ok) throw new Error('Failed to generate aura');

                const result = await response.json();

                // Get reading as well
                const readingResponse = await fetch('http://localhost:8000/reading/generate-template', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        aura_profile: result.data.profile,
                        biofeedback_summary: result.data.biofeedback_summary
                    })
                });

                const readingResult = await readingResponse.json();

                setData({
                    ...result.data,
                    reading: readingResult.data.sections
                });
            } catch (err) {
                console.error("Backend error, falling back to mock:", err);
                setData(sessionData);
            } finally {
                setIsLoading(false);
            }
        };

        fetchResults();
    }, [router]);

    if (isLoading) return (
        <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center">
            <div className="relative">
                <motion.div
                    animate={{
                        scale: [1, 1.2, 1],
                        rotate: 360,
                        opacity: [0.3, 0.6, 0.3]
                    }}
                    transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                    className="w-32 h-32 rounded-full border-t-2 border-purple-500 blur-sm absolute -inset-2"
                />
                <motion.div
                    animate={{ rotate: -360 }}
                    transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
                >
                    <Sparkles className="w-16 h-16 text-purple-400" />
                </motion.div>
            </div>
            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-8 text-center"
            >
                <h2 className="text-2xl font-bold tracking-widest text-white uppercase italic">Analyzing Energy</h2>
                <div className="flex gap-1 justify-center mt-2">
                    {[0, 1, 2].map((i) => (
                        <motion.div
                            key={i}
                            animate={{ opacity: [0.2, 1, 0.2] }}
                            transition={{ duration: 1, delay: i * 0.2, repeat: Infinity }}
                            className="w-1.5 h-1.5 bg-purple-500 rounded-full"
                        />
                    ))}
                </div>
            </motion.div>
        </div>
    );

    if (!data) return null;

    // Map backend colors to CSS colors
    const colorMap: Record<string, string> = {
        red: '#FF3333', orange: '#FF8800', yellow: '#FFDD00', green: '#33CC33',
        blue: '#3366FF', indigo: '#4B0082', violet: '#9400D3', pink: '#FF69B4',
        white: '#FFFFFF', gold: '#FFD700', silver: '#C0C0C0', turquoise: '#40E0D0',
        magenta: '#FF00FF', emerald: '#50C878', citrine: '#E4D00A', amethyst: '#9966CC',
        sapphire: '#0F52BA', ruby: '#E0115F', garnet: '#733635', opal: '#A9C6D5',
        peridot: '#8EB650', topaz: '#FFC87C', aquamarine: '#7FFFD4', lapis: '#26619C',
        carnelian: '#B31B1B', rose_quartz: '#FBC3C3', smoky_quartz: '#606060',
        tigers_eye: '#B5893E', moonstone: '#D2D2E6', sunstone: '#FFA54F',
        labradorite: '#8080A0', malachite: '#0BDA51', aventurine: '#50B450',
        obsidian: '#141414', jade: '#00A86B', amber: '#FFBF00', copper: '#B87333'
    };

    const majorityColor = colorMap[data.profile?.majority_color] || '#8B5CF6';
    const accentColors = data.profile?.moderate_colors.map((c: string) => colorMap[c] || '#D8B4FE') || ['#D8B4FE', '#6366F1'];

    return (
        <div className="min-h-screen bg-black text-white p-4 md:p-8 flex items-start justify-center overflow-x-hidden selection:bg-purple-500/30">
            {/* Background Ambient Glow */}
            <div
                className="fixed inset-0 pointer-events-none opacity-20 blur-[120px] transition-all duration-1000"
                style={{
                    background: `radial-gradient(circle at 70% 30%, ${majorityColor}, transparent 50%), radial-gradient(circle at 10% 80%, ${accentColors[0]}, transparent 50%)`
                }}
            />

            <div className="max-w-7xl w-full grid lg:grid-cols-12 gap-12 items-start py-8 relative z-10">

                {/* Left Column: Artistic Portrait (span 5) */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 1.2 }}
                    className="lg:col-span-5 lg:sticky lg:top-8"
                >
                    <div className="group relative">
                        {/* The Aura Image */}
                        <div className="relative aspect-[4/5] rounded-[48px] overflow-hidden shadow-[0_40px_100px_rgba(0,0,0,0.6)] border border-white/10 isolate">
                            <img
                                src={data.image}
                                alt="Your Aura Reading"
                                className="w-full h-full object-cover brightness-105 contrast-[1.05] scale-[1.01] hover:scale-105 transition-transform duration-[20s] ease-linear"
                            />

                            {/* Refined Glass Overlays */}
                            <div className="absolute inset-x-0 bottom-0 h-1/3 bg-gradient-to-t from-black/80 to-transparent z-20" />

                            {/* Metadata Floating Badge */}
                            <div className="absolute top-8 left-8 z-40">
                                <motion.div
                                    initial={{ x: -20, opacity: 0 }}
                                    animate={{ x: 0, opacity: 1 }}
                                    transition={{ delay: 1 }}
                                    className="bg-black/40 backdrop-blur-xl border border-white/10 pl-2 pr-6 py-2 rounded-full flex items-center gap-3"
                                >
                                    <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center">
                                        <Activity className="w-4 h-4 text-white" />
                                    </div>
                                    <div className="flex flex-col">
                                        <span className="text-[8px] font-bold uppercase tracking-widest text-white/40">Status</span>
                                        <span className="text-[10px] font-bold text-white uppercase tracking-tighter">Alignment Verified</span>
                                    </div>
                                </motion.div>
                            </div>
                        </div>

                        {/* Decorative Frames */}
                        <div className="absolute -inset-4 border border-white/5 rounded-[60px] pointer-events-none -z-10 group-hover:scale-105 transition-transform duration-1000" />
                        <div className="absolute -inset-8 border border-white/5 rounded-[72px] pointer-events-none -z-20 group-hover:scale-110 transition-transform duration-1000 delay-100" />
                    </div>
                </motion.div>

                {/* Right Column: Narrative & Stats (span 7) */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1, delay: 0.2 }}
                    className="lg:col-span-7 flex flex-col gap-10"
                >
                    {/* Header: Title & Chakra */}
                    <div className="space-y-6">
                        <div className="inline-flex items-center gap-4 px-4 py-2 bg-white/5 rounded-full border border-white/10">
                            <div className="w-3 h-3 rounded-full animate-pulse shadow-[0_0_10px_currentColor]" style={{ backgroundColor: majorityColor, color: majorityColor }} />
                            <span className="text-xs font-black uppercase tracking-[0.4em] text-white/60">Molecular Signature</span>
                        </div>

                        <div className="space-y-2">
                            <h1 className="text-7xl xl:text-8xl font-black italic tracking-tighter leading-[0.85] uppercase">
                                <span className="text-white block">The</span>
                                <span className="text-transparent bg-clip-text bg-gradient-to-br from-white via-white/80 to-white/20 block"
                                    style={{ WebkitTextFillColor: 'transparent', backgroundImage: `linear-gradient(135deg, white, ${majorityColor})` }}>
                                    {data.profile?.majority_color}
                                </span>
                                <span className="text-white block">Frequency</span>
                            </h1>
                        </div>

                        {/* Chakra & Dominance Stats */}
                        <div className="flex flex-wrap gap-4 pt-4">
                            <div className="px-6 py-4 bg-zinc-900 border border-white/10 rounded-3xl flex items-center gap-4 group hover:bg-zinc-800 transition-colors">
                                <div className="p-3 bg-white/5 rounded-2xl group-hover:bg-white/10 transition-colors">
                                    <Compass className="w-6 h-6 text-white" />
                                </div>
                                <div>
                                    <p className="text-[10px] text-white/40 uppercase font-black tracking-widest">Active Chakra</p>
                                    <p className="text-xl font-bold italic text-white tracking-tight">{data.profile?.chakra}</p>
                                </div>
                            </div>
                            <div className="px-6 py-4 bg-zinc-900 border border-white/10 rounded-3xl flex items-center gap-4 group hover:bg-zinc-800 transition-colors">
                                <div className="p-3 bg-white/5 rounded-2xl group-hover:bg-white/10 transition-colors">
                                    <Zap className="w-6 h-6 text-yellow-400" />
                                </div>
                                <div>
                                    <p className="text-[10px] text-white/40 uppercase font-black tracking-widest">Dominance</p>
                                    <p className="text-xl font-bold italic text-white tracking-tight">{data.profile?.majority_percentage}%</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Content Blocks */}
                    <div className="grid gap-6">
                        {data.reading?.map((section: any, idx: number) => (
                            <motion.div
                                key={idx}
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.5 + idx * 0.1 }}
                                className="relative overflow-hidden group"
                            >
                                <div className="absolute inset-0 bg-zinc-900/40 backdrop-blur-3xl rounded-[40px] border border-white/10 group-hover:border-white/20 transition-all" />
                                <div className="relative p-10 flex flex-col md:flex-row gap-8 items-start">
                                    <div className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center shrink-0 mt-1">
                                        {section.section === 'color_analysis' && <Info className="w-6 h-6 text-indigo-400" />}
                                        {section.section === 'alignment' && <Shield className="w-6 h-6 text-emerald-400" />}
                                        {section.section === 'guidance' && <Heart className="w-6 h-6 text-rose-400" />}
                                    </div>
                                    <div className="space-y-4">
                                        <h3 className="text-sm font-bold uppercase tracking-[0.25em] text-white/40 group-hover:text-white/80 transition-colors flex items-center gap-2">
                                            {section.title}
                                            <ChevronRight className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-all translate-x-[-4px] group-hover:translate-x-0" />
                                        </h3>
                                        <p className="text-xl font-light leading-relaxed text-gray-300 antialiased">
                                            {section.content}
                                        </p>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>

                    {/* User Action Footer */}
                    <div className="mt-6 space-y-4">
                        <Button className="w-full h-20 rounded-[32px] bg-white text-black hover:bg-zinc-200 text-xl font-black uppercase italic tracking-tight transition-all active:scale-[0.98] shadow-[0_20px_40px_rgba(255,255,255,0.1)]">
                            <Share2 className="w-6 h-6 mr-4" /> Share Your Aura
                        </Button>

                        <div className="grid grid-cols-2 gap-4">
                            <Button
                                variant="outline"
                                className="h-16 rounded-[24px] bg-transparent text-white border-white/10 hover:bg-white/5 hover:border-white/30 font-bold uppercase tracking-[0.2em] text-[10px]"
                                onClick={() => router.push('/session/capture')}
                            >
                                <RefreshCcw className="w-4 h-4 mr-3" /> Retake Scan
                            </Button>
                            <Button
                                variant="outline"
                                className="h-16 rounded-[24px] bg-transparent text-white border-white/10 hover:bg-white/5 hover:border-white/30 font-bold uppercase tracking-[0.2em] text-[10px]"
                                onClick={() => router.push('/dashboard')}
                            >
                                <Home className="w-4 h-4 mr-3" /> Dashboard
                            </Button>
                        </div>
                    </div>
                </motion.div>
            </div>
        </div>
    );
}
