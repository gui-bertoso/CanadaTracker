#!/usr/bin/env sh
set -eu

PROJECT_DIR="/home/patolizo/Documents/GitHub/CanadaTracker"
PRIMARY_AUTOSTART_DIR="$HOME/.config/autostart"
PRIMARY_DESKTOP_FILE="$PRIMARY_AUTOSTART_DIR/canada-tracker.desktop"
ALT_AUTOSTART_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/autostart"
ALT_DESKTOP_FILE="$ALT_AUTOSTART_DIR/canada-tracker.desktop"

mkdir -p "$PRIMARY_AUTOSTART_DIR"
cp "$PROJECT_DIR/scripts/canada-tracker.desktop" "$PRIMARY_DESKTOP_FILE"

if [ "$ALT_AUTOSTART_DIR" != "$PRIMARY_AUTOSTART_DIR" ]; then
  mkdir -p "$ALT_AUTOSTART_DIR"
  cp "$PROJECT_DIR/scripts/canada-tracker.desktop" "$ALT_DESKTOP_FILE"
fi

chmod +x "$PROJECT_DIR/scripts/run_canada_tracker.sh"
echo "Autostart instalado em $PRIMARY_DESKTOP_FILE"
