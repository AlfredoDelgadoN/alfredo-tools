#!/bin/bash

# Alfredo Tools - Installer
# Uso: ./install.sh

set -e

echo "🚀 Instalando Alfredo Tools..."
echo "================================"

# Verificar dependencias
echo "📦 Verificando dependencias..."
MISSING=()
for cmd in iw jq bc speedtest; do
    if ! command -v $cmd &>/dev/null; then
        MISSING+=($cmd)
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "⚠️  Dependencias faltantes: ${MISSING[*]}"
    echo "   Instala con: sudo apt install ${MISSING[*]}"
    read -p "¿Continuar de todas formas? (s/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

# Dar permisos
echo "🔧 Configurando permisos..."
chmod +x bin/alfredo
chmod +x modules/*

# Crear enlace simbólico
echo "🔗 Creando enlace global..."
sudo ln -sf $(pwd)/bin/alfredo /usr/local/bin/alfredo

# Verificar instalación
echo "✅ Verificando instalación..."
if command -v alfredo &>/dev/null; then
    echo "✅ Alfredo Tools instalado correctamente"
    echo "📍 Ubicación: $(which alfredo)"
    echo
    echo "📖 Uso: alfredo [salud|wifi|red|speed]"
else
    echo "❌ Error en la instalación"
    exit 1
fi
