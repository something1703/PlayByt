#!/bin/bash
set -e

echo "🚀 Starting PlayByt backend..."

# Start AI agent in background
echo "🤖 Starting AI agent (main.py)..."
python main.py &
AGENT_PID=$!

# Give the agent a moment to initialise before accepting HTTP traffic
sleep 3

# Start FastAPI server — Cloud Run expects $PORT
echo "🌐 Starting FastAPI server on port $PORT..."
uvicorn server:app --host 0.0.0.0 --port "$PORT"

# If uvicorn exits, kill the agent too
kill $AGENT_PID 2>/dev/null || true
