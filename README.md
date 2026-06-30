# StreamExtractor - Local Video Downloader

**StreamExtractor** is a modern, fast, and local web application that allows you to paste a video URL from supported social media platforms (YouTube, Twitter/X, TikTok, Instagram, etc.) and download the processed video directly to your local system.

It features a premium React UI with glassmorphism design and a powerful Python backend using FastAPI, `yt-dlp`, and `FFmpeg`.

> ⭐ **If you find this project useful, please consider giving it a star on GitHub!** It helps others discover the project and motivates continued development. [Star this repo →](https://github.com/sidharthhhh/stremextractor)

---

## 🌟 Features
- **Wide Platform Support**: Powered by `yt-dlp` to support hundreds of websites.
- **Optional Processing**: Trim your videos by start/end times or crop by dimensions using `FFmpeg`.
- **Live Progress Tracking**: See exactly what the server is doing while downloading or processing.
- **Local Privacy**: Everything runs on your own machine. Downloaded videos and temp files are automatically deleted from the server space shortly after your extraction finishes.
- **Modern UI**: An atmospheric and highly responsive user interface built with Vite, React, and TailwindCSS.

---

## 🚀 Getting Started

### Prerequisites
1. **Node.js** (v18 or higher) for the React frontend.
2. **Python** (3.9 or higher) for the FastAPI backend.
3. **FFmpeg** installed on your system.
   - *Windows*: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or use a package manager like `choco install ffmpeg`.
   - *Mac*: `brew install ffmpeg`
   - *Linux*: `sudo apt install ffmpeg`

### 1. Start the Backend

Open a terminal in the root directory and set up the Python environment:

```bash
# Optional but recommended: Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Configure environment variables (copy the example and edit as needed)
cp backend/.env.example backend/.env

# Start the server
python -m uvicorn backend.main:app --reload --port 8000

# On Windows using the venv Python (if the above doesn't find uvicorn):
.\backend\venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000
```

The FastAPI backend will now be running at `http://localhost:8000`.

### 2. Start the Frontend

Open a **new** terminal window, navigate to the frontend folder, and start the development server:

```bash
cd frontend

# Install Node dependencies
npm install

# Configure environment variables (copy the example and edit as needed)
cp .env.example .env

# Start the Vite dev server
npm run dev
```
The React frontend will be running at `http://localhost:5173`.

---

## ⚙️ Configuration (Environment Variables)

Both services are configured via `.env` files. Copy the provided `.env.example`
files and override values per environment. **Never commit real `.env` files** —
they are gitignored; only the `.env.example` templates are tracked.

### Backend (`backend/.env`)

| Variable | Default | Description |
| --- | --- | --- |
| `HOST` | `0.0.0.0` | Address the server binds to. |
| `PORT` | `8000` | Port the server listens on. |
| `RELOAD` | `false` | Auto-reload on code changes (local dev only). |
| `DEBUG` | `false` | Exposes the `/api/debug/tasks` endpoint. Keep `false` in production. |
| `CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Comma-separated list of allowed frontend origins. |
| `TEMP_DIR` | `backend/temp` | Directory for temporary download/processing files. |
| `FILE_CLEANUP_DELAY` | `5` | Seconds to keep a finished file before deleting it. |

### Frontend (`frontend/.env`)

| Variable | Default | Description |
| --- | --- | --- |
| `VITE_API_BASE_URL` | `http://127.0.0.1:8000/api` | Base URL of the backend API (including the `/api` prefix). |

### Production notes

- Set `DEBUG=false` and `RELOAD=false`.
- Restrict `CORS_ORIGINS` to your real frontend domain(s) — avoid `*`.
- Point `VITE_API_BASE_URL` at your deployed backend, then rebuild the frontend
  (`npm run build`) so the value is baked into the static assets.
- Run the backend without `--reload`, e.g.
  `python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000`.

---

## 💻 Usage

1. Open your browser and navigate to `http://localhost:5173`.
2. Paste the URL of the video you want to download.
3. Optional: Click "Show advanced options" to specify start/end times or crop dimensions in pixels.
4. Click **Extract & Download**.
5. Wait for the extraction and processing phases to complete. The file will automatically begin downloading to your browser once ready!
