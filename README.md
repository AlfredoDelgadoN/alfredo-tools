# 🛠️ Alfredo Tools

<div align="center">

**Suite de herramientas para diagnóstico y mantenimiento de sistemas**

[![GitHub release](https://img.shields.io/github/v/release/AlfredoDelgadoN/alfredo-tools)](https://github.com/AlfredoDelgadoN/alfredo-tools/releases)
[![GitHub stars](https://img.shields.io/github/stars/AlfredoDelgadoN/alfredo-tools)](https://github.com/AlfredoDelgadoN/alfredo-tools/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/AlfredoDelgadoN/alfredo-tools)](https://github.com/AlfredoDelgadoN/alfredo-tools/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 📋 Índice

- [Características](#-características)
- [Versiones disponibles](#-versiones-disponibles)
- [Instalación](#-instalación)
  - [Linux](#-linux)
  - [Windows](#-windows)
- [Módulos disponibles](#-módulos-disponibles)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Requisitos](#-requisitos)
- [Actualización](#-actualización)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## ✨ Características

- 🚀 **42+ módulos** de diagnóstico y mantenimiento
- 🖥️ **Multiplataforma**: Linux y Windows
- 🎨 **Interfaz visual** con colores y categorías
- 🔧 **Reparación automática** de problemas comunes
- 🌡️ **Monitoreo** de temperatura y rendimiento
- 📊 **Diagnóstico completo** del sistema
- ⚡ **Rápido y ligero** sin dependencias pesadas

---

## 📦 Versiones disponibles

| Sistema | Versión | Estado | Ubicación |
|---------|---------|--------|-----------|
| **🐧 Linux** | Bash | ✅ Estable | `linux/` |
| **🪟 Windows** | Python | ✅ Estable | `windows/` |
| **🪟 Windows (WSL)** | Bash | ✅ Estable | `linux/` |

---

## 🚀 Instalación

### 🐧 Linux

```bash
# Clonar el repositorio
git clone https://github.com/AlfredoDelgadoN/alfredo-tools.git
cd alfredo-tools/linux

# Ejecutar instalador
./install.sh

# ¡Listo! Ahora ejecuta:
alfredo

🪟 Windows
```bash

# Clonar el repositorio
git clone https://github.com/AlfredoDelgadoN/alfredo-tools.git
cd alfredo-tools\windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python alfredo.py salud

🪟 Windows (WSL)
```bash

# Abrir PowerShell como Administrador
Set-ExecutionPolicy Bypass -Scope Process -Force
iex (iwr -useb https://raw.githubusercontent.com/AlfredoDelgadoN/alfredo-tools/main/install.ps1)
