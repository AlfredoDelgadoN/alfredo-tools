#!/bin/bash
# install.sh - Instalador de Alfredo Tools (Linux)

set -e

# ============================================================
# DETECTAR DIRECTORIO BASE
# ============================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🚀 Instalando Alfredo Tools desde: $SCRIPT_DIR"
echo "========================================"
echo ""

# ============================================================
# VERIFICAR DEPENDENCIAS
# ============================================================
echo "📦 Verificando dependencias..."

MISSING=()
for cmd in git curl wget; do
    if ! command -v $cmd &>/dev/null; then
        MISSING+=($cmd)
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "⚠️  Dependencias faltantes: ${MISSING[*]}"
    echo "   Instalando..."
    sudo apt update -qq
    sudo apt install -y ${MISSING[*]}
fi

# Dependencias opcionales
echo "📦 Instalando dependencias opcionales..."
if command -v apt &>/dev/null; then
    sudo apt update -qq
    sudo apt install -y jq bc speedtest-cli smartmontools lm-sensors || true
fi

echo "✅ Dependencias verificadas"

# ============================================================
# CONFIGURAR PERMISOS
# ============================================================
echo ""
echo "🔧 Configurando permisos..."

# Usar rutas relativas
chmod +x "$SCRIPT_DIR/bin/alfredo"
chmod +x "$SCRIPT_DIR/modules/"* 2>/dev/null || true
chmod +x "$SCRIPT_DIR/lib/"* 2>/dev/null || true

echo "✅ Permisos configurados"

# ============================================================
# CREAR ENLACE GLOBAL
# ============================================================
echo ""
echo "🔗 Creando enlace global..."

# Crear enlace simbólico en /usr/local/bin
sudo ln -sf "$SCRIPT_DIR/bin/alfredo" /usr/local/bin/alfredo
echo "✅ Enlace creado en /usr/local/bin/alfredo"

# ============================================================
# VERIFICAR INSTALACIÓN
# ============================================================
echo ""
echo "🧪 Verificando instalación..."

if command -v alfredo &>/dev/null; then
    echo "✅ Alfredo Tools instalado correctamente"
    echo "   📍 Ubicación: $(which alfredo)"
    echo "   📦 Versión: $(alfredo version 2>/dev/null || echo "v1.0")"
else
    echo "⚠️  Alfredo Tools no está en el PATH"
    echo "   Para usar, ejecuta: $SCRIPT_DIR/bin/alfredo"
fi

# ============================================================
# RESUMEN FINAL
# ============================================================
echo ""
echo "========================================"
echo "          ✅ ¡Instalación Completada!"
echo "========================================"
echo ""
echo "📖 Para usar Alfredo Tools:"
echo ""
echo "   alfredo salud          - Estado del sistema"
echo "   alfredo speed          - Velocidad de Internet"
echo "   alfredo diagnostico    - Diagnóstico completo"
echo "   alfredo help           - Ver todos los comandos"
echo ""
echo "📌 Para más información:"
echo "   https://github.com/AlfredoDelgadoN/alfredo-tools"
echo ""
echo "========================================"
