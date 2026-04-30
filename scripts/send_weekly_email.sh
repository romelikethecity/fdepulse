#!/bin/bash
# Weekly FDE Pulse email send script, run via cron every Tuesday at 8 AM PT
#
# Server cron entry (add with: crontab -e):
#   0 15 * * 2 /bin/bash /home/rome/fdepulse/scripts/send_weekly_email.sh >> /home/rome/logs/fde_email.log 2>&1
#   (15:00 UTC = 8:00 AM PT Tuesday)
#
# Prerequisites:
#   - .env with RESEND_API_KEY and API_SECRET
#   - Domain fdepulse.com verified in Resend
#   - resend + requests Python packages

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/logs"
DATE=$(date +%Y-%m-%d)

# Use scrapers venv if on server, otherwise system python
if [ -f "/home/rome/scrapers/venv/bin/python3" ]; then
    PYTHON="/home/rome/scrapers/venv/bin/python3"
else
    PYTHON="python3"
fi

mkdir -p "$LOG_DIR"
mkdir -p /home/rome/logs 2>/dev/null || true

echo "=============================="
echo "FDE Pulse Weekly Email, $DATE"
echo "=============================="

# Load env if exists
if [ -f "$PROJECT_DIR/.env" ]; then
    export $(grep -v '^#' "$PROJECT_DIR/.env" | xargs)
fi

cd "$PROJECT_DIR"

# Pull latest code (in case generators/data were updated)
git pull --rebase --autostash 2>/dev/null || true

# Send the weekly email
echo "[$(date)] Sending weekly email..."
$PYTHON scripts/generate_weekly_email.py --send

# Push updated snapshot so git reset --hard doesn't lose it
if [ -f "data/previous_market_snapshot.json" ]; then
    git add data/previous_market_snapshot.json
    git diff --staged --quiet || git commit -m "Update FDE Pulse weekly email snapshot ($DATE)" && git push 2>/dev/null || true
fi

echo "[$(date)] Done!"
