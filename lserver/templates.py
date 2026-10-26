"""Plantillas predefinidas de start.sh para diferentes tipos de servidor."""

# ─────────────────────────────────────────────────────────────────────────────
# MENÚ PRINCIPAL — categorías que se le presentan al usuario
# ─────────────────────────────────────────────────────────────────────────────
MENU = [
    {
        'key':   'mc',
        'label': '⛏  Minecraft  (Paper, Purpur, Spigot, Vanilla)',
        'sub': [
            ('paper-lobby',    'Paper / Purpur  —  Lobby / Hub         (1G – 3G)'),
            ('paper-survival', 'Paper / Purpur  —  Survival / Minijuegos (1G – 5G)'),
            ('paper-basic',    'Paper / Purpur  —  Básico              (1G – 2G)'),
        ]
    },
    {
        'key':   'proxy',
        'label': '🔀  Proxy Minecraft  (BungeeCord, Velocity)',
        'sub': [
            ('bungeecord', 'BungeeCord  (1G – 2G)'),
            ('velocity',   'Velocity    (1G – 2G)'),
        ]
    },
    {
        'key':   'web',
        'label': '🌐  Proyectos Web / SaaS',
        'sub': [
            ('nodejs',     'Node.js  (node index.js)'),
            ('python',     'Python   (python3 app.py)'),
            ('nextjs',     'Next.js  (npm run build && npm start)'),
            ('react-vite', 'React / Vite  (npm run build + serve)'),
            ('fastapi',    'Python FastAPI  (uvicorn)'),
        ]
    },
    {
        'key':   'other',
        'label': '📦  Otro / Personalizado',
        'sub': [
            ('custom', 'Plantilla vacía — la edito yo mismo'),
        ]
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# BANNER ASCII LUMACRAFT (compartido entre templates de Minecraft)
# ─────────────────────────────────────────────────────────────────────────────
_LUMACRAFT_BANNER = '''\
# =========================================
# ██╗     ██╗   ██╗███╗   ███╗ █████╗  ██████╗██████╗  █████╗ ███████╗████████╗
# ██║     ██║   ██║████╗ ████║██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
# ██║     ██║   ██║██╔████╔██║███████║██║     ██████╔╝███████║█████╗     ██║
# ██║     ██║   ██║██║╚██╔╝██║██╔══██║██║     ██╔══██╗██╔══██║██╔══╝     ██║
# ███████╗╚██████╔╝██║ ╚═╝ ██║██║  ██║╚██████╗██║  ██║██║  ██║██║        ██║
# ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝
#
#           • By SrxMateo & LumaxStudio •
#
# ========================================='''

_AIKAR_FLAGS = '''\
-XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 \\
-XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch \\
-XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M \\
-XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 \\
-XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 \\
-XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 \\
-XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1'''

# ─────────────────────────────────────────────────────────────────────────────
# HELPER — genera el bloque completo de un servidor Minecraft con Paper/Purpur
# ─────────────────────────────────────────────────────────────────────────────
def _mc_template(mem_min, mem_max, label, log_prefix):
    return f'''#!/bin/bash
{_LUMACRAFT_BANNER}

# Configuración del servidor
SERVER_JAR="server.jar"
MEM_MIN="{mem_min}"
MEM_MAX="{mem_max}"

# JVM flags (Aikar's Flags — optimizadas para Paper/Purpur)
JVM_OPTS="{_AIKAR_FLAGS}"

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
  echo -e "${{RED}}❌ No se encontró Java en el sistema.${{RESET}}"
  echo -e "${{YELLOW}}Instálalo con:${{RESET}}"
  echo -e "   sudo apt install openjdk-21-jre-headless -y"
  exit 1
fi

JAVA_VERSION=$($JAVA_PATH -version 2>&1 | awk -F[\\"\\".] '/version/ {{print $2}}')
if [ "$JAVA_VERSION" -lt 21 ]; then
  echo -e "${{RED}}⚠️ Versión de Java insuficiente (necesitas 21 o superior).${{RESET}}"
  exit 1
fi

echo -e "${{GREEN}}✅ Java detectado: $($JAVA_PATH -version 2>&1 | head -n 1)${{RESET}}"

# =========================================
# 🧾 Verificación de archivo y EULA
# =========================================
if [ ! -f "$SERVER_JAR" ]; then
  echo -e "${{RED}}❌ Error: No se encontró $SERVER_JAR${{RESET}}"
  echo -e "${{YELLOW}}Renombra tu .jar a 'server.jar' o edita SERVER_JAR aquí arriba.${{RESET}}"
  exit 1
fi

if [ ! -f eula.txt ]; then
  echo "eula=true" > eula.txt
  echo -e "${{GREEN}}✅ EULA aceptado automáticamente.${{RESET}}"
fi

# =========================================
# 📁 Carpeta de logs
# =========================================
LOG_DIR="logs"
mkdir -p "$LOG_DIR"

# =========================================
# 🔁 Bucle de ejecución infinita (auto-restart)
# =========================================
while true; do
  clear
  echo -e "${{CYAN}}"
  echo "========================================"
  echo "     🚀 Bienvenido a LUMACRAFT 🚀"
  echo "         [ {label} ]"
  echo "========================================"
  echo -e "${{RESET}}"

  LOG_FILE="${{LOG_DIR}}/{log_prefix}_$(date +%Y-%m-%d_%H-%M-%S).log"
  echo -e "${{GREEN}}🚀 Iniciando servidor... (logs → $LOG_FILE)${{RESET}}"

  "$JAVA_PATH" -Xms$MEM_MIN -Xmx$MEM_MAX $JVM_OPTS -jar $SERVER_JAR nogui | tee -a "$LOG_FILE"

  echo -e "${{RED}}🛑 El servidor se ha cerrado.${{RESET}}"
  echo -e "${{YELLOW}}Presiona Ctrl + C ahora para detenerlo permanentemente.${{RESET}}"
  echo -e "${{CYAN}}Reinicio en:${{RESET}}"

  for i in 5 4 3 2 1; do
    echo "$i..."
    sleep 1
  done

  echo -e "${{GREEN}}🔄 Reiniciando servidor...${{RESET}}"
done
'''


# ─────────────────────────────────────────────────────────────────────────────
# TEMPLATES — diccionario principal
# ─────────────────────────────────────────────────────────────────────────────
TEMPLATES = {

    # ── Minecraft: Paper / Purpur ──────────────────────────────────────────
    'paper-lobby': {
        'description': 'Paper/Purpur — Lobby/Hub (1G–3G) Aikar Flags',
        'content': _mc_template('1G', '3G', 'Servidor Lobby', 'lobby'),
    },
    'paper-survival': {
        'description': 'Paper/Purpur — Survival/Minijuegos (1G–5G) Aikar Flags',
        'content': _mc_template('1G', '5G', 'Servidor Survival', 'survival'),
    },
    'paper-basic': {
        'description': 'Paper/Purpur — Básico (1G–2G) Aikar Flags',
        'content': _mc_template('1G', '2G', 'Servidor Minecraft', 'server'),
    },

    # ── Proxy ──────────────────────────────────────────────────────────────
    'bungeecord': {
        'description': 'BungeeCord Proxy (1G–2G)',
        'content': f'''#!/bin/bash
{_LUMACRAFT_BANNER}

# Configuración BungeeCord
PROXY_JAR="BungeeCord.jar"
MEM_MIN="1G"
MEM_MAX="2G"

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
  echo -e "${{RED}}❌ No se encontró Java en el sistema.${{RESET}}"
  echo -e "   sudo apt install openjdk-21-jre-headless -y"
  exit 1
fi

echo -e "${{GREEN}}✅ Java detectado: $($JAVA_PATH -version 2>&1 | head -n 1)${{RESET}}"

if [ ! -f "$PROXY_JAR" ]; then
  echo -e "${{RED}}❌ Error: No se encontró $PROXY_JAR${{RESET}}"
  echo -e "${{YELLOW}}Renombra tu BungeeCord.jar a '$PROXY_JAR' o edita PROXY_JAR.${{RESET}}"
  exit 1
fi

LOG_DIR="logs"
mkdir -p "$LOG_DIR"

# =========================================
# 🔁 Bucle de ejecución con auto-restart
# =========================================
while true; do
  clear
  echo -e "${{CYAN}}"
  echo "========================================"
  echo "   🔀 Bienvenido a LUMACRAFT 🔀"
  echo "       [ BungeeCord Proxy ]"
  echo "========================================"
  echo -e "${{RESET}}"

  LOG_FILE="${{LOG_DIR}}/proxy_$(date +%Y-%m-%d_%H-%M-%S).log"
  echo -e "${{GREEN}}🚀 Iniciando BungeeCord... (logs → $LOG_FILE)${{RESET}}"

  "$JAVA_PATH" -Xms$MEM_MIN -Xmx$MEM_MAX \\
    -XX:+UseG1GC \\
    -XX:G1HeapRegionSize=4M \\
    -XX:+DisableExplicitGC \\
    -XX:+ParallelRefProcEnabled \\
    -XX:+UnlockExperimentalVMOptions \\
    -XX:+AlwaysPreTouch \\
    -jar $PROXY_JAR | tee -a "$LOG_FILE"

  echo -e "${{RED}}🛑 BungeeCord se ha cerrado.${{RESET}}"
  echo -e "${{YELLOW}}Presiona Ctrl + C para detenerlo permanentemente.${{RESET}}"
  echo -e "${{CYAN}}Reinicio en:${{RESET}}"
  for i in 5 4 3 2 1; do echo "$i..."; sleep 1; done
  echo -e "${{GREEN}}🔄 Reiniciando...${{RESET}}"
done
''',
    },

    'velocity': {
        'description': 'Velocity Proxy (1G–2G)',
        'content': f'''#!/bin/bash
{_LUMACRAFT_BANNER}

# Configuración Velocity
PROXY_JAR="velocity.jar"
MEM_MIN="1G"
MEM_MAX="2G"

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
  echo -e "${{RED}}❌ No se encontró Java en el sistema.${{RESET}}"
  echo -e "   sudo apt install openjdk-21-jre-headless -y"
  exit 1
fi

echo -e "${{GREEN}}✅ Java detectado: $($JAVA_PATH -version 2>&1 | head -n 1)${{RESET}}"

if [ ! -f "$PROXY_JAR" ]; then
  echo -e "${{RED}}❌ Error: No se encontró $PROXY_JAR${{RESET}}"
  echo -e "${{YELLOW}}Renombra tu velocity.jar a '$PROXY_JAR' o edita PROXY_JAR.${{RESET}}"
  exit 1
fi

LOG_DIR="logs"
mkdir -p "$LOG_DIR"

# =========================================
# 🔁 Bucle de ejecución con auto-restart
# =========================================
while true; do
  clear
  echo -e "${{CYAN}}"
  echo "========================================"
  echo "   ⚡ Bienvenido a LUMACRAFT ⚡"
  echo "        [ Velocity Proxy ]"
  echo "========================================"
  echo -e "${{RESET}}"

  LOG_FILE="${{LOG_DIR}}/proxy_$(date +%Y-%m-%d_%H-%M-%S).log"
  echo -e "${{GREEN}}🚀 Iniciando Velocity... (logs → $LOG_FILE)${{RESET}}"

  "$JAVA_PATH" -Xms$MEM_MIN -Xmx$MEM_MAX \\
    -XX:+UseG1GC \\
    -XX:G1HeapRegionSize=4M \\
    -XX:+DisableExplicitGC \\
    -XX:+ParallelRefProcEnabled \\
    -XX:+UnlockExperimentalVMOptions \\
    -XX:+AlwaysPreTouch \\
    -jar $PROXY_JAR | tee -a "$LOG_FILE"

  echo -e "${{RED}}🛑 Velocity se ha cerrado.${{RESET}}"
  echo -e "${{YELLOW}}Presiona Ctrl + C para detenerlo permanentemente.${{RESET}}"
  echo -e "${{CYAN}}Reinicio en:${{RESET}}"
  for i in 5 4 3 2 1; do echo "$i..."; sleep 1; done
  echo -e "${{GREEN}}🔄 Reiniciando...${{RESET}}"
done
''',
    },

    # ── Web / SaaS ─────────────────────────────────────────────────────────
    'nodejs': {
        'description': 'Aplicación Node.js',
        'content': '''#!/bin/bash
# =========================================
# Fue creado con mucho amor por SrxMateo & LumaxStudio
# =========================================
echo "🚀 Iniciando aplicación Node.js..."
node index.js
''',
    },
    'python': {
        'description': 'Aplicación Python',
        'content': '''#!/bin/bash
# =========================================
# Fue creado con mucho amor por SrxMateo & LumaxStudio
# =========================================
echo "🚀 Iniciando aplicación Python..."
python3 app.py
''',
    },
    'nextjs': {
        'description': 'Next.js (Producción)',
        'content': '''#!/bin/bash
# =========================================
# Fue creado con mucho amor por SrxMateo & LumaxStudio
# =========================================
echo "🚀 Construyendo e iniciando Next.js en producción..."
npm run build && npm start
''',
    },
    'react-vite': {
        'description': 'React / Vite (build + serve)',
        'content': '''#!/bin/bash
# =========================================
# Fue creado con mucho amor por SrxMateo & LumaxStudio
# =========================================
echo "🚀 Construyendo e iniciando Vite/React..."
npm run build && npx serve -s dist -l 3000
''',
    },
    'fastapi': {
        'description': 'Python FastAPI (uvicorn)',
        'content': '''#!/bin/bash
# =========================================
# Fue creado con mucho amor por SrxMateo & LumaxStudio
# =========================================
echo "🚀 Iniciando servidor FastAPI..."
# pip install fastapi uvicorn  (si no lo tienes)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
''',
    },
    'custom': {
        'description': 'Plantilla vacía (personalizable)',
        'content': '''#!/bin/bash
# =========================================
# Fue creado con mucho amor por SrxMateo & LumaxStudio
# =========================================
echo "Iniciando LServer Nodo..."
# Escribe aquí tu comando de inicio
while true; do sleep 1000; done
''',
    },

    # Aliases heredados (compatibilidad)
    'minecraft':        {'description': 'Alias → paper-basic',    'content': None},
    'lumacraft-basic':  {'description': 'Alias → paper-basic',    'content': None},
    'lumacraft-survival':{'description': 'Alias → paper-survival', 'content': None},
}

# Resolver aliases
TEMPLATES['minecraft']['content']         = TEMPLATES['paper-basic']['content']
TEMPLATES['lumacraft-basic']['content']   = TEMPLATES['paper-basic']['content']
TEMPLATES['lumacraft-survival']['content']= TEMPLATES['paper-survival']['content']


# ─────────────────────────────────────────────────────────────────────────────
# API pública
# ─────────────────────────────────────────────────────────────────────────────
def get_template(template_name):
    t = TEMPLATES.get(template_name)
    return t['content'] if t else None


def list_templates():
    return list(TEMPLATES.keys())


def get_template_description(template_name):
    t = TEMPLATES.get(template_name)
    return t['description'] if t else None


def interactive_template_selector():
    """
    Asistente interactivo que guía al usuario para elegir el tipo de servidor.
    Retorna el nombre de la clave del template elegido, o None si cancela.
    """
    from lserver.ui import (print_menu, GOLD, ORANGE, LIGHT_ORANGE,
                             GRAY, WHITE, GREEN, CYAN, RESET, BOLD, _clean)
    import re

    width = 60
    c = LIGHT_ORANGE

    # ── Paso 1: categoría ──────────────────────────────────────────────────
    cat_options = [(str(i + 1), cat['label']) for i, cat in enumerate(MENU)]
    cat_options.append(('0', 'Cancelar'))
    cat_ans = print_menu(title='¿QUÉ TIPO DE SERVIDOR VAS A USAR?', options=cat_options)

    if cat_ans == '0' or cat_ans is None:
        return None

    try:
        cat_idx = int(cat_ans) - 1
        if cat_idx < 0 or cat_idx >= len(MENU):
            return None
        cat = MENU[cat_idx]
    except (ValueError, IndexError):
        return None

    # ── Paso 2: sub-tipo ──────────────────────────────────────────────────
    sub_options = [(str(i + 1), desc) for i, (_, desc) in enumerate(cat['sub'])]
    sub_options.append(('0', 'Volver atrás'))
    sub_ans = print_menu(title=f'ELIGE EL SUB-TIPO — {cat["label"]}', options=sub_options)

    if sub_ans == '0' or sub_ans is None:
        return interactive_template_selector()  # volver al menú principal

    try:
        sub_idx = int(sub_ans) - 1
        if sub_idx < 0 or sub_idx >= len(cat['sub']):
            return None
        chosen_key, _ = cat['sub'][sub_idx]
    except (ValueError, IndexError):
        return None

    return chosen_key
