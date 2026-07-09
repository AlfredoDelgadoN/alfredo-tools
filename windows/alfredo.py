#!/usr/bin/env python3
"""
Alfredo Tools - Versión Python para Windows
Módulos: salud, speed, discos, diagnostico, wifi, red, procesador, memoria, temp-cpu
"""

import sys
import os
import platform
import subprocess
import json
import socket
import psutil
from datetime import datetime

# Intentar importar módulos opcionales
try:
    import wmi
    HAS_WMI = True
except ImportError:
    HAS_WMI = False

try:
    import speedtest
    HAS_SPEEDTEST = True
except ImportError:
    HAS_SPEEDTEST = False

# ============================================================
# CLASE PRINCIPAL
# ============================================================

class AlfredoTools:
    def __init__(self):
        self.os_name = platform.system()
        self.os_version = platform.release()
        self.os_build = platform.version()
        self.hostname = platform.node()
        self.architecture = platform.machine()
        self.processor = platform.processor()
        self.is_windows = self.os_name == "Windows"
        self.is_linux = self.os_name == "Linux"
       
        # Colores (usando ANSI para Windows)
        self.GREEN = '\033[92m'
        self.RED = '\033[91m'
        self.YELLOW = '\033[93m'
        self.BLUE = '\033[94m'
        self.CYAN = '\033[96m'
        self.BOLD = '\033[1m'
        self.RESET = '\033[0m'
       
        # Si es Windows y no soporta ANSI, desactivar colores
        if self.is_windows:
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                self.GREEN = self.RED = self.YELLOW = self.BLUE = self.CYAN = self.BOLD = self.RESET = ""
   
    # ============================================================
    # FUNCIONES AUXILIARES
    # ============================================================
   
    def print_header(self, title):
        """Imprime un encabezado formateado"""
        print("\n" + "="*50)
        print(f"        {self.BOLD}{title}{self.RESET}")
        print("="*50)
   
    def print_field(self, label, value):
        """Imprime un campo con formato"""
        print(f"  {self.BOLD}{label}:{self.RESET} {value}")
   
    def get_wmi(self):
        """Obtiene conexión WMI (Windows)"""
        if not self.is_windows:
            return None
        if HAS_WMI:
            return wmi.WMI()
        return None
   
    # ============================================================
    # MÓDULO: SALUD (Estado del sistema)
    # ============================================================
   
    def salud(self):
        """Módulo salud - Estado del sistema"""
        self.print_header("ALFREDO TOOLS - SALUD")
       
        # Información básica
        print(f"{self.CYAN}🖥️  SISTEMA OPERATIVO{self.RESET}")
        print("-"*50)
        print(f"  Sistema: {self.os_name} {self.os_version}")
        print(f"  Hostname: {self.hostname}")
        print(f"  Arquitectura: {self.architecture}")
        print(f"  Procesador: {self.processor or 'No disponible'}")
       
        # Memoria
        mem = psutil.virtual_memory()
        print(f"\n{self.CYAN}💾 MEMORIA{self.RESET}")
        print("-"*50)
        print(f"  Total: {mem.total / (1024**3):.1f} GB")
        print(f"  Usada: {mem.used / (1024**3):.1f} GB ({mem.percent:.1f}%)")
        print(f"  Libre: {mem.free / (1024**3):.1f} GB")
        print(f"  Disponible: {mem.available / (1024**3):.1f} GB")
       
        # CPU
        print(f"\n{self.CYAN}📊 CPU{self.RESET}")
        print("-"*50)
        print(f"  Núcleos: {psutil.cpu_count()}")
        print(f"  Carga: {psutil.cpu_percent(interval=0.5):.1f}%")
       
        # Discos
        print(f"\n{self.CYAN}💿 DISCOS{self.RESET}")
        print("-"*50)
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                print(f"  📀 {partition.device} ({partition.mountpoint})")
                print(f"     {usage.used / (1024**3):.1f} GB / {usage.total / (1024**3):.1f} GB ({usage.percent:.1f}% usado)")
            except:
                pass
       
        # Discos físicos (Windows)
        if self.is_windows and HAS_WMI:
            print(f"\n{self.CYAN}📊 DISCOS FÍSICOS (WMI){self.RESET}")
            print("-"*50)
            w = self.get_wmi()
            if w:
                for disk in w.Win32_DiskDrive():
                    print(f"  📀 {disk.Model}")
                    print(f"     Tamaño: {int(disk.Size) / (1024**3):.1f} GB")
                    print(f"     Interfaz: {disk.InterfaceType}")
                    print(f"     Estado: {disk.Status}")
       
        print(f"\n{self.GREEN}✅ Salud del sistema completada{self.RESET}")
   
    # ============================================================
    # MÓDULO: SPEED (Velocidad de Internet)
    # ============================================================
   
    def speed(self):
        """Módulo speed - Velocidad de Internet"""
        self.print_header("ALFREDO TOOLS - SPEED")
       
        if not HAS_SPEEDTEST:
            print("❌ speedtest no instalado. Ejecuta: pip install speedtest-cli")
            return
       
        print("📊 Ejecutando prueba de velocidad...")
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download = st.download() / 1_000_000
            upload = st.upload() / 1_000_000
            ping = st.results.ping
           
            print(f"\n{self.CYAN}📡 Resultados:{self.RESET}")
            print("-"*50)
            print(f"  Ping: {ping:.2f} ms")
            print(f"  Descarga: {download:.2f} Mbps")
            print(f"  Subida: {upload:.2f} Mbps")
           
            if download > 100:
                print(f"\n{self.GREEN}✅ Conexión MUY BUENA{self.RESET}")
            elif download > 50:
                print(f"\n{self.GREEN}👍 Conexión BUENA{self.RESET}")
            elif download > 20:
                print(f"\n{self.YELLOW}⚠️  Conexión ACEPTABLE{self.RESET}")
            else:
                print(f"\n{self.RED}❌ Conexión LENTA{self.RESET}")
        except Exception as e:
            print(f"❌ Error: {e}")
   
    # ============================================================
    # MÓDULO: DISCOS (Información de discos)
    # ============================================================
   
    def discos(self):
        """Módulo discos - Información de discos"""
        self.print_header("ALFREDO TOOLS - DISCOS")
       
        # Discos físicos (Windows)
        if self.is_windows and HAS_WMI:
            print(f"{self.CYAN}💿 DISCOS FÍSICOS (Windows){self.RESET}")
            print("-"*50)
            w = self.get_wmi()
            if w:
                for disk in w.Win32_DiskDrive():
                    print(f"\n  📀 {disk.Model}")
                    print(f"    Tamaño: {int(disk.Size) / (1024**3):.1f} GB")
                    print(f"    Interfaz: {disk.InterfaceType}")
                    print(f"    Serial: {disk.SerialNumber}")
                    print(f"    Estado: {disk.Status}")
       
        # Particiones
        print(f"\n{self.CYAN}📂 PARTICIONES{self.RESET}")
        print("-"*50)
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                print(f"\n  📀 {partition.device}")
                print(f"    Punto de montaje: {partition.mountpoint}")
                print(f"    Sistema de archivos: {partition.fstype}")
                print(f"    Total: {usage.total / (1024**3):.1f} GB")
                print(f"    Usado: {usage.used / (1024**3):.1f} GB")
                print(f"    Libre: {usage.free / (1024**3):.1f} GB")
                print(f"    Uso: {usage.percent:.1f}%")
            except:
                pass
   
    # ============================================================
    # MÓDULO: DIAGNOSTICO (Diagnóstico completo)
    # ============================================================
   
    def diagnostico(self):
        """Módulo diagnostico - Diagnóstico completo"""
        self.print_header("ALFREDO TOOLS - DIAGNÓSTICO")
       
        problemas = 0
       
        # 1. Memoria
        print(f"\n{self.CYAN}💾 MEMORIA{self.RESET}")
        print("-"*50)
        mem = psutil.virtual_memory()
        print(f"  Total: {mem.total / (1024**3):.1f} GB")
        print(f"  Usado: {mem.percent:.1f}%")
       
        if mem.percent > 90:
            print(f"  {self.RED}❌ CRÍTICO: Memoria casi llena{self.RESET}")
            problemas += 1
        elif mem.percent > 75:
            print(f"  {self.YELLOW}⚠️  ALTO: Cierra aplicaciones{self.RESET}")
            problemas += 1
        else:
            print(f"  {self.GREEN}✅ OK: Memoria suficiente{self.RESET}")
       
        # 2. Disco
        print(f"\n{self.CYAN}💿 DISCO{self.RESET}")
        print("-"*50)
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                print(f"  {partition.device}: {usage.percent:.1f}% usado")
                if usage.percent > 90:
                    print(f"    {self.RED}❌ CRÍTICO: Espacio muy bajo{self.RESET}")
                    problemas += 1
                elif usage.percent > 75:
                    print(f"    {self.YELLOW}⚠️  ALTO: Considera liberar espacio{self.RESET}")
                    problemas += 1
                else:
                    print(f"    {self.GREEN}✅ OK: Espacio suficiente{self.RESET}")
            except:
                pass
       
        # 3. CPU
        print(f"\n{self.CYAN}📊 CPU{self.RESET}")
        print("-"*50)
        cpu_percent = psutil.cpu_percent(interval=0.5)
        print(f"  Carga: {cpu_percent:.1f}%")
        if cpu_percent > 80:
            print(f"  {self.YELLOW}⚠️  Alta carga de CPU{self.RESET}")
            problemas += 1
        else:
            print(f"  {self.GREEN}✅ Carga normal{self.RESET}")
       
        # 4. Procesos que más consumen
        print(f"\n{self.CYAN}🔄 PROCESOS QUE MÁS CONSUMEN{self.RESET}")
        print("-"*50)
        print("  Top 5 por CPU:")
        for proc in sorted(psutil.process_iter(['name', 'cpu_percent', 'memory_percent']),
                          key=lambda p: p.info['cpu_percent'] or 0,
                          reverse=True)[:5]:
            if proc.info['cpu_percent'] and proc.info['cpu_percent'] > 0:
                print(f"    {proc.info['name']}: {proc.info['cpu_percent']:.1f}% CPU")
       
        print("\n  Top 5 por Memoria:")
        for proc in sorted(psutil.process_iter(['name', 'memory_percent']),
                          key=lambda p: p.info['memory_percent'] or 0,
                          reverse=True)[:5]:
            if proc.info['memory_percent'] and proc.info['memory_percent'] > 0:
                print(f"    {proc.info['name']}: {proc.info['memory_percent']:.1f}% MEM")
       
        # 5. Resumen
        print(f"\n{self.CYAN}📋 RESUMEN{self.RESET}")
        print("-"*50)
        if problemas == 0:
            print(f"  {self.GREEN}✅ No se encontraron problemas{self.RESET}")
        else:
            print(f"  {self.YELLOW}⚠️  Se encontraron {problemas} problema(s){self.RESET}")
   
    # ============================================================
    # MÓDULO: WIFI (Información WiFi)
    # ============================================================
   
    def wifi(self):
        """Módulo wifi - Información WiFi"""
        self.print_header("ALFREDO TOOLS - WIFI")
       
        if not self.is_windows:
            print("ℹ️  Este módulo solo funciona en Windows")
            return
       
        try:
            # Usar netsh para obtener información WiFi
            output = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"],
                encoding="utf-8",
                stderr=subprocess.DEVNULL
            )
           
            print(f"{self.CYAN}📡 INTERFACES WiFi{self.RESET}")
            print("-"*50)
           
            # Extraer información
            lines = output.split('\n')
            for line in lines:
                line = line.strip()
                if ':' in line and not line.startswith('---'):
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    if any(k in key for k in ['Nombre', 'SSID', 'Estado', 'BSSID', 'Señal', 'Tipo de radio']):
                        print(f"  {key}: {value}")
           
            # Redes disponibles
            print(f"\n{self.CYAN}📶 REDES DISPONIBLES{self.RESET}")
            print("-"*50)
            try:
                networks = subprocess.check_output(
                    ["netsh", "wlan", "show", "networks"],
                    encoding="utf-8",
                    stderr=subprocess.DEVNULL
                )
                # Mostrar primeras 10 redes
                count = 0
                for line in networks.split('\n'):
                    if 'SSID' in line and ':' in line:
                        ssid = line.split(':', 1)[1].strip()
                        if ssid and count < 10:
                            print(f"  📶 {ssid}")
                            count += 1
                if count == 0:
                    print("  ℹ️  No se encontraron redes")
            except:
                print("  ℹ️  No se pudo escanear redes")
               
        except Exception as e:
            print(f"❌ Error al obtener información WiFi: {e}")
            print("  💡 Verifica que tienes un adaptador WiFi activo")
   
    # ============================================================
    # MÓDULO: RED (Configuración de red)
    # ============================================================
   
    def red(self):
        """Módulo red - Configuración de red"""
        self.print_header("ALFREDO TOOLS - RED")
       
        print(f"{self.CYAN}🌐 INFORMACIÓN DE RED{self.RESET}")
        print("-"*50)
       
        # Interfaces de red
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
       
        for iface, addrs in interfaces.items():
            # Verificar si está activa
            is_up = stats.get(iface, {}).isup if iface in stats else False
            status = "✅ Activa" if is_up else "❌ Inactiva"
           
            # Mostrar información
            print(f"\n  📶 {iface} ({status})")
            for addr in addrs:
                if addr.family == socket.AF_INET:  # IPv4
                    print(f"    IP: {addr.address}")
                    if addr.netmask:
                        print(f"    Máscara: {addr.netmask}")
                elif addr.family == socket.AF_INET6:  # IPv6
                    if not addr.address.startswith('fe80::'):
                        print(f"    IPv6: {addr.address}")
       
        # Gateway predeterminado
        print(f"\n{self.CYAN}🌍 GATEWAY PREDETERMINADO{self.RESET}")
        print("-"*50)
        try:
            # En Windows, obtener gateway con ipconfig
            if self.is_windows:
                output = subprocess.check_output(
                    ["ipconfig"],
                    encoding="utf-8",
                    stderr=subprocess.DEVNULL
                )
                for line in output.split('\n'):
                    if 'Puerta de enlace predeterminada' in line or 'Default Gateway' in line:
                        parts = line.split(':')
                        if len(parts) > 1:
                            gateway = parts[1].strip()
                            if gateway and gateway != '':
                                print(f"  Gateway: {gateway}")
        except:
            print("  ℹ️  No se pudo obtener el gateway")
       
        # Prueba de conectividad
        print(f"\n{self.CYAN}🔗 PRUEBAS DE CONECTIVIDAD{self.RESET}")
        print("-"*50)
       
        try:
            # Ping a Google DNS
            result = subprocess.run(
                ["ping", "-n", "2", "8.8.8.8"],
                capture_output=True,
                encoding="utf-8",
                timeout=5
            )
            if "TTL=" in result.stdout or "tiempo" in result.stdout:
                print(f"  {self.GREEN}✅ Internet: OK{self.RESET}")
            else:
                print(f"  {self.RED}❌ Internet: ERROR{self.RESET}")
        except:
            print(f"  {self.RED}❌ Internet: ERROR{self.RESET}")
   
    # ============================================================
    # MÓDULO: PROCESADOR (Información del procesador)
    # ============================================================
   
    def procesador(self):
        """Módulo procesador - Información del procesador"""
        self.print_header("ALFREDO TOOLS - PROCESADOR")
       
        print(f"{self.CYAN}⚡ INFORMACIÓN DEL PROCESADOR{self.RESET}")
        print("-"*50)
       
        if self.is_windows and HAS_WMI:
            w = self.get_wmi()
            if w:
                for cpu in w.Win32_Processor():
                    print(f"  Modelo: {cpu.Name}")
                    print(f"  Núcleos: {cpu.NumberOfCores}")
                    print(f"  Hilos: {cpu.NumberOfLogicalProcessors}")
                    print(f"  Velocidad: {cpu.MaxClockSpeed} MHz")
                    print(f"  Arquitectura: {cpu.Architecture}")
                    print(f"  Fabricante: {cpu.Manufacturer}")
        else:
            # Fallback con psutil
            print(f"  Procesador: {self.processor or 'No disponible'}")
            print(f"  Núcleos físicos: {psutil.cpu_count(logical=False)}")
            print(f"  Núcleos lógicos: {psutil.cpu_count(logical=True)}")
            print(f"  Carga actual: {psutil.cpu_percent(interval=0.5):.1f}%")
   
    # ============================================================
    # MÓDULO: MEMORIA (Información de memoria)
    # ============================================================
   
    def memoria(self):
        """Módulo memoria - Información de memoria"""
        self.print_header("ALFREDO TOOLS - MEMORIA")
       
        mem = psutil.virtual_memory()
       
        print(f"{self.CYAN}💾 ESTADO DE LA MEMORIA{self.RESET}")
        print("-"*50)
        print(f"  Total: {mem.total / (1024**3):.1f} GB")
        print(f"  Usada: {mem.used / (1024**3):.1f} GB ({mem.percent:.1f}%)")
        print(f"  Libre: {mem.free / (1024**3):.1f} GB")
        print(f"  Disponible: {mem.available / (1024**3):.1f} GB")
       
        # Swap
        swap = psutil.swap_memory()
        if swap.total > 0:
            print(f"\n{self.CYAN}🔄 SWAP{self.RESET}")
            print("-"*50)
            print(f"  Total: {swap.total / (1024**3):.1f} GB")
            print(f"  Usado: {swap.used / (1024**3):.1f} GB ({swap.percent:.1f}%)")
       
        # Procesos que más consumen
        print(f"\n{self.CYAN}📊 PROCESOS QUE MÁS CONSUMEN MEMORIA{self.RESET}")
        print("-"*50)
        for proc in sorted(psutil.process_iter(['name', 'memory_percent']),
                          key=lambda p: p.info['memory_percent'] or 0,
                          reverse=True)[:5]:
            if proc.info['memory_percent'] and proc.info['memory_percent'] > 0:
                print(f"  {proc.info['name']}: {proc.info['memory_percent']:.1f}%")
   
    # ============================================================
    # MÓDULO: TEMP-CPU (Temperatura de CPU)
    # ============================================================
   
    def temp_cpu(self):
        """Módulo temp-cpu - Temperatura de CPU"""
        self.print_header("ALFREDO TOOLS - TEMPERATURA CPU")
       
        if self.is_windows and HAS_WMI:
            print(f"{self.CYAN}🌡️  TEMPERATURA{self.RESET}")
            print("-"*50)
            w = self.get_wmi()
            if w:
                try:
                    # Intentar obtener temperatura desde WMI
                    temps = w.Win32_TemperatureProbe()
                    for temp in temps:
                        if temp.CurrentReading:
                            print(f"  Temperatura: {temp.CurrentReading}°C")
                            break
                except:
                    pass
       
        # Si no hay WMI o no se pudo, mostrar mensaje
        if self.is_linux:
            print("  ℹ️  En Linux usa: alfredo temp-cpu (versión Bash)")
        else:
            print("  ℹ️  La temperatura puede no estar disponible en este sistema")
            print("  💡 Prueba: alfredo diagnostico para más información")
   
    # ============================================================
    # MÓDULO: HELP (Ayuda)
    # ============================================================
   
    def help(self):
        """Muestra la ayuda"""
        print("""
=========================================
          ALFREDO TOOLS v1.0 (Python)
=========================================

📖 COMANDOS DISPONIBLES:

  salud          - Estado del sistema
  speed          - Velocidad de Internet
  discos         - Información de discos
  diagnostico    - Diagnóstico completo
  wifi           - Información WiFi
  red            - Configuración de red
  procesador     - Información del procesador
  memoria        - Información de memoria
  temp-cpu       - Temperatura de CPU
  help           - Esta ayuda

📌 EJEMPLOS:
  alfredo salud
  alfredo speed
  alfredo diagnostico
  alfredo wifi
""")

# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    tools = AlfredoTools()
   
    if len(sys.argv) < 2:
        tools.help()
        sys.exit(0)
   
    command = sys.argv[1].lower()
   
    commands = {
        "salud": tools.salud,
        "speed": tools.speed,
        "discos": tools.discos,
        "diagnostico": tools.diagnostico,
        "wifi": tools.wifi,
        "red": tools.red,
        "procesador": tools.procesador,
        "memoria": tools.memoria,
        "temp-cpu": tools.temp_cpu,
        "help": tools.help,
        "--help": tools.help,
        "-h": tools.help
    }
   
    if command in commands:
        commands[command]()
    else:
        print(f"❌ Comando '{command}' no reconocido")
        print("Ejecuta 'alfredo help' para ver los comandos disponibles")

if __name__ == "__main__":
    main()
