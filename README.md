# PlayByt — AI That Catches What You Miss

> Built for **Vision Possible: Agent Protocol** hackathon · Powered by Stream Vision Agents SDK

PlayByt is a multi-user AI sports analysis agent. Fans join a shared room, share a live sports broadcast, and get real-time AI analysis from an agent that **spots what the commentators miss** — tactical shifts, controversial decisions, and emerging patterns — with YOLO player tracking on every frame.

>Deployed link - https://playbyt-i9ae.vercel.app/
>Backend and Agent deployed on an EC2 instance at - https://54-208-69-71.sslip.io/
---

## What It Does

- **Catches what humans miss**: Tactical patterns, early injury signals, referee controversy, pressing traps
- **YOLO player tracking**: YOLOv11 detects players and poses with skeleton overlays on every frame
- **Tool calling**: Agent logs highlights automatically and generates match summaries on demand
- **Role-based analysis**: Join as Analyst 🧠, Hype Fan 🔥, Stats Nerd 📊, or Coach 📋 — get analysis tailored to your style
- **Multi-user rooms**: Multiple fans in the same Stream room — each gets responses matched to their role
- **Voice-native**: Speak to ask questions; PlayByt responds by voice instantly
- **Highlights timeline**: AI-logged key moments displayed in a live timeline panel

---

## Architecture

```
Screen Share (sports broadcast)
         │
         ▼
  SportsProcessor (custom)     ← THE HERO: turns raw video into structured data
    ├── YOLOPoseProcessor      ← Detects players, overlays skeletons
    ├── Analysis Engine        ← Computes zones, formations, fatigue, pressing
    └── HUD Overlay            ← Draws intelligence panel on video frame
         │
         ▼ annotated frames + HUD
  Gemini Realtime (fps=3)     ← Sees video + HUD data + hears audio → speaks back
    ├── log_highlight()       ← Tool: logs key moments to disk
    ├── get_match_summary()   ← Tool: generates match recap
    ├── get_field_analysis()  ← Tool: reads live sports intelligence data
    └── get_highlight_count() ← Tool: returns current count
         │
         ▼
  Stream Edge (WebRTC)        ← Multiple users in same room
         │
    ┌────┴────┐
  Fan 1    Fan 2    Fan N...   ← Each picks a role (analyst/hype/stats/coach)
  (analyst)  (hype)

  FastAPI (server.py)
    ├── /api/token            ← JWT auth for Stream
    ├── /api/call-id          ← Auto-detect active call
    └── /api/highlights       ← Serve logged highlights to frontend
```

---

## Quick Start

### 1. Prerequisites
- Python 3.12+, [uv](https://docs.astral.sh/uv/), Node.js 18+
- API keys: `GEMINI_API_KEY`, `STREAM_API_KEY`, `STREAM_API_SECRET`

### 2. Setup

```bash
# Clone and install Python deps
uv sync

# Configure environment
cp .env.example .env   # Edit with your API keys
```

Create a `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key
STREAM_API_KEY=your_stream_api_key
STREAM_API_SECRET=your_stream_api_secret
```

### 3. Run (3 terminals)

**Terminal 1 — AI Agent:**
```bash
uv run python main.py run
```

**Terminal 2 — Token Server:**
```bash
uv run python -m uvicorn server:app --port 8000
```

**Terminal 3 — Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### 4. Use It

1. Open `http://localhost:5173` in your browser
2. Enter your name — the Call ID auto-fills from the running agent
3. **Pick your role** — Analyst, Hype Fan, Stats Nerd, or Coach
4. Click **Enter Game Room**
5. Click **📺 Share Screen** → select the tab/window with your sports broadcast
6. Unmute your mic and ask PlayByt anything!
7. Watch the **Highlights Timeline** populate as PlayByt logs key moments
8. Share the Call ID with friends so they can join with their own role

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Framework | [Vision Agents SDK](https://visionagents.ai/) by Stream |
| Vision AI | Gemini 2.5 Flash Native Audio (Realtime) |
| Object Detection | YOLOv11 Pose (ultralytics) |
| Tool Calling | `register_function()` — log highlights, match summaries |
| Video Transport | Stream Edge Network (WebRTC) |
| Backend | FastAPI (auth + highlights API) |
| Frontend | React + TypeScript + @stream-io/video-react-sdk |

---

## SDK Features Used

- **`gemini.Realtime(fps=3)`** — Multimodal live analysis (video + audio → speech)
- **`@llm.register_function()`** — Tool calling: field analysis, highlight logging, match summaries
- **`VideoProcessorPublisher`** — Custom `SportsProcessor` subclass: YOLO + analysis engine + HUD overlay
- **`ultralytics.YOLOPoseProcessor`** — Used internally by SportsProcessor for pose detection
- **`getstream.Edge()`** — WebRTC room management via Stream
- **`Agent(..., instructions="Read @instructions.md")`** — File-based agent personality
- **`agent.llm.simple_response()`** — Programmatic greeting on join

---

## Project Structure

```
├── main.py              # Agent with tool calling (Vision Agents SDK)
├── sports_processor.py  # Custom VideoProcessorPublisher: YOLO + analysis + HUD
├── server.py            # FastAPI: auth + call-id + highlights API
├── instructions.md      # Agent identity & role-based behavior rules
├── pyproject.toml       # Python dependencies
├── yolo11n-pose.pt      # YOLO model (auto-downloaded)
├── .env                 # API keys (not committed)
└── frontend/
    ├── src/
    │   ├── App.tsx                    # Root with role system + join/room routing
    │   └── components/
    │       ├── JoinRoom.tsx           # Landing page with role picker
    │       └── PlayBytRoom.tsx        # Dashboard: video + highlights timeline + live feed
    └── package.json
```

---

*Vision Possible: Agent Protocol · Deadline March 1, 2026*
