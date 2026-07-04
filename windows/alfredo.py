#!/usr/bin/env python3
"""
Alfredo Tools - Versión Python para Windows
"""

import sys
import os
import platform
import subprocess
import json
from datetime import datetime

# Intentar importar psutil
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("⚠️  psutil no instalado. Instala con: pip install psutil")

class AlfredoTools:
    def __init__(self):
        self.os_name = platform.system()
        self.os_version = platform.release()
        self.hostname = platform.node()
        self.is_windows = self.os_name == "Windows"
        self.is_linux = self.os_name == "Linux"
       
    def get_system_info(self):
        """Obtiene información básica del sistema"""
        info = {
            "SO": f"{self.os_name} {self.os_version}",
            "Hostname": self.hostname,
            "Arquitectura": platform.machine(),
            "Procesador": platform.processor()
        }
       
        if HAS_PSUTIL:
            mem = psutil.virtual_memory()
            info["RAM Total"] = f"{mem.total / (1024**3):.1f} GB"
            info["RAM Usada"] = f"{mem.used / (1024**3):.1f} GB"
            info["RAM Disponible"] = f"{mem.available / (1024**3):.1f} GB"
            info["CPU Carga"] = f"{psutil.cpu_percent(interval=0.5)}%"
            info["Núcleos"] = psutil.cpu_count()
       
        return info
   
    def salud(self):
        """Módulo salud - Estado del sistema"""
        print("\n" + "="*50)
        print("        ALFREDO TOOLS - SALUD")
        print("="*50)
       
        info = self.get_system_info()
        print(f"🖥️  Sistema: {info['SO']}")
        print(f"💻 Hostname: {info['Hostname']}")
        print(f"📐 Arquitectura: {info['Arquitectura']}")
        print(f"⚡ Procesador: {info['Procesador']}")
       
        if HAS_PSUTIL:
            print(f"💾 RAM: {info['RAM Usada']} / {info['RAM Total']}")
            print(f"📊 CPU: {info['CPU Carga']} ({info['Núcleos']} núcleos)")
           
            # Información de disco
            print("\n💿 DISCOS:")
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    print(f"  📀 {partition.device} ({partition.mountpoint})")
                    print(f"     {usage.used / (1024**3):.1f} GB / {usage.total / (1024**3):.1f} GB ({usage.percent}% usado)")
                except:
                    pass
           
            # Información de discos físicos (solo Windows)
            if self.is_windows:
                print("\n📊 DISCOS FÍSICOS (WMI):")
                try:
                    import wmi
                    w = wmi.WMI()
                    for disk in w.Win32_DiskDrive():
                        print(f"  📀 {disk.Model}")
                        print(f"     Tamaño: {int(disk.Size) / (1024**3):.1f} GB")
                        print(f"     Interfaz: {disk.InterfaceType}")
                except ImportError:
                    print("  ℹ️  wmi no instalado (opcional)")
        else:
            print("ℹ️  Instala psutil para más información: pip install psutil")
       
        print("\n✅ Salud del sistema completada")
   
    def speed(self):
        """Módulo speed - Velocidad de Internet"""
        print("\n" + "="*50)
        print("        ALFREDO TOOLS - SPEED")
        print("="*50)
        print("📊 Ejecutando prueba de velocidad...")
       
        try:
            import speedtest
            st = speedtest.Speedtest()
            st.get_best_server()
            download = st.download() / 1_000_000
            upload = st.upload() / 1_000_000
            ping = st.results.ping
           
            print(f"\n📡 Resultados:")
            print(f"  Ping: {ping:.2f} ms")
            print(f"  Descarga: {download:.2f} Mbps")
            print(f"  Subida: {upload:.2f} Mbps")
           
            if download > 100:
                print("\n✅ Conexión MUY BUENA")
            elif download > 50:
                print("\n👍 Conexión BUENA")
            else:
                print("\n⚠️  Conexión LENTA")
        except ImportError:
            print("❌ speedtest no instalado. Ejecuta: pip install speedtest-cli")
        except Exception as e:
            print(f"❌ Error en prueba de velocidad: {e}")
   
    def discos(self):
        """Módulo discos - Información de discos"""
        print("\n" + "="*50)
        print("        ALFREDO TOOLS - DISCOS")
        print("="*50)
       
        if not HAS_PSUTIL:
            print("❌ psutil no instalado. Instala: pip install psutil")
            return
       
        # Discos físicos con WMI (Windows)
        if self.is_windows:
            print("💿 DISCOS FÍSICOS (Windows):")
            try:
                import wmi
                w = wmi.WMI()
                for disk in w.Win32_DiskDrive():
                    print(f"\n📀 {disk.Model}")
                    print(f"  Tamaño: {int(disk.Size) / (1024**3):.1f} GB")
                    print(f"  Interfaz: {disk.InterfaceType}")
                    print(f"  Serial: {disk.SerialNumber}")
                    print(f"  Estado: {disk.Status}")
            except ImportError:
                print("  ℹ️  wmi no instalado")
       
        # Particiones
        print("\n📂 PARTICIONES:")
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                print(f"\n  📀 {partition.device}")
                print(f"    Punto de montaje: {partition.mountpoint}")
                print(f"    Sistema de archivos: {partition.fstype}")
                print(f"    Total: {usage.total / (1024**3):.1f} GB")
                print(f"    Usado: {usage.used / (1024**3):.1f} GB")
                print(f"    Libre: {usage.free / (1024**3):.1f} GB")
                print(f"    Uso: {usage.percent}%")
            except:
                pass
   
    def help(self):
        """Muestra ayuda"""
        print("""
=========================================
          ALFREDO TOOLS v1.0 (Python)
=========================================

Uso:
  python alfredo.py salud          - Estado del sistema
  python alfredo.py speed          - Velocidad de Internet
  python alfredo.py discos         - Información de discos
  python alfredo.py help           - Esta ayuda
""")

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        tools = AlfredoTools()
        tools.help()
        sys.exit(0)
   
    tools = AlfredoTools()
    command = sys.argv[1].lower()
   
    if command == "salud":
        tools.salud()
    elif command == "speed":
        tools.speed()
    elif command == "discos":
        tools.discos()
    elif command == "help" or command == "--help" or command == "-h":
        tools.help()
    else:
        print(f"❌ Comando '{command}' no reconocido")
        print("Ejecuta 'python alfredo.py help' para ver los comandos disponibles")

if __name__ == "__main__":
    main()
