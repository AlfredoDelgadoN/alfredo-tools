#!/bin/bash

echo "🧪 Alfredo Tools - Test Suite"
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
