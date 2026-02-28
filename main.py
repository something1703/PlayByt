"""
PlayByt — AI Sports Analyst That Catches What You Miss
Built with Vision Agents SDK by Stream

Architecture:
  Screen share → YOLO (player/pose detection) → Annotated frames → Gemini Realtime (analysis)
  Users join with a role (analyst/hype/stats/coach).
  Agent uses tool calling to log highlights and generate match reports.
  Google Search grounds stats and player info in real data.
"""

import json
import logging
import time
from pathlib import Path

from dotenv import load_dotenv
from vision_agents.core import Agent, Runner, User
from vision_agents.core.agents import AgentLauncher
from vision_agents.plugins import gemini, getstream

from sports_processor import SportsProcessor

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()

CALL_ID_FILE = Path(__file__).parent / ".call_id"
HIGHLIGHTS_FILE = Path(__file__).parent / ".highlights.json"

# ── Game State ──────────────────────────────────────────────────────────
game_state: dict = {
    "highlights": [],
    "participant_count": 0,
    "start_time": None,
}


def _persist_call_id(call_type: str, call_id: str) -> None:
    """Write the active call ID to disk so the token server can serve it."""
    CALL_ID_FILE.write_text(json.dumps({"call_type": call_type, "call_id": call_id}))
    logger.info("Call ID persisted → %s", CALL_ID_FILE)


def _save_highlights() -> None:
    """Persist highlights to disk for the API."""
    HIGHLIGHTS_FILE.write_text(json.dumps(game_state["highlights"], indent=2))


# ── Agent Factory ───────────────────────────────────────────────────────
async def create_agent(**kwargs) -> Agent:
    """Create the PlayByt sports analyst agent with tools."""

    llm = gemini.Realtime(fps=3)

    # ── Tool: Log Highlight ─────────────────────────────────────────
    @llm.register_function(
        description=(
            "Log a key match highlight. Call this for goals, cards, big saves, "
            "controversial decisions, injuries, or any moment worth remembering. "
            "Provide a short vivid description of what happened."
        )
    )
    async def log_highlight(description: str, category: str = "moment") -> str:
        """Log a highlight moment during the match."""
        highlight = {
            "id": len(game_state["highlights"]) + 1,
            "description": description,
            "category": category,
            "timestamp": time.time(),
            "elapsed": (
                round(time.time() - game_state["start_time"])
                if game_state["start_time"]
                else 0
            ),
        }
        game_state["highlights"].append(highlight)
        _save_highlights()
        logger.info("⚡ Highlight #%d: %s", highlight["id"], description)
        return f"Highlight #{highlight['id']} logged: {description}"

    # ── Tool: Get Match Summary ─────────────────────────────────────
    @llm.register_function(
        description=(
            "Generate a summary of the match so far. Call this when a user asks "
            "for a recap, summary, or 'what did I miss'. Returns all logged highlights."
        )
    )
    async def get_match_summary() -> str:
        """Return all logged highlights as a match summary."""
        if not game_state["highlights"]:
            return "No highlights logged yet. The match is still developing."

        elapsed_total = (
            round(time.time() - game_state["start_time"])
            if game_state["start_time"]
            else 0
        )
        mins = elapsed_total // 60

        lines = [f"Match summary ({mins} min watched, {len(game_state['highlights'])} key moments):"]
        for h in game_state["highlights"]:
            m = h["elapsed"] // 60
            s = h["elapsed"] % 60
            lines.append(f"  [{m:02d}:{s:02d}] {h['description']}")

        return "\n".join(lines)

    # ── Tool: Get Highlight Count ───────────────────────────────────
    @llm.register_function(
        description="Get the number of highlights logged so far in this session."
    )
    async def get_highlight_count() -> str:
        """Return highlight count."""
        count = len(game_state["highlights"])
        return f"{count} highlight{'s' if count != 1 else ''} logged so far."

    # ── Custom Sports Intelligence Processor ────────────────────────
    sports = SportsProcessor(
        model_path="yolo11n-pose.pt",
        conf_threshold=0.5,
        fps=3,
    )

    # ── Tool: Get Field Analysis ────────────────────────────────────
    @llm.register_function(
        description=(
            "Get the current real-time field analysis computed from YOLO pose data. "
            "Returns player count, zone distribution, formation estimate, pressing "
            "intensity, fatigue flags, and dominant side. Call this when you want "
            "to give a tactical breakdown or when users ask about player positioning, "
            "fatigue, formation, or pressing. This data comes from computer vision "
            "analysis that humans cannot compute in real time."
        )
    )
    async def get_field_analysis() -> str:
        """Return the latest sports intelligence analysis."""
        a = sports.latest_analysis
        if not a or a.get("player_count", 0) == 0:
            return "No players currently detected in frame."

        lines = [
            f"Players tracked: {a['player_count']}",
            f"Formation: {a['formation']}",
            f"Pressing intensity: {a['pressing_intensity']}",
            f"Dominant side: {a['dominant_side']}",
            f"Zones — L:{a['zones']['left']} C:{a['zones']['center']} R:{a['zones']['right']}",
            f"Thirds — Def:{a['zones']['def_third']} Mid:{a['zones']['mid_third']} Att:{a['zones']['att_third']}",
        ]

        if a["fatigue_flags"]:
            for f in a["fatigue_flags"]:
                lines.append(
                    f"⚠ Player {f['player_id']+1}: {f['severity']} fatigue "
                    f"(spine angle {f['spine_angle']}°)"
                )

        trend = sports.get_trend()
        if trend.get("trend") != "insufficient_data":
            lines.append(f"Trend: {trend.get('player_movement', 'stable')}")
            lines.append(f"Fatigue events (last 10 frames): {trend.get('fatigue_events_last_10_frames', 0)}")

        return "\n".join(lines)

    # ── Build Agent ─────────────────────────────────────────────────
    agent = Agent(
        edge=getstream.Edge(),
        agent_user=User(name="PlayByt", id="playbyt-agent"),
        instructions="Read @instructions.md",
        llm=llm,
        processors=[sports],
    )

    return agent


# ── Call Lifecycle ──────────────────────────────────────────────────────
async def join_call(agent: Agent, call_type: str, call_id: str, **kwargs) -> None:
    """Join a Stream call and run until it ends."""
    _persist_call_id(call_type, call_id)
    game_state["start_time"] = time.time()
    game_state["highlights"] = []
    _save_highlights()

    call = await agent.create_call(call_type, call_id)

    async with agent.join(call):
        await agent.llm.simple_response(
            text="PlayByt online. Sports intelligence processor active — tracking player "
            "positions, fatigue, formations, and pressing intensity in real time. "
            "Share your screen with the match. I will catch what everyone else misses."
        )
        await agent.finish()


if __name__ == "__main__":
    Runner(AgentLauncher(create_agent=create_agent, join_call=join_call)).cli()
