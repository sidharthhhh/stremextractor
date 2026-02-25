import type { TaskStatus } from '../api/client';
import { CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';

interface Props {
    status: TaskStatus;
    onReset: () => void;
}

export function ProgressTracker({ status, onReset }: Props) {
    const isFinished = status.status === 'completed';
    const isFailed = status.status === 'failed';
    const isProcessing = status.status === 'processing';
    const isDownloading = status.status === 'downloading';

    let message = 'Preparing download...';
    if (isDownloading) message = `Downloading video... ${status.progress.toFixed(1)}%`;
    if (isProcessing) message = 'Processing with FFmpeg...';
    if (isFinished) message = 'Extraction complete! Starting download...';
    if (isFailed) message = 'Failed to extract video.';

    return (
        <div className="flex flex-col items-center justify-center py-8 space-y-6">

            <div className="relative">
                {/* Glow effect */}
                <div className={`absolute inset-0 rounded-full blur-xl opacity-50 ${isFinished ? 'bg-green-500' : isFailed ? 'bg-red-500' : 'bg-purple-500'} animate-pulse`} />

                {/* Icon based on state */}
                <div className="relative w-20 h-20 bg-white/10 backdrop-blur-xl border border-white/20 rounded-full flex items-center justify-center shadow-2xl">
                    {isFinished ? (
                        <CheckCircle2 className="w-10 h-10 text-green-400" />
                    ) : isFailed ? (
                        <AlertCircle className="w-10 h-10 text-red-400" />
                    ) : (
                        <Loader2 className="w-10 h-10 text-purple-400 animate-spin" />
                    )}
                </div>
            </div>

            <div className="text-center space-y-2">
                <h3 className="text-lg font-medium text-white">{message}</h3>
                {!isFinished && !isFailed && (
                    <p className="text-sm text-purple-200/60 font-mono">
                        {status.status.toUpperCase()}
                    </p>
                )}
            </div>

            {(!isFinished && !isFailed) && (
                <div className="w-full max-w-sm h-2 bg-white/5 rounded-full overflow-hidden border border-white/5">
                    <div
                        className="h-full bg-gradient-to-r from-purple-500 to-indigo-500 transition-all duration-300 ease-out"
                        style={{ width: `${Math.max(5, status.progress)}%` }}
                    />
                </div>
            )}

            {(isFinished || isFailed) && (
                <button
                    onClick={onReset}
                    className="mt-6 px-6 py-2.5 rounded-lg bg-white/10 hover:bg-white/20 border border-white/10 text-sm font-medium text-white transition-all backdrop-blur-md"
                >
                    {isFailed ? 'Try Again' : 'Extract Another Video'}
                </button>
            )}

        </div>
    );
}
