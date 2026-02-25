import { useState } from 'react';
import type { DownloadRequest } from '../api/client';
import { Youtube, Settings2, Download, Crop, Clock } from 'lucide-react';

interface Props {
    onSubmit: (data: DownloadRequest) => void;
    isLoading: boolean;
}

export function DownloadForm({ onSubmit, isLoading }: Props) {
    const [url, setUrl] = useState('');
    const [showAdvanced, setShowAdvanced] = useState(false);

    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');
    const [cropW, setCropW] = useState('');
    const [cropH, setCropH] = useState('');
    const [cropX, setCropX] = useState('');
    const [cropY, setCropY] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!url) return;

        onSubmit({
            url,
            startTime: startTime || undefined,
            endTime: endTime || undefined,
            crop: (cropW && cropH) ? {
                width: parseInt(cropW),
                height: parseInt(cropH),
                x: parseInt(cropX) || 0,
                y: parseInt(cropY) || 0
            } : undefined
        });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
                <label className="text-sm font-medium text-purple-100/80 flex items-center gap-2">
                    <Youtube className="w-4 h-4" /> Video URL
                </label>
                <div className="relative">
                    <input
                        type="url"
                        required
                        placeholder="Paste YouTube, X, TikTok, or Instagram link..."
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all font-medium"
                    />
                </div>
            </div>

            <div className="pt-2">
                <button
                    type="button"
                    onClick={() => setShowAdvanced(!showAdvanced)}
                    className="text-xs text-purple-300 hover:text-white flex items-center gap-1.5 transition-colors"
                >
                    <Settings2 className="w-3.5 h-3.5" />
                    {showAdvanced ? 'Hide advanced options' : 'Show advanced options'}
                </button>
            </div>

            {showAdvanced && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm animate-in fade-in slide-in-from-top-2">

                    {/* Trimming */}
                    <div className="space-y-3">
                        <h4 className="text-xs font-semibold text-purple-200 uppercase tracking-wider flex items-center gap-1">
                            <Clock className="w-3.5 h-3.5" /> Trimming
                        </h4>
                        <div className="grid grid-cols-2 gap-2">
                            <input type="text" placeholder="Start (e.g. 00:01:30)" value={startTime} onChange={(e) => setStartTime(e.target.value)} className="w-full bg-black/20 border border-white/5 rounded-lg px-3 py-2 text-sm text-white placeholder-white/20 focus:outline-none focus:border-purple-500/50 transition-colors" />
                            <input type="text" placeholder="End (e.g. 00:02:00)" value={endTime} onChange={(e) => setEndTime(e.target.value)} className="w-full bg-black/20 border border-white/5 rounded-lg px-3 py-2 text-sm text-white placeholder-white/20 focus:outline-none focus:border-purple-500/50 transition-colors" />
                        </div>
                    </div>

                    {/* Cropping */}
                    <div className="space-y-3">
                        <h4 className="text-xs font-semibold text-purple-200 uppercase tracking-wider flex items-center gap-1">
                            <Crop className="w-3.5 h-3.5" /> Cropping (Pixels)
                        </h4>
                        <div className="grid grid-cols-2 gap-2">
                            <input type="number" placeholder="Width" value={cropW} onChange={(e) => setCropW(e.target.value)} className="w-full bg-black/20 border border-white/5 rounded-lg px-3 py-2 text-sm text-white placeholder-white/20 focus:outline-none focus:border-purple-500/50 transition-colors" />
                            <input type="number" placeholder="Height" value={cropH} onChange={(e) => setCropH(e.target.value)} className="w-full bg-black/20 border border-white/5 rounded-lg px-3 py-2 text-sm text-white placeholder-white/20 focus:outline-none focus:border-purple-500/50 transition-colors" />
                            <input type="number" placeholder="X Offset (Opt)" value={cropX} onChange={(e) => setCropX(e.target.value)} className="w-full bg-black/20 border border-white/5 rounded-lg px-3 py-2 text-sm text-white placeholder-white/20 focus:outline-none focus:border-purple-500/50 transition-colors" />
                            <input type="number" placeholder="Y Offset (Opt)" value={cropY} onChange={(e) => setCropY(e.target.value)} className="w-full bg-black/20 border border-white/5 rounded-lg px-3 py-2 text-sm text-white placeholder-white/20 focus:outline-none focus:border-purple-500/50 transition-colors" />
                        </div>
                    </div>

                </div>
            )}

            <button
                type="submit"
                disabled={isLoading || !url}
                className="relative w-full overflow-hidden rounded-xl bg-gradient-to-r from-purple-500 to-indigo-600 p-[1px] group transition-all duration-300 hover:shadow-[0_0_2rem_-0.5rem_#8b5cf6] disabled:opacity-50 disabled:cursor-not-allowed"
            >
                <span className="absolute inset-0 bg-gradient-to-r from-purple-500 to-indigo-600 opacity-0 group-hover:opacity-100 transition-opacity" />
                <div className="relative bg-black/20 backdrop-blur-sm rounded-xl px-6 py-4 flex items-center justify-center gap-2 font-medium text-white transition-all group-hover:bg-transparent">
                    {isLoading ? (
                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    ) : (
                        <>
                            <Download className="w-5 h-5" />
                            <span>Extract & Download</span>
                        </>
                    )}
                </div>
            </button>
        </form>
    );
}
