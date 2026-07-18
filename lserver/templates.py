"""Plantillas predefinidas de start.sh para diferentes tipos de servidor."""

TEMPLATES = {
    'minecraft': {
        'description': 'Servidor Minecraft con flags Aikar optimizados',
        'content': '''#!/bin/bash
echo "Iniciando servidor Minecraft con flags Aikar..."
java -Xms1G -Xmx4G \\
  -XX:+UseG1GC -XX:+ParallelRefProcEnabled \\
  -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions \\
  -XX:+DisableExplicitGC -XX:+AlwaysPreTouch \\
  -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 \\
  -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 \\
  -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 \\
  -XX:InitiatingHeapOccupancyPercent=15 \\
  -XX:G1MixedGCLiveThresholdPercent=90 \\
  -XX:G1RSetUpdatingPauseTimePercent=5 \\
  -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem \\
  -XX:MaxTenuringThreshold=1 \\
  -jar server.jar nogui
'''
    },
    'nodejs': {
        'description': 'Aplicacion Node.js',
        'content': '''#!/bin/bash
echo "Iniciando aplicacion Node.js..."
node index.js
'''
    },
    'python': {
        'description': 'Aplicacion Python',
        'content': '''#!/bin/bash
echo "Iniciando aplicacion Python..."
python3 app.py
'''
    },
    'custom': {
        'description': 'Plantilla vacia (personalizable)',
        'content': '''#!/bin/bash
echo "Iniciando LServer Nodo..."
# Agrega aqui el comando para iniciar tu servidor
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
