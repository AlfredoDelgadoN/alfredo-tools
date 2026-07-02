#!/bin/bash
echo "🧪 Probando Alfredo Tools..."
echo

for module in salud wifi red speed; do
    echo "📦 Probando módulo: $module"
    if ~/Documentos/alfredo-tools/modules/$module; then
        echo "✅ $module: OK"
    else
        echo "❌ $module: ERROR"
    fi
    echo "---"
    echo
done
EOF

chmod +x ~/Documentos/alfredo-tools/test.sh
~/Documentos/alfredo-tools/test.sh
