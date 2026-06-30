import axios from 'axios';

// Backend API base URL. Configured via the VITE_API_BASE_URL env var,
// falling back to the local backend for development.
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api';

export interface DownloadRequest {
    url: string;
    startTime?: string;
    endTime?: string;
    isVertical?: boolean;
    format?: string;
}

export interface TaskStatus {
    status: 'queued' | 'downloading' | 'processing' | 'completed' | 'failed';
    progress: number;
}

export const downloadVideo = async (request: DownloadRequest): Promise<string> => {
    const response = await axios.post(`${BASE_URL}/download`, request);
    return response.data.task_id;
};

export const fetchTaskStatus = async (taskId: string): Promise<TaskStatus> => {
    const response = await axios.get(`${BASE_URL}/status/${taskId}`);
    return response.data;
};

export const getDownloadUrl = (taskId: string): string => {
    return `${BASE_URL}/file/${taskId}`;
};
