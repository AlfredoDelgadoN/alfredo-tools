#!/bin/bash

echo "🚀 Instalando Alfredo Tools v0.9..."
echo "========================================"
echo

# Verificar dependencias
echo "📦 Verificando dependencias..."
DEPENDENCIAS=(bash awk grep sed ping iw jq bc speedtest-cli smartmontools lm-sensors)
FALTANTES=()

for cmd in "${DEPENDENCIAS[@]}"; do
    if ! command -v $cmd &>/dev/null; then
        FALTANTES+=($cmd)
    fi
done

if [ ${#FALTANTES[@]} -gt 0 ]; then
    echo "⚠️  Dependencias faltantes: ${FALTANTES[*]}"
    echo "   Instala con: sudo apt install ${FALTANTES[*]}"
    read -p "¿Continuar de todas formas? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
else
    echo "✅ Todas las dependencias instaladas"
fi

# Dar permisos
echo
echo "🔧 Configurando permisos..."
chmod +x ~/Documentos/alfredo-tools/bin/alfredo
chmod +x ~/Documentos/alfredo-tools/modules/*
chmod +x ~/Documentos/alfredo-tools/lib/*

# Crear enlace simbólico
echo
echo "🔗 Creando enlace global..."
sudo ln -sf ~/Documentos/alfredo-tools/bin/alfredo /usr/local/bin/alfredo

# Verificar instalación
echo
echo "✅ Instalación completada"
echo
echo "📊 Resumen:"
echo "  📂 Ubicación: ~/Documentos/alfredo-tools"
echo "  🔗 Comando: alfredo"
echo "  📦 Módulos: $(ls -1 ~/Documentos/alfredo-tools/modules | wc -l)"
echo
echo "📖 Para ver todos los módulos:"
echo "  alfredo help"
