# StreamExtractor - Local Video Downloader

**StreamExtractor** is a modern, fast, and local web application that allows you to paste a video URL from supported social media platforms (YouTube, Twitter/X, TikTok, Instagram, etc.) and download the processed video directly to your local system.

It features a premium React UI with glassmorphism design and a powerful Python backend using FastAPI, `yt-dlp`, and `FFmpeg`.

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

# Start the server
python -m uvicorn backend.main:app --reload --port 8000
```
The FastAPI backend will now be running at `http://localhost:8000`.

### 2. Start the Frontend

Open a **new** terminal window, navigate to the frontend folder, and start the development server:

```bash
cd frontend

# Install Node dependencies
npm install

# Start the Vite dev server
npm run dev
```
The React frontend will be running at `http://localhost:5173`.

---

## 💻 Usage

1. Open your browser and navigate to `http://localhost:5173`.
2. Paste the URL of the video you want to download.
3. Optional: Click "Show advanced options" to specify start/end times or crop dimensions in pixels.
4. Click **Extract & Download**.
5. Wait for the extraction and processing phases to complete. The file will automatically begin downloading to your browser once ready!
