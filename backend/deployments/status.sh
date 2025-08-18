#!/bin/bash
# Check Crestal Monitor Status

# Get the script directory and go to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "🎯 Crestal Network Monitor Status"
echo "================================="

# Check if processes are running
SCHEDULER_RUNNING=false
WEBAPP_RUNNING=false

if [ -f logs/scheduler.pid ]; then
    SCHEDULER_PID=$(cat logs/scheduler.pid)
    if kill -0 $SCHEDULER_PID 2>/dev/null; then
        SCHEDULER_RUNNING=true
        echo "✅ Scheduler:        Running (PID: $SCHEDULER_PID)"
    else
        echo "❌ Scheduler:        Stopped"
    fi
else
    echo "❌ Scheduler:        Not started"
fi

if [ -f logs/webapp.pid ]; then
    WEBAPP_PID=$(cat logs/webapp.pid)
    if kill -0 $WEBAPP_PID 2>/dev/null; then
        WEBAPP_RUNNING=true
        echo "✅ Web Dashboard:    Running (PID: $WEBAPP_PID)"
    else
        echo "❌ Web Dashboard:    Stopped"
    fi
else
    echo "❌ Web Dashboard:    Not started"
fi

echo ""
echo "📁 Data Files:"
echo "================================="

# Check data files
if [ -f tweets.csv ]; then
    LINES=$(wc -l < tweets.csv)
    SIZE=$(du -h tweets.csv | cut -f1)
    echo "✅ tweets.csv:       $LINES lines, $SIZE"
else
    echo "❌ tweets.csv:       Not found"
fi

if [ -f tweets.db ]; then
    SIZE=$(du -h tweets.db | cut -f1)
    echo "✅ tweets.db:        $SIZE"
else
    echo "❌ tweets.db:        Not found"
fi

if [ -f config.yaml ]; then
    echo "✅ config.yaml:      Present"
else
    echo "❌ config.yaml:      Missing"
fi

echo ""
echo "📊 Recent Activity:"
echo "================================="

# Show recent log entries
if [ -f logs/scheduler.log ]; then
    echo "Last 3 scheduler log entries:"
    tail -n 3 logs/scheduler.log
else
    echo "No scheduler logs found"
fi

echo ""
echo "💾 Disk Usage:"
echo "================================="
df -h /opt/crestal-monitor
