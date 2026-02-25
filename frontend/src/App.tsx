import { useState, useEffect } from 'react';
import { DownloadForm } from './components/DownloadForm';
import { ProgressTracker } from './components/ProgressTracker';
import { downloadVideo, fetchTaskStatus, getDownloadUrl } from './api/client';
import type { DownloadRequest, TaskStatus } from './api/client';
import { Sparkles, MonitorPlay } from 'lucide-react';

function App() {
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<TaskStatus | null>(null);

  useEffect(() => {
    let interval: number;

    const checkStatus = async () => {
      if (!taskId) return;
      try {
        const currentStatus = await fetchTaskStatus(taskId);
        setStatus(currentStatus);

        if (currentStatus.status === 'completed') {
          window.location.href = getDownloadUrl(taskId);
        }

        if (currentStatus.status === 'completed' || currentStatus.status === 'failed') {
          clearInterval(interval);
        }
      } catch (e) {
        console.error("Failed to fetch task status", e);
      }
    };

    if (taskId && (!status || (status.status !== 'completed' && status.status !== 'failed'))) {
      interval = window.setInterval(checkStatus, 1500);
      checkStatus();
    }

    return () => clearInterval(interval);
  }, [taskId]);

  const handleDownload = async (request: DownloadRequest) => {
    try {
      const newTaskId = await downloadVideo(request);
      setTaskId(newTaskId);
      setStatus({ status: 'queued', progress: 0 });
    } catch (e) {
      console.error("Failed to start download", e);
      alert("Failed to connect to the backend server. Make sure it's running.");
    }
  };

  const reset = () => {
    setTaskId(null);
    setStatus(null);
  };

  return (
    <div className="min-h-screen bg-slate-950 font-sans selection:bg-purple-500/30 text-slate-50 relative overflow-hidden flex flex-col justify-center items-center p-4">
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-600/20 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-indigo-600/20 blur-[120px] rounded-full pointer-events-none" />

      <main className="w-full max-w-xl relative z-10">
        <div className="text-center mb-10 space-y-4">
          <div className="inline-flex items-center justify-center p-3 bg-white/5 rounded-2xl border border-white/10 backdrop-blur-md mb-2 shadow-2xl">
            <MonitorPlay className="w-8 h-8 text-purple-400" />
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight">
            Stream<span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-indigo-400">Extractor</span>
          </h1>
          <p className="text-lg text-slate-400 flex items-center justify-center gap-2">
            Local multi-platform video downloading <Sparkles className="w-4 h-4 text-amber-300" />
          </p>
        </div>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 shadow-2xl rounded-3xl p-6 md:p-8">
          {(!taskId || !status || status.status === 'queued') ? (
            <DownloadForm onSubmit={handleDownload} isLoading={!!taskId} />
          ) : (
            <ProgressTracker status={status} onReset={reset} />
          )}
        </div>

        <div className="mt-8 text-center text-sm text-slate-500 font-medium">
          Downloads are processed locally on your machine.
        </div>
      </main>

    </div>
  );
}

export default App;
