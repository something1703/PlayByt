# PlayByt — The Idea, Explained Simply

## The One-Liner

**PlayByt is an AI that watches sports with you and tells you things you'd never notice yourself.**

---

## The Problem

You're watching a football match. The broadcast commentator says "great attack!" — but you have no idea *why* it worked. Was it a formation change? Was the defense exhausted? Was one side of the pitch completely exposed?

Even if you're a hardcore fan, your human eyes can only track one thing at a time. You watch the ball. You miss the 20 other players around it.

Professional analysts get this data — but only *after* the game, from expensive tracking systems. Nobody gets it **live, while watching**.

---

## The Solution

PlayByt is an AI agent that joins your video call, watches the same sports broadcast you're screen-sharing, and gives you **real-time intelligence that no human eye can compute**.

It doesn't just "comment on the game." It:

- Tracks every visible player using computer vision (YOLO pose detection)
- Computes their **zone distribution** — how many players are on the left, center, right
- Estimates the **formation** in real time (is it a 4-3-3? A 3-5-2?)
- Measures **pressing intensity** — how tightly packed the players are
- Detects **fatigue** — forward lean in a player's spine means they're gassing out
- Identifies **side overloads** — "3 players on the left, only 1 on the right = exploit that"

Then it **speaks to you out loud** in real time, combining what it sees with what the data says.

---

## How It Actually Works (No Jargon)

### Step 1: You share your screen

You're watching a match on TV, a stream, whatever. You screen-share it into a PlayByt video room.

### Step 2: The AI "sees" the game

Every 3rd of a second (3 frames per second), the AI takes a screenshot of your screen share. 

A computer vision model called **YOLO** finds every person in the frame and maps 17 body points on each one (head, shoulders, hips, knees, ankles). This is called "pose detection."

### Step 3: The Sports Intelligence Processor kicks in

This is the brain of PlayByt. It takes those 17 body points per player and **computes things humans can't**:

- **Where is everyone?** Divides the screen into zones and counts players in each
- **What formation is this?** Groups players by their vertical position
- **Are they tired?** Measures the angle of each player's spine — if it's leaning forward more than 25°, they're fatiguing
- **Are they pressing?** Calculates the average distance between all players — closer = higher pressing
- **Which side is overloaded?** Compares player counts left vs right

### Step 4: The AI talks to you

Google's Gemini AI model sees:
1. The actual video frame (the match)
2. The YOLO skeleton overlays (player positions highlighted)
3. A **HUD overlay** in the corner showing all the computed data

It combines all three to make specific, data-backed observations:

> "HUD shows 5 players in the defensive third with HIGH pressing — they're setting a trap on the right channel. Watch for the long ball over the top."

That's something no human commentator would say live — because they can't compute zone distributions in their head at 3 FPS.

### Step 5: It logs highlights automatically

When something important happens (goal, card, big save), the AI decides on its own to call a tool function that logs it. After the match, you have a complete timeline of key moments.

---

## What Makes This Different From "Just Asking ChatGPT About Sports"

| | ChatGPT | PlayByt |
|--|---------|---------|
| Sees the game live? | ❌ No | ✅ Yes, via screen share |
| Tracks player positions? | ❌ No | ✅ YOLO pose detection |
| Computes formations in real time? | ❌ No | ✅ Custom analysis engine |
| Detects fatigue from body posture? | ❌ No | ✅ Spine angle calculation |
| Speaks back in real time? | ❌ No | ✅ Voice in, voice out |
| Multi-user? | ❌ No | ✅ Multiple fans in one room |
| Logs highlights automatically? | ❌ No | ✅ Tool calling |

The key difference: **PlayByt doesn't just process language. It processes video frames with computer vision and converts them into structured spatial data that an AI language model can reason about.** That pipeline is what makes it genuinely useful, not a wrapper.

---

## The Role System

Not every fan watches the same way. When you join PlayByt, you pick a role:

| Role | What You Get |
|------|-------------|
| 🧠 **Analyst** | Tactical breakdowns, formation changes, pressing triggers |
| 🔥 **Hype Fan** | Pure energy reactions — "OHHHH WHAT A SAVE!" |
| 📊 **Stats Nerd** | Patterns, probabilities, counting events |
| 📋 **Coach** | Player fitness analysis, positioning errors, improvement tips |

The AI adapts its entire communication style based on your role.

---

## The Tech Stack (Simple Version)

| What | Why |
|------|-----|
| **Vision Agents SDK** (by Stream) | The framework that ties everything together — video, AI, and WebRTC |
| **YOLO v11 Pose** | Finds players and their body positions in each frame |
| **Custom SportsProcessor** | Our code that turns skeleton data into football intelligence |
| **Google Gemini** | The AI brain that sees frames + data and speaks back |
| **Stream Edge** | WebRTC infrastructure — handles the video call plumbing |
| **React Frontend** | The dashboard where fans join, pick roles, and watch |
| **FastAPI Backend** | Generates auth tokens and serves highlight data |

---

## The Pipeline Visualized

```
Your TV / Stream / Laptop
        │
        │  screen share
        ▼
┌─────────────────────────────────────────────────────┐
│  SportsProcessor (our custom code)                  │
│                                                     │
│  Raw Frame ──► YOLO ──► 17 keypoints per player     │
│                  │                                  │
│                  ▼                                  │
│  Analysis Engine:                                   │
│    • Zone distribution (L/C/R, Def/Mid/Att)         │
│    • Formation estimate (4-3-3, etc.)               │
│    • Pressing intensity (high/med/low)              │
│    • Fatigue detection (spine angle > 25°)          │
│    • Side overload detection                        │
│                  │                                  │
│                  ▼                                  │
│  HUD Overlay drawn on frame                         │
│  ┌──────────────────┐                               │
│  │ PLAYBYT INTEL    │                               │
│  │ Players: 8       │                               │
│  │ L:2 C:4 R:2      │                               │
│  │ Formation: 4-3-1  │                               │
│  │ Pressing: HIGH    │                               │
│  └──────────────────┘                               │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  Gemini Realtime                                    │
│                                                     │
│  SEES: video + skeletons + HUD                      │
│  HEARS: user voice                                  │
│  SPEAKS: real-time analysis                         │
│  CALLS TOOLS: log_highlight, get_field_analysis     │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
     Stream WebRTC Video Room
        │         │         │
      Fan 1     Fan 2     Fan 3
    (analyst)   (hype)   (coach)
```

---

## Why It Matters

Sports broadcasts are designed for passive watching. PlayByt turns watching into an **interactive, data-driven experience** — where an AI companion catches the things you miss, adapts to how you like to watch, and builds a highlight log you can review later.

It's not replacing commentators. It's adding a layer of intelligence that only exists because computer vision + AI + real-time video infrastructure came together in 2025-2026.

---

*Built for the Vision Possible: Agent Protocol hackathon — March 2026*
*Powered by Stream Vision Agents SDK + Google Gemini + YOLO v11*
