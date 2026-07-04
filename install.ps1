# install.ps1 - Instalador de Alfredo Tools para Windows
# ============================================================
# Este script instala Alfredo Tools en Windows usando WSL 2
# Ejecutar como Administrador
# ============================================================

# Configuración de seguridad
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072

# ============================================================
# 1. VERIFICAR ADMINISTRADOR
# ============================================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     Alfredo Tools - Instalador Windows" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si es administrador
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "❌ Este script debe ejecutarse como Administrador" -ForegroundColor Red
    Write-Host "   Haz clic derecho en PowerShell y selecciona 'Ejecutar como administrador'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Presiona cualquier tecla para salir..."
    Read-Host
    exit 1
}
Write-Host "✅ Ejecutando como Administrador" -ForegroundColor Green

# ============================================================
# 2. VERIFICAR WSL
# ============================================================
Write-Host ""
Write-Host "🔍 Verificando WSL..." -ForegroundColor Blue

# Verificar si WSL está instalado
$wslInstalled = $false
try {
    $wslVersion = wsl --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        $wslInstalled = $true
        Write-Host "✅ WSL instalado" -ForegroundColor Green
    }
} catch {
    $wslInstalled = $false
}

if (-not $wslInstalled) {
    Write-Host "⚠️  WSL no está instalado" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📦 Instalando WSL..." -ForegroundColor Blue
    
    # Instalar WSL
    wsl --install 2>&1 | Out-Host
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error al instalar WSL" -ForegroundColor Red
        Write-Host "   Intenta instalar manualmente:" -ForegroundColor Yellow
        Write-Host "   wsl --install" -ForegroundColor Yellow
        Write-Host ""
        Read-Host "Presiona Enter para salir"
        exit 1
    }
    
    Write-Host "✅ WSL instalado correctamente" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  Se requiere reiniciar para completar la instalación" -ForegroundColor Yellow
    Write-Host "   Después del reinicio, vuelve a ejecutar este script" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para reiniciar"
    Restart-Computer
    exit 0
}

# Verificar versión de WSL
$wslVersionInfo = wsl --status 2>$null
if ($wslVersionInfo -match "2") {
    Write-Host "✅ WSL 2 activo" -ForegroundColor Green
} else {
    Write-Host "⚠️  WSL 1 detectado, configurando WSL 2..." -ForegroundColor Yellow
    wsl --set-default-version 2 2>&1 | Out-Host
}

# ============================================================
# 3. VERIFICAR DISTRIBUCIÓN LINUX
# ============================================================
Write-Host ""
Write-Host "🔍 Verificando distribución Linux..." -ForegroundColor Blue

# Verificar si Ubuntu está instalado
$ubuntuInstalled = $false
try {
    $distros = wsl -l -q 2>$null
    if ($distros -match "Ubuntu") {
        $ubuntuInstalled = $true
        Write-Host "✅ Ubuntu detectado" -ForegroundColor Green
    }
} catch {
    $ubuntuInstalled = $false
}

if (-not $ubuntuInstalled) {
    Write-Host "⚠️  Ubuntu no está instalado en WSL" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📦 Instalando Ubuntu..." -ForegroundColor Blue
    wsl --install -d Ubuntu 2>&1 | Out-Host
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error al instalar Ubuntu" -ForegroundColor Red
        Write-Host "   Intenta instalar manualmente:" -ForegroundColor Yellow
        Write-Host "   wsl --install -d Ubuntu" -ForegroundColor Yellow
        Write-Host ""
        Read-Host "Presiona Enter para salir"
        exit 1
    }
    
    Write-Host "✅ Ubuntu instalado correctamente" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  Se requiere configurar usuario en Ubuntu" -ForegroundColor Yellow
    Write-Host "   Se abrirá una ventana de Ubuntu para configurar usuario y contraseña" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para continuar"
    
    # Abrir Ubuntu para configuración inicial
    ubuntu.exe
}

# ============================================================
# 4. INSTALAR ALFREDO TOOLS
# ============================================================
Write-Host ""
Write-Host "🔧 Instalando Alfredo Tools..." -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Cyan

# Comandos a ejecutar en WSL
$wslCommands = @"
cd /tmp
rm -rf alfredo-tools
git clone https://github.com/AlfredoDelgadoN/alfredo-tools.git
cd alfredo-tools
chmod +x install.sh
./install.sh
"@

# Ejecutar en WSL
Write-Host "📥 Clonando repositorio y ejecutando instalador..." -ForegroundColor Yellow
$wslCommands | wsl -d Ubuntu -u $(whoami) 2>&1 | Out-Host

# ============================================================
# 5. VERIFICAR INSTALACIÓN
# ============================================================
Write-Host ""
Write-Host "✅ Verificando instalación..." -ForegroundColor Blue

# Verificar si alfredo está instalado
$checkCommand = "which alfredo && alfredo version"
$version = $checkCommand | wsl -d Ubuntu -u $(whoami) 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Alfredo Tools instalado correctamente" -ForegroundColor Green
    Write-Host "   Versión: $version" -ForegroundColor Green
} else {
    Write-Host "❌ Error en la instalación" -ForegroundColor Red
    Write-Host "   Intenta ejecutar manualmente:" -ForegroundColor Yellow
    Write-Host "   wsl -d Ubuntu" -ForegroundColor Yellow
    Write-Host "   cd ~/alfredo-tools" -ForegroundColor Yellow
    Write-Host "   ./install.sh" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

# ============================================================
# 6. INSTRUCCIONES DE USO
# ============================================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     ✅ ¡Instalación Completada!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📖 Para usar Alfredo Tools en Windows:" -ForegroundColor Blue
Write-Host ""
Write-Host "1️⃣  Abre Ubuntu desde el menú de inicio" -ForegroundColor Yellow
Write-Host "    O ejecuta: wsl -d Ubuntu" -ForegroundColor Yellow
Write-Host ""
Write-Host "2️⃣  Ejecuta los comandos:" -ForegroundColor Yellow
Write-Host "    alfredo salud          - Estado del sistema" -ForegroundColor White
Write-Host "    alfredo speed          - Velocidad de Internet" -ForegroundColor White
Write-Host "    alfredo diagnostico    - Diagnóstico completo" -ForegroundColor White
Write-Host "    alfredo help           - Ver todos los comandos" -ForegroundColor White
Write-Host ""
Write-Host "3️⃣  Para más información:" -ForegroundColor Blue
Write-Host "    https://github.com/AlfredoDelgadoN/alfredo-tools" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Read-Host "Presiona Enter para finalizar"
