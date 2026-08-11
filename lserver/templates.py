"""Plantillas predefinidas de start.sh para diferentes tipos de servidor."""

TEMPLATES = {
    'lumacraft-survival': {
        'description': 'Lumacraft Survival (1G-5G) - Aikar Flags',
        'content': '''#!/bin/bash
# =========================================
# ██╗      ██╗   ██╗███╗   ███╗ █████╗  ██████╗██████╗  █████╗ ███████╗████████╗
# ██║      ██║   ██║████╗ ████║██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
# ██║      ██║   ██║██╔████╔██║███████║██║     ██████╔╝███████║█████╗     ██║   
# ██║      ██║   ██║██║╚██╔╝██║██╔══██║██║     ██╔══██╗██╔══██║██╔══╝     ██║   
# ███████╗ ╚██████╔╝██║ ╚═╝ ██║██║  ██║╚██████╗██║  ██║██║  ██║██║        ██║   
# ╚══════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   
#
#            • By SrxMateo •
#
# =========================================

# Configuración del servidor SURVIVAL
SERVER_JAR="server.jar"
MEM_MIN="1G"
MEM_MAX="5G"

# JVM flags (Aikar's Flags optimizadas para Paper/Purpur)
JVM_OPTS="-XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 \\
-XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch \\
-XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M \\
-XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 \\
-XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 \\
-XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 \\
-XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1"

# Colores
GREEN="\\033[1;32m"
RED="\\033[1;31m"
YELLOW="\\033[1;33m"
CYAN="\\033[1;36m"
RESET="\\033[0m"

# =========================================
# 🔍 Detección automática de Java
# =========================================
JAVA_PATH=$(which java)

if [ -z "$JAVA_PATH" ]; then
  echo -e "${RED}❌ No se encontró Java en el sistema.${RESET}"
  echo -e "${YELLOW}Instálalo con:${RESET}"
  echo -e "   sudo apt install openjdk-21-jre-headless -y"
  exit 1
fi

JAVA_VERSION=$($JAVA_PATH -version 2>&1 | awk -F[\\".] '/version/ {print $2}')
if [ "$JAVA_VERSION" -lt 21 ]; then
  echo -e "${RED}⚠️ Versión de Java insuficiente (necesitas 21 o superior).${RESET}"
  exit 1
fi

echo -e "${GREEN}✅ Java detectado: $($JAVA_PATH -version 2>&1 | head -n 1)${RESET}"

# =========================================
# 🧾 Verificación de archivo y EULA
# =========================================
if [ ! -f "$SERVER_JAR" ]; then
  echo -e "${RED}❌ Error: No se encontró ${SERVER_JAR}${RESET}"
  echo -e "${YELLOW}Asegúrate de que el archivo se llame exactamente 'server.jar' o 'lobby.jar'.${RESET}"
  exit 1
fi

if [ ! -f eula.txt ]; then
  echo "eula=true" > eula.txt
  echo -e "${GREEN}✅ EULA aceptado automáticamente.${RESET}"
fi

# =========================================
# 📁 Carpeta de logs
# =========================================
LOG_DIR="logs"
mkdir -p "$LOG_DIR"

# =========================================
# 🔁 Bucle de ejecución infinita
# =========================================
while true; do
  clear
  echo -e "${CYAN}"
  echo "========================================"
  echo "     🚀 Bienvenido a LUMACRAFT 🚀"
  echo "         [ Servidor Survival ]"
  echo "========================================"
  echo -e "${RESET}"

  LOG_FILE="${LOG_DIR}/server_$(date +%Y-%m-%d_%H-%M-%S).log"
  echo -e "${GREEN}🚀 Iniciando servidor... (logs → $LOG_FILE)${RESET}"

  "$JAVA_PATH" -Xms$MEM_MIN -Xmx$MEM_MAX $JVM_OPTS -jar $SERVER_JAR nogui | tee -a "$LOG_FILE"

  echo -e "${RED}🛑 El servidor se ha cerrado.${RESET}"
  echo -e "${YELLOW}Presiona Ctrl + C ahora si deseas detenerlo permanentemente.${RESET}"
  echo -e "${CYAN}Reinicio en:${RESET}"

  for i in 5 4 3 2 1; do
    echo "$i..."
    sleep 1
  done

  echo -e "${GREEN}🔄 Reiniciando servidor...${RESET}"
done
'''
    },
    'lumacraft-basic': {
        'description': 'Lumacraft Básico (1G-2G) - Optimizado',
        'content': '''#!/bin/bash
# =========================================
# ██╗     ██╗   ██╗███╗   ███╗ █████╗  ██████╗██████╗  █████╗ ███████╗████████╗
# ██║     ██║   ██║████╗ ████║██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
# ██║     ██║   ██║██╔████╔██║███████║██║     ██████╔╝███████║█████╗     ██║   
# ██║     ██║   ██║██║╚██╔╝██║██╔══██║██║     ██╔══██╗██╔══██║██╔══╝     ██║   
# ███████╗╚██████╔╝██║ ╚═╝ ██║██║  ██║╚██████╗██║  ██║██║  ██║██║        ██║   
# ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   
#
#           • By SrxMateo •
#
# =========================================

# Configuración del servidor
SERVER_JAR="server.jar"
MEM_MIN="1G"
MEM_MAX="2G"

# JVM flags (rendimiento optimizado para Paper/Spigot)
JVM_OPTS="-XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 \\
-XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch \\
-XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M \\
-XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 \\
-XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 \\
-XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 \\
-XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1"

# Colores
GREEN="\\033[1;32m"
RED="\\033[1;31m"
YELLOW="\\033[1;33m"
CYAN="\\033[1;36m"
RESET="\\033[0m"

# =========================================
# 🔍 Detección automática de Java
# =========================================
JAVA_PATH=$(which java)

if [ -z "$JAVA_PATH" ]; then
  echo -e "${RED}❌ No se encontró Java en el sistema.${RESET}"
  echo -e "${YELLOW}Instálalo con:${RESET}"
  echo -e "   sudo apt install openjdk-21-jre -y"
  exit 1
fi

JAVA_VERSION=$($JAVA_PATH -version 2>&1 | awk -F[\\".] '/version/ {print $2}')
if [ "$JAVA_VERSION" -lt 21 ]; then
  echo -e "${RED}⚠️ Versión de Java insuficiente (necesitas 21 o superior).${RESET}"
  exit 1
fi

echo -e "${GREEN}✅ Java detectado: $($JAVA_PATH -version 2>&1 | head -n 1)${RESET}"

# =========================================
# 🧾 Verificación de archivo y EULA
# =========================================
if [ ! -f "$SERVER_JAR" ]; then
  echo -e "${RED}❌ Error: No se encontró ${SERVER_JAR}${RESET}"
  exit 1
fi

if [ ! -f eula.txt ]; then
  echo "eula=true" > eula.txt
  echo -e "${GREEN}✅ EULA aceptado automáticamente.${RESET}"
fi

# =========================================
# 📁 Carpeta de logs
# =========================================
LOG_DIR="logs"
mkdir -p "$LOG_DIR"

# =========================================
# 🔁 Bucle de ejecución infinita
# =========================================
while true; do
  clear
  echo -e "${CYAN}"
  echo "========================================"
  echo "     🚀 Bienvenido a LUMACRAFT 🚀"
  echo "========================================"
  echo -e "${RESET}"

  LOG_FILE="${LOG_DIR}/server_$(date +%Y-%m-%d_%H-%M-%S).log"
  echo -e "${GREEN}🚀 Iniciando servidor... (logs → $LOG_FILE)${RESET}"

  "$JAVA_PATH" -Xms$MEM_MIN -Xmx$MEM_MAX $JVM_OPTS -jar $SERVER_JAR nogui | tee -a "$LOG_FILE"

  echo -e "${RED}🛑 El servidor se ha cerrado.${RESET}"
  echo -e "${YELLOW}Presiona Ctrl + C ahora si deseas detenerlo permanentemente.${RESET}"
  echo -e "${CYAN}Reinicio en:${RESET}"

  for i in 5 4 3 2 1; do
    echo "$i..."
    sleep 1
  done

  echo -e "${GREEN}🔄 Reiniciando servidor...${RESET}"
done
'''
    },
    'minecraft': {
        'description': 'Minecraft Básico (Vanilla)',
        'content': '''#!/bin/bash
java -Xms1G -Xmx4G -jar server.jar nogui
'''
    },
    'nodejs': {
        'description': 'Aplicación Node.js Básico',
        'content': '''#!/bin/bash
# =========================================
# Fue creado con mucho amor por SrxMateo & LumaxStudio
# =========================================
echo "Iniciando aplicacion Node.js..."
node index.js
'''
    },
    'python': {
        'description': 'Aplicación Python Básico',
        'content': '''#!/bin/bash
# =========================================
# Fue creado con mucho amor por SrxMateo & LumaxStudio
# =========================================
echo "Iniciando aplicacion Python..."
python3 app.py
'''
    },
    'nextjs': {
        'description': 'Next.js (Producción)',
        'content': '''#!/bin/bash
# =========================================
# Fue creado con mucho amor por SrxMateo & LumaxStudio
# =========================================
echo "Construyendo e iniciando Next.js en Producción..."
npm run build && npm start
'''
    },
    'react-vite': {
        'description': 'React / Vite (Producción Estática)',
        'content': '''#!/bin/bash
# =========================================
# Fue creado con mucho amor por SrxMateo & LumaxStudio
# =========================================
echo "Construyendo e iniciando Vite/React..."
npm run build && npx serve -s dist -l 3000
'''
    },
    'fastapi': {
        'description': 'Python FastAPI (Web API)',
        'content': '''#!/bin/bash
# =========================================
# Fue creado con mucho amor por SrxMateo & LumaxStudio
# =========================================
echo "Iniciando servidor FastAPI..."
# Instala fastapi y uvicorn si no lo tienes: pip install fastapi uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
'''
    },
    'custom': {
        'description': 'Plantilla vacía (personalizable)',
        'content': '''#!/bin/bash
# =========================================
# Fue creado con mucho amor por SrxMateo & LumaxStudio
# =========================================
echo "Iniciando LServer Nodo..."
while true; do sleep 1000; done
'''
    }
}

def get_template(template_name):
    t = TEMPLATES.get(template_name)
    if t:
        return t['content']
    return None

def list_templates():
    return list(TEMPLATES.keys())

def get_template_description(template_name):
    t = TEMPLATES.get(template_name)
    if t:
        return t['description']
    return None
