#!/bin/bash

# Alfredo Tools - Installer
# Uso: ./install.sh [--help] [--force]

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# Configuración
PROJECT_NAME="Alfredo Tools"
PROJECT_VERSION="v0.6"
INSTALL_DIR="/usr/local/bin"
PROJECT_DIR="$(pwd)"

# Funciones
echo_color() {
    echo -e "${2}${1}${RESET}"
}

show_header() {
    clear
    echo_color "=========================================" "$CYAN"
    echo_color "          Alfredo Tools Installer" "$BOLD$CYAN"
    echo_color "          Version $PROJECT_VERSION" "$CYAN"
    echo_color "=========================================" "$CYAN"
    echo
}

show_help() {
    show_header
    echo "Uso: ./install.sh [OPCIONES]"
    echo
    echo "Opciones:"
    echo "  --help, -h     Mostrar esta ayuda"
    echo "  --force, -f    Forzar instalación sin confirmación"
    echo "  --uninstall    Desinstalar Alfredo Tools"
    echo
    echo "El instalador verificará dependencias y configurará el proyecto."
}

check_dependencies() {
    echo_color "📦 Verificando dependencias..." "$BLUE"
    echo "--------------------------------------------------"
    
    local MISSING=()
    local OPTIONAL=()
    
    # Dependencias obligatorias
    for cmd in bash awk grep sed ping; do
        if ! command -v $cmd &>/dev/null; then
            MISSING+=($cmd)
        fi
    done
    
    # Dependencias para módulos específicos
    for cmd in iw jq bc speedtest; do
        if ! command -v $cmd &>/dev/null; then
            OPTIONAL+=($cmd)
        fi
    done
    
    # Verificar dependencias obligatorias
    if [ ${#MISSING[@]} -gt 0 ]; then
        echo_color "❌ Dependencias obligatorias faltantes:" "$RED"
        for cmd in "${MISSING[@]}"; do
            echo "   - $cmd"
        done
        echo
        echo_color "⚠️  El sistema no podrá funcionar correctamente" "$YELLOW"
        return 1
    else
        echo_color "✅ Dependencias obligatorias: OK" "$GREEN"
    fi
    
    # Verificar dependencias opcionales
    if [ ${#OPTIONAL[@]} -gt 0 ]; then
        echo
        echo_color "⚠️  Dependencias opcionales faltantes:" "$YELLOW"
        for cmd in "${OPTIONAL[@]}"; do
            echo "   - $cmd"
        done
        echo
        echo_color "📌 Algunos módulos no funcionarán completamente" "$YELLOW"
        echo "   Instala con: sudo apt install ${OPTIONAL[*]}"
        echo
        read -p "¿Continuar de todas formas? (s/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Ss]$ ]]; then
            echo_color "❌ Instalación cancelada" "$RED"
            exit 1
        fi
    else
        echo_color "✅ Dependencias opcionales: OK" "$GREEN"
    fi
    
    return 0
}

install_project() {
    echo
    echo_color "🔧 Configurando Alfredo Tools..." "$BLUE"
    echo "--------------------------------------------------"
    
    # Verificar estructura de directorios
    local DIRS=("bin" "lib" "modules" "docs" "tests")
    for dir in "${DIRS[@]}"; do
        if [ ! -d "$PROJECT_DIR/$dir" ]; then
            echo_color "   ⚠️  Creando directorio: $dir" "$YELLOW"
            mkdir -p "$PROJECT_DIR/$dir"
        fi
    done
    
    # Dar permisos de ejecución
    echo "   🔑 Asignando permisos..."
    chmod +x "$PROJECT_DIR/bin/alfredo" 2>/dev/null || echo "   ⚠️  bin/alfredo no encontrado"
    chmod +x "$PROJECT_DIR/modules/"* 2>/dev/null || echo "   ⚠️  Módulos no encontrados"
    chmod +x "$PROJECT_DIR/lib/"* 2>/dev/null || echo "   ⚠️  Librerías no encontradas"
    
    echo_color "✅ Permisos configurados" "$GREEN"
}

create_symlink() {
    echo
    echo_color "🔗 Creando enlace simbólico..." "$BLUE"
    echo "--------------------------------------------------"
    
    local TARGET="$PROJECT_DIR/bin/alfredo"
    local LINK="$INSTALL_DIR/alfredo"
    
    # Verificar si el enlace ya existe
    if [ -L "$LINK" ] || [ -f "$LINK" ]; then
        echo "   ⚠️  Ya existe un archivo en $LINK"
        read -p "   ¿Sobrescribir? (s/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Ss]$ ]]; then
            echo_color "❌ Instalación cancelada" "$RED"
            exit 1
        fi
        sudo rm -f "$LINK"
    fi
    
    # Crear enlace
    sudo ln -sf "$TARGET" "$LINK"
    
    if [ -L "$LINK" ]; then
        echo_color "✅ Enlace creado: $LINK -> $TARGET" "$GREEN"
    else
        echo_color "❌ Error al crear el enlace" "$RED"
        return 1
    fi
}

verify_installation() {
    echo
    echo_color "🧪 Verificando instalación..." "$BLUE"
    echo "--------------------------------------------------"
    
    if command -v alfredo &>/dev/null; then
        echo_color "✅ Alfredo Tools instalado correctamente" "$GREEN"
        echo "   📍 Ubicación: $(which alfredo)"
        echo "   📦 Versión: $PROJECT_VERSION"
        
        # Verificar módulos disponibles
        echo
        echo "   📂 Módulos disponibles:"
        if [ -d "$PROJECT_DIR/modules" ]; then
            for module in $(ls -1 "$PROJECT_DIR/modules" 2>/dev/null); do
                if [ -x "$PROJECT_DIR/modules/$module" ]; then
                    echo "      ✅ $module"
                else
                    echo "      ⚠️  $module (no ejecutable)"
                fi
            done
        fi
        return 0
    else
        echo_color "❌ Error: Alfredo Tools no está en el PATH" "$RED"
        return 1
    fi
}

uninstall() {
    echo
    echo_color "🗑️  Desinstalando Alfredo Tools..." "$RED"
    echo "--------------------------------------------------"
    
    # Eliminar enlace simbólico
    if [ -L "$INSTALL_DIR/alfredo" ]; then
        sudo rm -f "$INSTALL_DIR/alfredo"
        echo_color "✅ Enlace eliminado" "$GREEN"
    else
        echo_color "ℹ️  No se encontró enlace en $INSTALL_DIR" "$YELLOW"
    fi
    
    echo
    echo_color "💡 Para eliminar completamente el proyecto:" "$YELLOW"
    echo "   rm -rf $PROJECT_DIR"
    echo
    echo_color "✅ Desinstalación completada" "$GREEN"
}

show_summary() {
    echo
    echo_color "=========================================" "$CYAN"
    echo_color "          Instalación Completada" "$BOLD$GREEN"
    echo_color "=========================================" "$CYAN"
    echo
    echo_color "📖 Uso:" "$BLUE"
    echo "  alfredo salud          - Estado del sistema"
    echo "  alfredo wifi           - Info WiFi"
    echo "  alfredo red            - Info de red"
    echo "  alfredo speed          - Velocidad de Internet"
    echo "  alfredo diagnostico    - Diagnóstico completo"
    echo "  alfredo reparar        - Reparación automática"
    echo "  alfredo fix-amd        - Solución específica AMD"
    echo "  alfredo setup-monitors - Configurar monitores"
    echo "  alfredo fix-screen     - Solución rápida pantalla negra"
    echo "  alfredo monitor-screen - Monitorear cambios"
    echo
    echo_color "📌 Para más información:" "$BLUE"
    echo "  alfredo help"
    echo "  cat README.md"
    echo
    echo_color "✅ ¡Alfredo Tools está listo para usar!" "$GREEN"
}

# ============================================
# MAIN SCRIPT
# ============================================

# Procesar argumentos
case "$1" in
    --help|-h)
        show_help
        exit 0
        ;;
    --uninstall)
        show_header
        uninstall
        exit 0
        ;;
esac

# Mostrar header
show_header

# Verificar que estamos en el directorio correcto
if [ ! -f "$PROJECT_DIR/bin/alfredo" ]; then
    echo_color "❌ Error: No se encuentra bin/alfredo en el directorio actual" "$RED"
    echo "   Asegúrate de ejecutar este script desde la raíz del proyecto"
    echo "   Ejecuta: cd ~/Documentos/alfredo-tools && ./install.sh"
    exit 1
fi

# Verificar dependencias
if ! check_dependencies; then
    echo_color "❌ No se puede continuar con la instalación" "$RED"
    exit 1
fi

# Instalar proyecto
install_project

# Crear enlace simbólico
if ! create_symlink; then
    echo_color "❌ Error al crear el enlace simbólico" "$RED"
    exit 1
fi

# Verificar instalación
if ! verify_installation; then
    echo_color "⚠️  La instalación puede estar incompleta" "$YELLOW"
fi

# Mostrar resumen
show_summary

# Sugerencias post-instalación
echo
echo_color "💡 Recomendaciones:" "$YELLOW"
echo "  1. Si tienes AMD: ejecuta 'alfredo fix-amd'"
echo "  2. Configura tus monitores: 'alfredo setup-monitors'"
echo "  3. Ejecuta un diagnóstico: 'alfredo diagnostico'"
echo "  4. Para actualizar: git pull && ./install.sh --force"
