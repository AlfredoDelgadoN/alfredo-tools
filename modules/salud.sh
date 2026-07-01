#!/bin/bash

echo
echo "========================================="
echo "        Alfredo Tools - Salud"
echo "========================================="
echo

echo "Sistema : $(grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '"')"
echo "Kernel  : $(uname -r)"
echo "Usuario : $USER"
echo "Equipo  : $(hostname)"
echo "Fecha   : $(date)"

echo
echo "Uso del disco raíz"

df -h / | tail -1

echo
echo "Memoria"

free -h

echo
echo "Estado : OK"
echo
