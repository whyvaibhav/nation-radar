#!/bin/bash
# Stop Crestal Monitor

# Get the script directory and go to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "🛑 Stopping Crestal Network Monitor..."

# Stop scheduler
if [ -f logs/scheduler.pid ]; then
    SCHEDULER_PID=$(cat logs/scheduler.pid)
    if kill -0 $SCHEDULER_PID 2>/dev/null; then
        kill $SCHEDULER_PID
        echo "✅ Scheduler stopped"
    else
        echo "⚠️  Scheduler was not running"
    fi
    rm -f logs/scheduler.pid
fi

# Stop web app
if [ -f logs/webapp.pid ]; then
    WEBAPP_PID=$(cat logs/webapp.pid)
    if kill -0 $WEBAPP_PID 2>/dev/null; then
        kill $WEBAPP_PID
        echo "✅ Web dashboard stopped"
    else
        echo "⚠️  Web dashboard was not running"
    fi
    rm -f logs/webapp.pid
fi

echo "🏁 Crestal Monitor stopped"
