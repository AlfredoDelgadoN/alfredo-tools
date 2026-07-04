# 🛠️ Alfredo Tools

Suite de herramientas para diagnóstico y mantenimiento de sistemas.

## ✨ Características
- 28+ módulos de diagnóstico
- Multiplataforma (Linux, Windows con WSL, macOS)
- Fácil instalación
- Sin dependencias complejas

## 📦 Módulos Disponibles

### 🖥️ Diagnóstico de Sistema
| Módulo | Descripción | Comando |
|--------|-------------|---------|
| `salud` | Estado completo del sistema | `alfredo salud` |
| `diagnostico` | Diagnóstico completo | `alfredo diagnostico` |
| `procesador` | Información del CPU | `alfredo procesador` |
| `memoria` | Información de RAM | `alfredo memoria` |
| `discos` | Información de almacenamiento | `alfredo discos` |

### 🌐 Red y Conectividad
| Módulo | Descripción | Comando |
|--------|-------------|---------|
| `wifi` | Información WiFi | `alfredo wifi` |
| `red` | Configuración de red | `alfredo red` |
| `speed` | Velocidad de Internet | `alfredo speed` |

### 🔧 Reparación y Mantenimiento
| Módulo | Descripción | Comando |
|--------|-------------|---------|
| `reparar` | Reparación automática | `alfredo reparar` |
| `reparar-todo` | Reparación completa | `alfredo reparar-todo` |
| `fix-audio` | Solución de audio | `alfredo fix-audio` |
| `fix-amd` | Solución AMD | `alfredo fix-amd` |

### 🌡️ Monitoreo
| Módulo | Descripción | Comando |
|--------|-------------|---------|
| `temp-cpu` | Temperatura CPU | `alfredo temp-cpu` |
| `temp-discos` | Temperatura discos | `alfredo temp-discos` |

## 🚀 Instalación

### Linux / macOS
```bash
git clone https://github.com/AlfredoDelgadoN/alfredo-tools.git
cd alfredo-tools
./install.sh
