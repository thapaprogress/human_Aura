'use client';

import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { useAuthStore } from '@/store/authStore';
import { Camera, History, Sparkles } from 'lucide-react';

export default function DashboardPage() {
    const router = useRouter();
    const { user } = useAuthStore();

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold">Welcome, {user?.firstName || 'Guest'}</h1>
                    <p className="text-muted-foreground mt-2">
                        Ready to discover your aura today?
                    </p>
                </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
                {/* Start Reading Card */}
                <motion.div
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    className="p-8 rounded-2xl bg-gradient-to-br from-primary/10 to-purple-500/10 border-2 border-primary/20 cursor-pointer text-center flex flex-col items-center justify-center min-h-[300px]"
                    onClick={() => router.push('/session/capture')}
                >
                    <div className="w-20 h-20 rounded-full bg-primary/20 flex items-center justify-center mb-6">
                        <Camera className="w-10 h-10 text-primary" />
                    </div>
                    <h2 className="text-2xl font-bold mb-2">New Reading</h2>
                    <p className="text-muted-foreground mb-6 max-w-xs">
                        Capture your photo and biofeedback data to reveal your current energy.
                    </p>
                    <Button size="lg" className="w-full max-w-xs gap-2">
                        <Sparkles className="w-4 h-4" />
                        Start Session
                    </Button>
                </motion.div>

                {/* History Card (Placeholder) */}
                <div className="p-8 rounded-2xl bg-card border border-border min-h-[300px] flex flex-col">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="w-10 h-10 rounded-lg bg-secondary/20 flex items-center justify-center">
                            <History className="w-5 h-5 text-secondary-foreground" />
                        </div>
                        <h2 className="text-xl font-semibold">Recent Readings</h2>
                    </div>

                    <div className="flex-1 flex flex-col items-center justify-center text-center text-muted-foreground">
                        <p>No recent readings found.</p>
                        <p className="text-sm mt-1">Start your first session to see history!</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
