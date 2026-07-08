#!/bin/bash
# LServer CLI - Instalador Automático de 1 Clic
# Creado por SrxMateo & Lumax Studio

set -e

# Colores Premium
GOLD="\033[38;5;220m"
ORANGE="\033[38;5;208m"
GREEN="\033[1;32m"
RED="\033[1;31m"
RESET="\033[0m"

echo -e "${GOLD}╔════════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${GOLD}║         ⚡ LSERVER CLI INSTALADOR AUTOMÁTICO ⚡                ║${RESET}"
echo -e "${GOLD}╚════════════════════════════════════════════════════════════════╝${RESET}"

echo -e "\n${ORANGE}[1/3] Verificando dependencias del sistema...${RESET}"
if ! command -v git >/dev/null 2>&1; then
    echo -e "${RED}Git no está instalado. Instalándolo ahora...${RESET}"
    sudo apt-get update && sudo apt-get install git -y
fi

if ! command -v pip3 >/dev/null 2>&1; then
    echo -e "${RED}Python3-pip no está instalado. Instalándolo ahora...${RESET}"
    sudo apt-get update && sudo apt-get install python3-pip -y
fi

echo -e "\n${ORANGE}[2/3] Descargando la última versión de LServer...${RESET}"
TMP_DIR=$(mktemp -d)
# Clonamos el repositorio oficial
git clone https://github.com/SrxMateo/LServer.git "$TMP_DIR"
cd "$TMP_DIR"

echo -e "\n${ORANGE}[3/3] Compilando e Instalando a nivel global...${RESET}"
# Instalamos la CLI de Python en modo global, forzando la instalación para entornos Linux modernos
if pip3 install --help | grep -q "break-system-packages"; then
    sudo pip3 install . --break-system-packages
else
    sudo pip3 install .
fi

echo -e "\n${GREEN}╔════════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}║ [ÉXITO] LServer se ha instalado correctamente en tu servidor.  ║${RESET}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${RESET}"
echo -e "${GOLD}Para comenzar, escribe en tu terminal:${RESET} lserver\n"

# Limpieza
rm -rf "$TMP_DIR"
