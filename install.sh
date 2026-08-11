#!/bin/bash
# LServer CLI - Instalador Automático de 1 Clic
# Creado por SrxMateo & Lumax Studio

set -e

# Colores Premium
GOLD="\033[38;5;220m"
ORANGE="\033[38;5;208m"
GREEN="\033[1;32m"
RED="\033[1;31m"
CYAN="\033[1;36m"
RESET="\033[0m"

# Función Spinner (Animación de carga elegante)
spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf "  ${CYAN}[%c]${RESET}  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

echo -e "${GOLD}╔════════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${GOLD}║         ⚡ LSERVER CLI INSTALADOR AUTOMÁTICO ⚡                ║${RESET}"
echo -e "${GOLD}╚════════════════════════════════════════════════════════════════╝${RESET}\n"

echo -e "${ORANGE}[1/3] Verificando dependencias del sistema...${RESET}"
{
    if ! command -v git >/dev/null 2>&1; then
        sudo apt-get update -qq && sudo apt-get install git -qq -y
    fi

    if ! command -v pip3 >/dev/null 2>&1; then
        sudo apt-get update -qq && sudo apt-get install python3-pip python3-setuptools -qq -y
    fi
} &
spinner $!
echo -e "  ${GREEN}✔ Dependencias verificadas.${RESET}\n"

echo -e "${ORANGE}[2/3] Descargando la última versión de LServer...${RESET}"
TMP_DIR=$(mktemp -d)
{
    git clone --quiet https://github.com/SrxMateo/LServer.git "$TMP_DIR"
} &
spinner $!
echo -e "  ${GREEN}✔ Descarga completada.${RESET}\n"

echo -e "${ORANGE}[3/3] Compilando e Instalando a nivel global...${RESET}"
cd "$TMP_DIR"
{
    if pip3 install --help | grep -q "break-system-packages"; then
        sudo env PIP_BREAK_SYSTEM_PACKAGES=1 pip3 install --quiet --root-user-action=ignore . --break-system-packages
    else
        sudo pip3 install --quiet --root-user-action=ignore .
    fi
} &
spinner $!
echo -e "  ${GREEN}✔ Instalación global completada.${RESET}\n"

# Limpieza
rm -rf "$TMP_DIR"

echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}║ [ÉXITO] LServer se ha instalado correctamente en tu servidor.  ║${RESET}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${RESET}"
echo -e "${GOLD}Para comenzar, escribe en tu terminal:${RESET} lserver\n"
