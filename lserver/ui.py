import sys
import os
import re
# Codigos ANSI para colores
GOLD = "\033[38;5;220m"
ORANGE = "\033[38;5;208m"
LIGHT_ORANGE = "\033[38;5;214m"
YELLOW = "\033[38;5;226m"
GREEN = "\033[1;32m"
DARK_GREEN = "\033[38;5;34m"
BLUE = "\033[1;34m"
RED = "\033[1;31m"
DARK_RED = "\033[38;5;196m"
CYAN = "\033[36m"
GRAY = "\033[90m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

BG_GREEN   = "\033[48;5;22m"
BG_RED     = "\033[48;5;52m"
BG_ORANGE  = "\033[48;5;130m"
BG_GRAY    = "\033[48;5;236m"

def print_dashboard(nodes, is_running_func):
    from lserver.core import get_node_resources, get_node_ports, get_current_uptime, format_uptime
    
    colors = [226, 220, 214, 208, 202, 196]
    c_border = LIGHT_ORANGE
    
    def print_box_line(text, visual_length=None):
        if visual_length is None:
            import re
            clean_text = re.sub(r'\033\[[0-9;]*m', '', text)
            visual_length = len(clean_text)
        padding = 78 - visual_length
        if padding < 0: padding = 0
        print(f"{c_border}║{RESET}{text}{' ' * padding}{c_border}║{RESET}")
    
    print(f"{c_border}╔══════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{c_border}║                                                                              ║{RESET}")
    
    ascii_art = [
        "   ██╗     ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗   ",
        "   ██║     ██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗  ",
        "   ██║     ███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝  ",
        "   ██║     ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗  ",
        "   ███████╗███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║  ",
        "   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝  "
    ]
    
    for i, line in enumerate(ascii_art):
        color = f"\033[38;5;{colors[i]}m"
        print(f"{c_border}║{RESET}{color}        {line}        {RESET}{c_border}║{RESET}")
        
    print(f"{c_border}║                                                                              ║{RESET}")
    credits = "⚡ Hecho por SrxMateo & Lumax Studio ⚡"
    pad = (78 - len(credits)) // 2
    credits_line = (" " * pad) + credits + (" " * (78 - len(credits) - pad))
    print(f"{c_border}║{RESET}\033[38;5;226m{credits_line}{RESET}{c_border}║{RESET}")
    print(f"{c_border}╠══════════════════════════════════════════════════════════════════════════════╣{RESET}")
    
    from lserver.state import get_setting
    lang = get_setting('language') or 'es'
    
    t = {
        'es': {
            'options': 'OPCIONES DISPONIBLES:', 'nodes': 'ESTADO DE LOS NODOS', 'no_nodes': 'No hay nodos creados. Usa: lserver -c <nombre>',
            'p': 'Encender el servidor y mantenerlo 24/7.', 'd': 'Detener el nodo de forma segura.', 'k': 'Matar el proceso del servidor (forzado).',
            'c': 'Crear un nodo (carpeta y config).', 'x': 'Borrar el nodo y su directorio.', 'a': 'Alternar Auto-Heal (Watchdog).',
            'b': 'Opciones de Backup (Manual/Automatico).', 'r': 'Reinicio programado diario.', 'e': 'Consola interactiva (Ctrl+C para salir).',
            'o': 'Editar el start.sh del nodo.', 'g': 'Gestionar grupos de nodos.', 'w': 'Configurar alertas Discord/Telegram.',
            'ds': 'Arranca el vigilante en background.', 'd_stop': 'Detiene el vigilante.', 'ws': 'Abre el panel web privado.',
            'u': 'Buscar actualizaciones de LServer.', 't': 'Cambiar idioma interactivo (es/en/pt/fr).', 'l': 'Mostrar Dashboard con nodos creados.',
            'v': 'Mostrar la version de LServer.',
            'h_status': 'Status', 'h_node': 'Nodo', 'h_port': 'Puerto'
        },
        'en': {
            'options': 'AVAILABLE OPTIONS:', 'nodes': 'NODES STATUS', 'no_nodes': 'No nodes created. Use: lserver -c <name>',
            'p': 'Start server and keep it online 24/7.', 'd': 'Stop the node safely.', 'k': 'Kill the server process (force).',
            'c': 'Create a new node (folder and config).', 'x': 'Delete the node and its directory.', 'a': 'Toggle Auto-Heal (Watchdog).',
            'b': 'Backup options (Manual/Automatic).', 'r': 'Daily scheduled restart.', 'e': 'Interactive console (Ctrl+C to exit).',
            'o': "Edit node's start.sh.", 'g': 'Manage node groups.', 'w': 'Configure Discord/Telegram alerts.',
            'ds': 'Start the background watcher.', 'd_stop': 'Stop the watcher.', 'ws': 'Open the private web panel.',
            'u': 'Check for LServer updates.', 't': 'Interactive language change (es/en/pt/fr).', 'l': 'Show Dashboard with created nodes.',
            'v': 'Show LServer version.',
            'h_status': 'Status', 'h_node': 'Node', 'h_port': 'Port'
        },
        'pt': {
            'options': 'OPÇÕES DISPONÍVEIS:', 'nodes': 'STATUS DOS NÓS', 'no_nodes': 'Nenhum nó criado. Use: lserver -c <nome>',
            'p': 'Iniciar servidor e manter online 24/7.', 'd': 'Parar o nó com segurança.', 'k': 'Matar o processo (forçar).',
            'c': 'Criar um novo nó (pasta e config).', 'x': 'Apagar o nó e seu diretório.', 'a': 'Alternar Auto-Heal (Watchdog).',
            'b': 'Opções de Backup (Manual/Auto).', 'r': 'Reinício programado diário.', 'e': 'Console interativo (Ctrl+C para sair).',
            'o': 'Editar start.sh do nó.', 'g': 'Gerenciar grupos de nós.', 'w': 'Configurar alertas Discord/Telegram.',
            'ds': 'Iniciar o vigilante em background.', 'd_stop': 'Parar o vigilante.', 'ws': 'Abrir o painel web privado.',
            'u': 'Buscar atualizações do LServer.', 't': 'Mudar idioma interativo (es/en/pt/fr).', 'l': 'Mostrar Dashboard com nós criados.',
            'v': 'Mostrar a versão do LServer.',
            'h_status': 'Status', 'h_node': 'Nó', 'h_port': 'Porta'
        },
        'fr': {
            'options': 'OPTIONS DISPONIBLES:', 'nodes': 'STATUT DES NŒUDS', 'no_nodes': 'Aucun nœud créé. Utilisez: lserver -c <nom>',
            'p': 'Démarrer le serveur (24/7).', 'd': 'Arrêter le nœud en toute sécurité.', 'k': 'Tuer le processus (forcer).',
            'c': 'Créer un nouveau nœud (dossier et config).', 'x': 'Supprimer le nœud et son répertoire.', 'a': 'Basculer Auto-Heal (Watchdog).',
            'b': 'Options de sauvegarde (Manuel/Auto).', 'r': 'Redémarrage quotidien programmé.', 'e': 'Console interactive (Ctrl+C pour quitter).',
            'o': 'Modifier le start.sh du nœud.', 'g': 'Gérer les groupes de nœuds.', 'w': 'Configurer alertes Discord/Telegram.',
            'ds': 'Démarrer le watcher.', 'd_stop': 'Arrêter le watcher.', 'ws': 'Ouvrir le panneau web privé.',
            'u': 'Vérifier les mises à jour LServer.', 't': 'Changement de langue interactif.', 'l': 'Afficher le Dashboard avec les nœuds.',
            'v': 'Afficher la version de LServer.',
            'h_status': 'Statut', 'h_node': 'Nœud', 'h_port': 'Port'
        }
    }
    _t = t.get(lang, t['es'])

    print_box_line(f" {YELLOW}{_t['options']}{RESET}")
    print_box_line(f"  {GOLD}lserver -p <nodo>{RESET}    {ORANGE}{_t['p']}{RESET}")
    print_box_line(f"  {GOLD}lserver -d <nodo>{RESET}    {ORANGE}{_t['d']}{RESET}")
    print_box_line(f"  {GOLD}lserver -k <nodo>{RESET}    {ORANGE}{_t['k']}{RESET}")
    print_box_line(f"  {GOLD}lserver -c <nodo>{RESET}    {ORANGE}{_t['c']}{RESET}")
    print_box_line(f"  {GOLD}lserver -x <nodo>{RESET}    {ORANGE}{_t['x']}{RESET}")
    print_box_line(f"  {GOLD}lserver -a <nodo>{RESET}    {ORANGE}{_t['a']}{RESET}")
    print_box_line(f"  {GOLD}lserver -b <nodo>{RESET}    {ORANGE}{_t['b']}{RESET}")
    print_box_line(f"  {GOLD}lserver -r <nodo> HH:MM{RESET} {ORANGE}{_t['r']}{RESET}")
    print_box_line(f"  {GOLD}lserver -e <nodo>{RESET}    {ORANGE}{_t['e']}{RESET}")
    print_box_line(f"  {GOLD}lserver -o <nodo>{RESET}    {ORANGE}{_t['o']}{RESET}")
    print_box_line(f"  {GOLD}lserver group{RESET}        {ORANGE}{_t['g']}{RESET}")
    print_box_line(f"  {GOLD}lserver webhook{RESET}      {ORANGE}{_t['w']}{RESET}")
    print_box_line(f"  {GOLD}lserver daemon start{RESET} {ORANGE}{_t['ds']}{RESET}")
    print_box_line(f"  {GOLD}lserver daemon stop{RESET}  {ORANGE}{_t['d_stop']}{RESET}")
    print_box_line(f"  {GOLD}lserver web start{RESET}    {ORANGE}{_t['ws']}{RESET}")
    print_box_line(f"  {GOLD}lserver update{RESET}       {ORANGE}{_t['u']}{RESET}")
    print_box_line(f"  {GOLD}lserver -t [lang]{RESET}    {ORANGE}{_t['t']}{RESET}")
    print_box_line(f"  {GOLD}lserver -l{RESET}           {ORANGE}{_t['l']}{RESET}")
    print_box_line(f"  {GOLD}lserver -v{RESET}           {ORANGE}{_t['v']}{RESET}")
    print(f"{c_border}╠══════════════════════════════════════════════════════════════════════════════╣{RESET}")

    print_box_line(f" {YELLOW}{_t['nodes']}{RESET}")
    
    hdr = f"  {GOLD}{_t['h_status']:<10}{RESET} {GOLD}{_t['h_node']:<14}{RESET} {GOLD}{'CPU':>5}{RESET} {GOLD}{'RAM':>6}{RESET} {GOLD}{_t['h_port']:>8}{RESET} {GOLD}{'Uptime':>10}{RESET}"
    print_box_line(hdr)
    sep_line = f"  {LIGHT_ORANGE}{'─'*74}{RESET}"
    print_box_line(sep_line)

    if not nodes:
        print_box_line(f"  {GRAY}{_t['no_nodes']}{RESET}")
    else:
        for name, data in nodes.items():
            running = is_running_func(name)
            
            # Status
            if running:
                status = f"{GREEN}● ONLINE{RESET} "
            else:
                status = f"{RED}× OFFLINE{RESET}"
            
            # Iconos
            heal_icon = "❤" if data.get('is_critical') else " "
            backup_icon = "💾" if data.get('backup_enabled') else " "
            
            # Nombre con iconos
            node_display = f"{heal_icon}{backup_icon}{name}"
            if len(node_display) > 14:
                node_display = node_display[:11] + "..."
            
            if running:
                # Obtener PID para recursos
                pid_file_path = None
                node_info = get_node_func_safe(name, data)
                if node_info:
                    pid_file = os.path.join(data['path'], 'server.pid')
                    try:
                        with open(pid_file, 'r') as f:
                            pid = int(f.read().strip())
                        res = get_node_resources(pid)
                        ports = get_node_ports(pid)
                    except Exception:
                        res = {'cpu': '—', 'ram': '—'}
                        ports = '—'
                else:
                    res = {'cpu': '—', 'ram': '—'}
                    ports = '—'
                
                uptime_secs = get_current_uptime(name)
                uptime_str = format_uptime(uptime_secs)
            else:
                res = {'cpu': '—', 'ram': '—'}
                ports = '—'
                total_up = data.get('total_uptime', 0) or 0
                uptime_str = format_uptime(total_up) if total_up > 0 else '—'
            
            # Truncar puerto si es muy largo
            if len(ports) > 8:
                ports = ports[:7] + "…"
            if len(uptime_str) > 10:
                uptime_str = uptime_str[:9] + "…"
            
            row = f"  {status} {GOLD}{node_display:<14}{RESET} {CYAN}{res['cpu']:>5}{RESET} {CYAN}{res['ram']:>6}{RESET} {ORANGE}{ports:>8}{RESET} {WHITE}{uptime_str:>10}{RESET}"
            print_box_line(row)

    print(f"{c_border}╚══════════════════════════════════════════════════════════════════════════════╝{RESET}")
    print("")

def get_node_func_safe(name, data):
    """Helper seguro para obtener info del nodo."""
    import os
    pid_file = os.path.join(data.get('path', ''), 'server.pid')
    if os.path.exists(pid_file):
        return True
    return False

def print_wiki():
    """Wiki interactiva multi-idioma de LServer."""
    from lserver.state import get_setting
    lang = get_setting('language') or 'es'

    W = 78
    c = LIGHT_ORANGE

    def line(text=""):
        clean = re.sub(r'\033\[[0-9;]*m', '', text)
        pad = W - len(clean)
        print(f"{c}║{RESET}{text}{' ' * max(0, pad)}{c}║{RESET}")

    def sep():
        print(f"{c}╠{'═' * W}╣{RESET}")

    def blank():
        print(f"{c}║{RESET}{' ' * W}{c}║{RESET}")

    # ─── Traducciones ────────────────────────────────────────────────────
    T = {
        'es': {
            'title':    '🔥  LSERVER — WIKI Y MANUAL DE USUARIO  🔥',
            's1':  '📦  1. GESTIÓN BÁSICA DE NODOS',
            'c1':  [
                ('lserver -c <nombre>',          'Crear nodo  (ej: lserver -c lobby)'),
                ('lserver -c <nombre> --template minecraft', 'Crear con plantilla Java/Minecraft'),
                ('lserver -p <nombre>',          'Encender el nodo (keep-alive 24/7)'),
                ('lserver -d <nombre>',          'Detener el nodo de forma segura'),
                ('lserver -k <nombre>',          'Forzar cierre inmediato (kill)'),
                ('lserver -e <nombre>',          'Entrar a la consola interactiva'),
                ('lserver -o <nombre>',          'Editar el start.sh del nodo'),
                ('lserver -x <nombre>',          'Borrar el nodo (pregunta por la carpeta)'),
            ],
            's2':  '👥  2. SISTEMA DE GRUPOS',
            'c2':  [
                ('lserver group',                'Abrir menú interactivo de grupos'),
                ('lserver group list',           'Ver grupos + estado ONLINE/OFFLINE'),
                ('lserver group create prod',    'Crear grupo llamado "prod"'),
                ('lserver group add prod lobby', 'Agregar nodo "lobby" al grupo "prod"'),
                ('lserver group remove prod hub','Quitar "hub" del grupo (no borra nada)'),
                ('lserver group start prod',     'Encender TODOS los nodos del grupo'),
                ('lserver group stop  prod',     'Apagar  TODOS los nodos del grupo'),
                ('lserver group delete prod',    'Eliminar el grupo (nodos NO se borran)'),
            ],
            's3':  '⚙️   3. AUTOMATIZACIÓN Y FUNCIONES AVANZADAS',
            'c3':  [
                ('lserver -a <nombre>',          'Auto-Heal ❤  — revive si crashea'),
                ('lserver -r <nombre> 04:00',    'Reinicio diario a las 04:00 AM'),
                ('lserver -b <nombre>',          'Menú de backups (manual o automático)'),
                ('lserver daemon start',         'Activar vigilante 24/7 en background'),
                ('lserver daemon stop',          'Detener el vigilante'),
                ('lserver web start 9090',       'Panel web privado en http://IP:9090'),
                ('lserver web password',         'Configurar usuario y contraseña del panel'),
                ('lserver update',               'Actualizar LServer desde GitHub'),
                ('lserver -t',                   'Cambiar idioma (es / en / pt / fr)'),
            ],
            's4':  '🔔  4. ALERTAS WEBHOOK (DISCORD / TELEGRAM)',
            'c4':  [
                ('lserver webhook set <URL>',    'Guardar URL del webhook'),
                ('lserver webhook test',         'Enviar alerta de prueba'),
                ('lserver webhook status',       'Ver si hay webhook configurado'),
                ('lserver webhook remove',       'Eliminar el webhook guardado'),
            ],
            's5':  '💡  5. GUÍA RÁPIDA — PRIMER USO',
            'qs': [
                '1.  lserver -c miservidor            # Crea el nodo',
                '2.  lserver -o miservidor            # Edita start.sh con tu comando',
                '3.  lserver -p miservidor            # Lo enciende y lo mantiene vivo',
                '4.  lserver -e miservidor            # Entra a su consola',
                '5.  lserver daemon start             # Activa Auto-Heal y reinicios',
            ],
        },
        'en': {
            'title':    '🔥  LSERVER — WIKI & USER MANUAL  🔥',
            's1':  '📦  1. BASIC NODE MANAGEMENT',
            'c1':  [
                ('lserver -c <name>',            'Create node  (e.g. lserver -c lobby)'),
                ('lserver -c <name> --template minecraft', 'Create with Java/Minecraft template'),
                ('lserver -p <name>',            'Start the node (24/7 keep-alive)'),
                ('lserver -d <name>',            'Stop the node safely'),
                ('lserver -k <name>',            'Force kill (immediate)'),
                ('lserver -e <name>',            'Open interactive console'),
                ('lserver -o <name>',            "Edit node's start.sh"),
                ('lserver -x <name>',            'Delete node (asks about folder)'),
            ],
            's2':  '👥  2. GROUP SYSTEM',
            'c2':  [
                ('lserver group',                'Open interactive groups menu'),
                ('lserver group list',           'Show groups + ONLINE/OFFLINE status'),
                ('lserver group create prod',    'Create group named "prod"'),
                ('lserver group add prod lobby', 'Add node "lobby" to group "prod"'),
                ('lserver group remove prod hub','Remove "hub" from group (no delete)'),
                ('lserver group start prod',     'Start ALL nodes in the group'),
                ('lserver group stop  prod',     'Stop  ALL nodes in the group'),
                ('lserver group delete prod',    'Delete group (nodes are NOT deleted)'),
            ],
            's3':  '⚙️   3. AUTOMATION & ADVANCED FEATURES',
            'c3':  [
                ('lserver -a <name>',            'Auto-Heal ❤  — revives on crash'),
                ('lserver -r <name> 04:00',      'Daily restart at 04:00 AM'),
                ('lserver -b <name>',            'Backup menu (manual or automatic)'),
                ('lserver daemon start',         'Enable 24/7 background watcher'),
                ('lserver daemon stop',          'Stop the watcher'),
                ('lserver web start 9090',       'Private web panel at http://IP:9090'),
                ('lserver web password',         'Set web panel user & password'),
                ('lserver update',               'Update LServer from GitHub'),
                ('lserver -t',                   'Change language (es / en / pt / fr)'),
            ],
            's4':  '🔔  4. WEBHOOK ALERTS (DISCORD / TELEGRAM)',
            'c4':  [
                ('lserver webhook set <URL>',    'Save webhook URL'),
                ('lserver webhook test',         'Send a test alert'),
                ('lserver webhook status',       'Check if webhook is configured'),
                ('lserver webhook remove',       'Remove saved webhook'),
            ],
            's5':  '💡  5. QUICK START GUIDE',
            'qs': [
                '1.  lserver -c myserver              # Create the node',
                '2.  lserver -o myserver              # Edit start.sh with your command',
                '3.  lserver -p myserver              # Start it and keep it alive',
                '4.  lserver -e myserver              # Open its console',
                '5.  lserver daemon start             # Enable Auto-Heal & restarts',
            ],
        },
        'pt': {
            'title':    '🔥  LSERVER — WIKI E MANUAL DO USUÁRIO  🔥',
            's1':  '📦  1. GESTÃO BÁSICA DE NÓS',
            'c1':  [
                ('lserver -c <nome>',            'Criar nó  (ex: lserver -c lobby)'),
                ('lserver -c <nome> --template minecraft', 'Criar com template Java/Minecraft'),
                ('lserver -p <nome>',            'Iniciar o nó (keep-alive 24/7)'),
                ('lserver -d <nome>',            'Parar o nó com segurança'),
                ('lserver -k <nome>',            'Forçar encerramento (kill)'),
                ('lserver -e <nome>',            'Abrir console interativo'),
                ('lserver -o <nome>',            'Editar o start.sh do nó'),
                ('lserver -x <nome>',            'Apagar o nó (pergunta sobre a pasta)'),
            ],
            's2':  '👥  2. SISTEMA DE GRUPOS',
            'c2':  [
                ('lserver group',                'Abrir menu interativo de grupos'),
                ('lserver group list',           'Ver grupos + status ONLINE/OFFLINE'),
                ('lserver group create prod',    'Criar grupo chamado "prod"'),
                ('lserver group add prod lobby', 'Adicionar "lobby" ao grupo "prod"'),
                ('lserver group remove prod hub','Remover "hub" do grupo (sem apagar)'),
                ('lserver group start prod',     'Iniciar TODOS os nós do grupo'),
                ('lserver group stop  prod',     'Parar   TODOS os nós do grupo'),
                ('lserver group delete prod',    'Excluir grupo (nós NÃO são apagados)'),
            ],
            's3':  '⚙️   3. AUTOMAÇÃO E FUNÇÕES AVANÇADAS',
            'c3':  [
                ('lserver -a <nome>',            'Auto-Heal ❤  — revive ao travar'),
                ('lserver -r <nome> 04:00',      'Reinício diário às 04:00 AM'),
                ('lserver -b <nome>',            'Menu de backups (manual ou automático)'),
                ('lserver daemon start',         'Ativar vigilante 24/7'),
                ('lserver daemon stop',          'Parar o vigilante'),
                ('lserver web start 9090',       'Painel web em http://IP:9090'),
                ('lserver web password',         'Configurar usuário e senha do painel'),
                ('lserver update',               'Atualizar LServer do GitHub'),
                ('lserver -t',                   'Mudar idioma (es / en / pt / fr)'),
            ],
            's4':  '🔔  4. ALERTAS WEBHOOK (DISCORD / TELEGRAM)',
            'c4':  [
                ('lserver webhook set <URL>',    'Salvar URL do webhook'),
                ('lserver webhook test',         'Enviar alerta de teste'),
                ('lserver webhook status',       'Verificar webhook configurado'),
                ('lserver webhook remove',       'Remover webhook salvo'),
            ],
            's5':  '💡  5. GUIA RÁPIDO — PRIMEIRO USO',
            'qs': [
                '1.  lserver -c meuservidor          # Cria o nó',
                '2.  lserver -o meuservidor          # Edita start.sh com seu comando',
                '3.  lserver -p meuservidor          # Inicia e mantém vivo',
                '4.  lserver -e meuservidor          # Abre o console',
                '5.  lserver daemon start            # Ativa Auto-Heal e reinícios',
            ],
        },
        'fr': {
            'title':    "🔥  LSERVER — WIKI & MANUEL D'UTILISATION  🔥",
            's1':  '📦  1. GESTION DE BASE DES NŒUDS',
            'c1':  [
                ('lserver -c <nom>',             'Créer un nœud  (ex: lserver -c lobby)'),
                ('lserver -c <nom> --template minecraft', 'Créer avec template Java/Minecraft'),
                ('lserver -p <nom>',             'Démarrer le nœud (keep-alive 24/7)'),
                ('lserver -d <nom>',             'Arrêter le nœud proprement'),
                ('lserver -k <nom>',             'Forcer la fermeture (kill)'),
                ('lserver -e <nom>',             'Ouvrir la console interactive'),
                ('lserver -o <nom>',             'Modifier le start.sh du nœud'),
                ('lserver -x <nom>',             'Supprimer le nœud (demande dossier)'),
            ],
            's2':  '👥  2. SYSTÈME DE GROUPES',
            'c2':  [
                ('lserver group',                'Ouvrir le menu interactif des groupes'),
                ('lserver group list',           'Voir groupes + état ONLINE/OFFLINE'),
                ('lserver group create prod',    'Créer le groupe "prod"'),
                ('lserver group add prod lobby', 'Ajouter "lobby" au groupe "prod"'),
                ('lserver group remove prod hub','Retirer "hub" du groupe (sans suppr.)'),
                ('lserver group start prod',     'Démarrer TOUS les nœuds du groupe'),
                ('lserver group stop  prod',     'Arrêter TOUS les nœuds du groupe'),
                ('lserver group delete prod',    'Supprimer le groupe (nœuds conservés)'),
            ],
            's3':  '⚙️   3. AUTOMATISATION ET FONCTIONS AVANCÉES',
            'c3':  [
                ('lserver -a <nom>',             'Auto-Heal ❤  — relance si plantage'),
                ('lserver -r <nom> 04:00',       'Redémarrage quotidien à 04:00'),
                ('lserver -b <nom>',             'Menu sauvegardes (manuel/auto)'),
                ('lserver daemon start',         'Activer le gardien 24/7'),
                ('lserver daemon stop',          'Arrêter le gardien'),
                ('lserver web start 9090',       'Panneau web http://IP:9090'),
                ('lserver web password',         'Configurer identifiants du panneau'),
                ('lserver update',               'Mettre à jour LServer depuis GitHub'),
                ('lserver -t',                   'Changer de langue (es / en / pt / fr)'),
            ],
            's4':  '🔔  4. ALERTES WEBHOOK (DISCORD / TELEGRAM)',
            'c4':  [
                ('lserver webhook set <URL>',    'Enregistrer l\'URL du webhook'),
                ('lserver webhook test',         'Envoyer une alerte de test'),
                ('lserver webhook status',       'Vérifier le webhook configuré'),
                ('lserver webhook remove',       'Supprimer le webhook enregistré'),
            ],
            's5':  '💡  5. GUIDE RAPIDE — PREMIER DÉMARRAGE',
            'qs': [
                '1.  lserver -c monserveur           # Créer le nœud',
                '2.  lserver -o monserveur           # Éditer start.sh',
                '3.  lserver -p monserveur           # Démarrer et maintenir actif',
                '4.  lserver -e monserveur           # Ouvrir sa console',
                '5.  lserver daemon start            # Activer Auto-Heal & redémarrages',
            ],
        },
    }

    t = T.get(lang, T['es'])
    CMD_W = 36  # ancho columna izquierda (comando)

    print(f"\n{c}╔{'═' * W}╗{RESET}")
    title_pad = W - len(t['title'])
    print(f"{c}║{RESET} {GOLD}{BOLD}{t['title']}{RESET}{' ' * max(0, title_pad - 1)}{c}║{RESET}")
    sep()

    for section_key in ['s1', 's2', 's3', 's4']:
        cmds_key = section_key.replace('s', 'c')
        line(f" {CYAN}{BOLD}{t[section_key]}{RESET}")
        blank()
        for cmd_text, desc_text in t[cmds_key]:
            cmd_col  = f" {GOLD}{cmd_text:<{CMD_W}}{RESET}"
            desc_col = f"{GRAY}{desc_text}{RESET}"
            line(f"{cmd_col}{desc_col}")
        blank()
        sep()

    # Sección quick start
    line(f" {CYAN}{BOLD}{t['s5']}{RESET}")
    blank()
    for step in t['qs']:
        line(f"  {ORANGE}{step}{RESET}")
    blank()
    print(f"{c}╚{'═' * W}╝{RESET}\n")

def print_help():
    from lserver.core import list_all_nodes
    list_all_nodes()


def _clean(text):
    """Elimina codigos ANSI para calcular longitud real."""
    return re.sub(r'\033\[[0-9;]*m', '', text)


def log_success(msg):
    """Mensaje de exito con icono verde y linea decorativa."""
    prefix = f"{BG_GREEN}{BOLD} ✔ OK {RESET}"
    print(f"{prefix}  {GREEN}{BOLD}{msg}{RESET}")


def log_info(msg):
    """Mensaje informativo con icono naranja."""
    prefix = f"{BG_ORANGE}{BOLD} ℹ  {RESET}"
    print(f"{prefix}  {LIGHT_ORANGE}{msg}{RESET}")


def log_warn(msg):
    """Mensaje de advertencia con icono amarillo."""
    prefix = f"{YELLOW}{BOLD} ⚠  WARN {RESET}"
    print(f"{prefix} {YELLOW}{msg}{RESET}")


def log_error(msg):
    """Mensaje de error con icono rojo prominente."""
    prefix = f"{BG_RED}{BOLD} ✖ ERROR {RESET}"
    print(f"{prefix} {RED}{BOLD}{msg}{RESET}")


def error_exit(msg):
    """Error fatal con caja visual antes de salir."""
    width = 68
    print(f"\n{RED}╔{'═' * width}╗{RESET}")
    # Dividir el mensaje si es muy largo
    words = msg.split()
    lines = []
    current = ""
    for w in words:
        if len(current) + len(w) + 1 <= width - 4:
            current = (current + " " + w).strip()
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)
    for line in lines:
        padding = width - 2 - len(line)
        print(f"{RED}║{RESET} {BOLD}{RED}{line}{RESET}{' ' * padding} {RED}║{RESET}")
    print(f"{RED}╚{'═' * width}╝{RESET}\n")
    sys.exit(1)


def print_menu(title, options, node_name=None):
    """
    Imprime un menu interactivo con estilo LServer.
    options: lista de (key, label) ej. [("1", "Backup manual"), ("0", "Cancelar")]
    """
    width = 54
    c = LIGHT_ORANGE
    # Header
    if node_name:
        header = f"  {GOLD}⚡ {title}{RESET} {GRAY}[{node_name}]{RESET}"
    else:
        header = f"  {GOLD}⚡ {title}{RESET}"
    print(f"\n{c}╔{'═' * width}╗{RESET}")
    pad = width - len(_clean(header)) - 1
    print(f"{c}║{RESET}{header}{' ' * max(0,pad)}{c}║{RESET}")
    print(f"{c}╠{'═' * width}╣{RESET}")
    for key, label in options:
        if key == "0":
            key_color = GRAY
            label_color = GRAY
        else:
            key_color = GOLD
            label_color = WHITE
        row = f"  {key_color}[{key}]{RESET}  {label_color}{label}{RESET}"
        pad = width - len(_clean(row)) - 1
        print(f"{c}║{RESET}{row}{' ' * max(0,pad)}{c}║{RESET}")
    print(f"{c}╚{'═' * width}╝{RESET}")
    # Prompt con estilo
    if node_name:
        return input(f"\n  {GOLD}➤{RESET}  Opción: ")
    return input(f"\n  {GOLD}➤{RESET}  Opción: ")
