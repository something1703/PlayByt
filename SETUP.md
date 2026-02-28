# PlayByt — Setup Guide

Get PlayByt running on your machine in ~10 minutes.

---

## Prerequisites

You need these installed before starting:

| Tool | Minimum Version | How to Check | Install Link |
|------|----------------|--------------|--------------|
| **Python** | 3.12+ | `python3 --version` | [python.org/downloads](https://www.python.org/downloads/) |
| **uv** (Python package manager) | Any | `uv --version` | [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) |
| **Node.js** | 18+ | `node --version` | [nodejs.org](https://nodejs.org/) |
| **npm** | 9+ | `npm --version` | Comes with Node.js |
| **Git** | Any | `git --version` | [git-scm.com](https://git-scm.com/) |

### Quick Install (if you don't have them)

**uv** (one command):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Node.js** (via nvm — recommended):
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
nvm install 22
```

---

## Step 1: Clone the Repo

```bash
git clone <repo-url>
cd EdgeEye-agent
```

---

## Step 2: Get Your API Keys

You need **3 keys**. Here's where to get each one:

### 2a. Gemini API Key (Google)

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Click **"Create API Key"**
3. Copy the key — it starts with `AIza...`

### 2b. Stream API Key + Secret

1. Go to [dashboard.getstream.io](https://dashboard.getstream.io)
2. Sign up / log in
3. Create a new app (or use an existing one)
   - Choose **US East** region
4. Go to your app dashboard
5. Copy the **API Key** and **API Secret**

---

## Step 3: Create Environment Files

### Root `.env`

Create a file called `.env` in the project root (`EdgeEye-agent/.env`):

```env
GEMINI_API_KEY=your_gemini_key_here
STREAM_API_KEY=your_stream_api_key_here
STREAM_API_SECRET=your_stream_api_secret_here
```

### Frontend `.env`

Create a file called `.env` inside the `frontend/` folder (`EdgeEye-agent/frontend/.env`):

```env
VITE_STREAM_API_KEY=your_stream_api_key_here
```

> ⚠️ The Stream API key in both files must be the **same key**.

---

## Step 4: Install Python Dependencies

From the project root:

```bash
uv sync
```

This will:
- Create a virtual environment (`.venv/`)
- Install all Python packages: vision-agents SDK, FastAPI, uvicorn, PyJWT, python-dotenv

---

## Step 5: Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

---

## Step 6: Run Everything

You need **3 terminals** running at the same time. Open 3 terminal tabs/windows.

### Terminal 1 — The AI Agent

```bash
uv run python main.py run
```

This starts the PlayByt AI agent. It will:
- Download the YOLO model (~6MB) on first run
- Connect to Stream and join a video call
- Start processing video and speaking

### Terminal 2 — The Backend Server

```bash
uv run uvicorn server:app --host 0.0.0.0 --port 8000
```

This starts the FastAPI backend on `http://localhost:8000`. It handles:
- Authentication tokens for the frontend
- Call ID auto-detection
- Highlight data serving

### Terminal 3 — The Frontend

```bash
cd frontend
npm run dev
```

This starts the React app on `http://localhost:5173`.

---

## Step 7: Use It

1. Open **http://localhost:5173** in your browser
2. Enter your name
3. Pick a fan role:
   - 🧠 **Analyst** — tactical breakdowns
   - 🔥 **Hype Fan** — pure energy
   - 📊 **Stats Nerd** — patterns and numbers
   - 📋 **Coach** — positioning and fitness analysis
4. Click **Join Room**
5. Allow microphone access when prompted
6. Click the **Share Screen** button in the dashboard
7. Select the window/tab where you're watching a sports broadcast
8. The AI agent will start analyzing and speaking!

---

## Project Structure

```
EdgeEye-agent/
├── main.py              # AI agent entry point
├── sports_processor.py  # Custom YOLO + analysis engine
├── server.py            # FastAPI backend
├── instructions.md      # Agent personality/behavior
├── pyproject.toml       # Python dependencies
├── yolo11n-pose.pt      # YOLO model (auto-downloaded)
├── .env                 # API keys (you create this)
│
└── frontend/
    ├── .env             # Frontend API key (you create this)
    ├── package.json     # Node dependencies
    └── src/
        ├── App.tsx          # Root component
        └── components/
            ├── JoinRoom.tsx     # Landing page + role picker
            └── PlayBytRoom.tsx  # Main dashboard
```

---

## Troubleshooting

### "Module not found" errors in Python
```bash
uv sync
```

### YOLO model not downloading
The file `yolo11n-pose.pt` should auto-download on first run. If it doesn't, you're probably behind a firewall. Download it manually from [Ultralytics](https://github.com/ultralytics/assets/releases) and place it in the project root.

### Frontend can't connect to backend
Make sure the backend (Terminal 2) is running on port **8000**. The frontend expects it at `http://localhost:8000`.

### "Invalid API key" errors
Double-check your `.env` files. Make sure there are no extra spaces or quotes around the keys.

### Agent starts but no one joins the call
The agent creates a call when it starts. The frontend auto-detects the call ID from the backend. If that fails, check that both the agent and the backend are using the **same** Stream API key.

### Browser says "Microphone blocked"
Click the lock icon in your address bar → allow microphone access → refresh.

### Python version too old
PlayByt requires Python **3.12 or higher**. Check with:
```bash
python3 --version
```

---

## Ports Used

| Service | Port | URL |
|---------|------|-----|
| Frontend | 5173 | http://localhost:5173 |
| Backend | 8000 | http://localhost:8000 |

---

## Quick Reference — All Commands

```bash
# Install everything
uv sync
cd frontend && npm install && cd ..

# Run everything (3 separate terminals)
uv run python main.py run              # Terminal 1: AI Agent
uv run uvicorn server:app --host 0.0.0.0 --port 8000  # Terminal 2: Backend
cd frontend && npm run dev             # Terminal 3: Frontend

# Open in browser
# http://localhost:5173
```

---

*Built for the Vision Possible: Agent Protocol hackathon — March 2026*
