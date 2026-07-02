#!/bin/bash

# Determinar la ruta base
if [ -n "$ALFREDO_BASE" ]; then
    BASE="$ALFREDO_BASE"
else
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    BASE="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

source "$BASE/lib/ui"


title "🧪 Alfredo Tools - Test Suite"
echo "=============================="
echo

for module in salud wifi red speed; do
    echo "📦 Probando módulo: $module"
    echo "---"
    if ./modules/$module; then
        echo "✅ $module: ÉXITO"
    else
        echo "❌ $module: FALLÓ"
    fi
    echo "---"
    echo
    read -p "Presiona Enter para continuar..."
    clear
done
