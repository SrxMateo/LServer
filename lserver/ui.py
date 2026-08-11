import sys
import os
# Codigos ANSI para colores
GOLD = "\033[38;5;220m"
ORANGE = "\033[38;5;208m"
LIGHT_ORANGE = "\033[38;5;214m"
YELLOW = "\033[38;5;226m"
GREEN = "\033[1;32m"
BLUE = "\033[1;34m"
RED = "\033[1;31m"
CYAN = "\033[36m"
GRAY = "\033[90m"
WHITE = "\033[97m"
RESET = "\033[0m"

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
    """Imprime una wiki interactiva, detallada y colorida para LServer."""
    from lserver.state import get_setting
    lang = get_setting('language') or 'es'

    if lang == 'en':
        print(f"\n{LIGHT_ORANGE}╔══════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {GOLD}🔥 LSERVER WIKI & USER MANUAL 🔥{RESET}                                           {LIGHT_ORANGE}║{RESET}")
        print(f"{LIGHT_ORANGE}╠══════════════════════════════════════════════════════════════════════════════╣{RESET}")
        
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}1. BASIC NODE MANAGEMENT 📦{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Create a server:     {GOLD}lserver -c <name>{RESET} (Add {GRAY}--template minecraft{RESET}{WHITE}){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Start node:          {GREEN}lserver -p <name>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Safe stop:           {RED}lserver -d <name>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Kill (Force):        {RED}lserver -k <name>{RESET} 💀{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Console / Terminal:  {ORANGE}lserver -e <name>{RESET} (Ctrl+C to exit, Arrows supported){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET}")
        
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}2. GROUP SYSTEM 👥{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Create group:        {GOLD}lserver -g <group> -c{RESET} (Interactive: prompts for nodes){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Stop all:            {RED}lserver -g <group> -a{RESET} (Stops all nodes in group){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Start all:           {GREEN}lserver -g <group> -s{RESET} (Starts all nodes in group){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Add/Remove node:     {ORANGE}lserver -g <group> --add <node>{RESET} / {GRAY}--remove <node>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} List groups:         {GOLD}lserver -g list{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET}")
        
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}3. ADVANCED FEATURES & AUTOMATION ⚙️{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Private Web Panel:   {GOLD}lserver web start 8080{RESET} 🌐 (Use {GRAY}lserver web password{RESET}{WHITE}){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Auto-Heal (Revive):  {ORANGE}lserver -a <node>{RESET} ❤️ (Revives if it crashes){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Daily Restart:       {ORANGE}lserver -r <node> HH:MM{RESET} ⏰ (Ex: {GRAY}lserver -r lobby 04:00{RESET}{WHITE}){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Edit start.sh:       {ORANGE}lserver -o <node>{RESET} ✏️{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Start Daemon:        {GOLD}lserver daemon start{RESET} 🛡️ (Required for Auto-Heal/Restarts){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Change Language:     {GOLD}lserver -t{RESET} 🌐 (Interactive language prompt){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET}")
        
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}4. WEBHOOK ALERTS (DISCORD/TELEGRAM) 🔔{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Setup webhook:       {GOLD}lserver webhook set <URL>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Test alert:          {GREEN}lserver webhook test{RESET}")
        
        print(f"{LIGHT_ORANGE}╚══════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

    elif lang == 'pt':
        print(f"\n{LIGHT_ORANGE}╔══════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {GOLD}🔥 LSERVER WIKI & MANUAL DO USUÁRIO 🔥{RESET}                                     {LIGHT_ORANGE}║{RESET}")
        print(f"{LIGHT_ORANGE}╠══════════════════════════════════════════════════════════════════════════════╣{RESET}")
        
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}1. GESTÃO BÁSICA DE NÓS 📦{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Criar um servidor:   {GOLD}lserver -c <nome>{RESET} (Adicione {GRAY}--template minecraft{RESET}{WHITE}){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Iniciar nó:          {GREEN}lserver -p <nome>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Parada segura:       {RED}lserver -d <nome>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Matar (Forçar):      {RED}lserver -k <nome>{RESET} 💀{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Console / Terminal:  {ORANGE}lserver -e <nome>{RESET} (Ctrl+C para sair, Setas suportadas){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET}")
        
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}2. SISTEMA DE GRUPOS 👥{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Criar grupo:         {GOLD}lserver -g <grupo> -c{RESET} (Interativo: solicitará os nós){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Desligar todos:      {RED}lserver -g <grupo> -a{RESET} (Para todos os nós do grupo){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Ligar todos:         {GREEN}lserver -g <grupo> -s{RESET} (Inicia todos os nós do grupo){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Adic./Remov. nó:     {ORANGE}lserver -g <grupo> --add <nó>{RESET} / {GRAY}--remove <nó>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Listar grupos:       {GOLD}lserver -g list{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET}")
        
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}3. RECURSOS AVANÇADOS & AUTOMAÇÃO ⚙️{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Painel Web Privado:  {GOLD}lserver web start 8080{RESET} 🌐 (Use {GRAY}lserver web password{RESET}{WHITE}){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Auto-Heal (Reviver): {ORANGE}lserver -a <nó>{RESET} ❤️ (Revive se travar){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Reinício Diário:     {ORANGE}lserver -r <nó> HH:MM{RESET} ⏰ (Ex: {GRAY}lserver -r lobby 04:00{RESET}{WHITE}){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Editar start.sh:     {ORANGE}lserver -o <nó>{RESET} ✏️{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Iniciar Daemon:      {GOLD}lserver daemon start{RESET} 🛡️ (Requerido para Auto-Heal/Reinícios){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Mudar Idioma:        {GOLD}lserver -t{RESET} 🌐 (Menu interativo de idiomas){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET}")
        
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}4. ALERTAS WEBHOOK (DISCORD/TELEGRAM) 🔔{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Configurar webhook:  {GOLD}lserver webhook set <URL>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Testar alerta:       {GREEN}lserver webhook test{RESET}")
        
        print(f"{LIGHT_ORANGE}╚══════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

    elif lang == 'fr':
        print(f"\n{LIGHT_ORANGE}╔══════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {GOLD}🔥 LSERVER WIKI & MANUEL D'UTILISATION 🔥{RESET}                                  {LIGHT_ORANGE}║{RESET}")
        print(f"{LIGHT_ORANGE}╠══════════════════════════════════════════════════════════════════════════════╣{RESET}")
        
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}1. GESTION DE BASE DES NŒUDS 📦{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Créer un serveur:    {GOLD}lserver -c <nom>{RESET} (Ajoutez {GRAY}--template minecraft{RESET}{WHITE}){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Démarrer le nœud:    {GREEN}lserver -p <nom>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Arrêt sécurisé:      {RED}lserver -d <nom>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Tuer (Forcer):       {RED}lserver -k <nom>{RESET} 💀{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Console / Terminal:  {ORANGE}lserver -e <nom>{RESET} (Ctrl+C pour quitter, Flèches supportées){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET}")
        
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}2. SYSTÈME DE GROUPES 👥{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Créer un groupe:     {GOLD}lserver -g <groupe> -c{RESET} (Interactif: demande les nœuds){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Arrêter tout:        {RED}lserver -g <groupe> -a{RESET} (Arrête tous les nœuds du groupe){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Démarrer tout:       {GREEN}lserver -g <groupe> -s{RESET} (Démarre tous les nœuds du groupe){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Ajout/Retrait nœud:  {ORANGE}lserver -g <groupe> --add <nœud>{RESET} / {GRAY}--remove <nœud>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Lister groupes:      {GOLD}lserver -g list{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET}")
        
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}3. FONCTIONNALITÉS AVANCÉES & AUTOMATISATION ⚙️{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Panneau Web Privé:   {GOLD}lserver web start 8080{RESET} 🌐 (Utilisez {GRAY}lserver web password{RESET}{WHITE}){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Auto-Heal (Réanimer):{ORANGE}lserver -a <nœud>{RESET} ❤️ (Réanime s'il plante){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Redémarrage Quotid.: {ORANGE}lserver -r <nœud> HH:MM{RESET} ⏰ (Ex: {GRAY}lserver -r lobby 04:00{RESET}{WHITE}){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Modifier start.sh:   {ORANGE}lserver -o <nœud>{RESET} ✏️{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Lancer Daemon:       {GOLD}lserver daemon start{RESET} 🛡️ (Requis pour Auto-Heal/Redémarrages){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Changer de Langue:   {GOLD}lserver -t{RESET} 🌐 (Invite de langue interactive){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET}")
        
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}4. ALERTES WEBHOOK (DISCORD/TELEGRAM) 🔔{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Configurer webhook:  {GOLD}lserver webhook set <URL>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Tester l'alerte:     {GREEN}lserver webhook test{RESET}")
        
        print(f"{LIGHT_ORANGE}╚══════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

    else:
        print(f"\n{LIGHT_ORANGE}╔══════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {GOLD}🔥 LSERVER WIKI & MANUAL DE USUARIO 🔥{RESET}                                     {LIGHT_ORANGE}║{RESET}")
        print(f"{LIGHT_ORANGE}╠══════════════════════════════════════════════════════════════════════════════╣{RESET}")
        
        # Seccion 1: Basicos
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}1. GESTIÓN BÁSICA DE NODOS 📦{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Crea un servidor:    {GOLD}lserver -c <nombre>{RESET} (Añade {GRAY}--template minecraft{RESET}{WHITE}){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Arrancar nodo:       {GREEN}lserver -p <nombre>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Detener seguro:      {RED}lserver -d <nombre>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Matar (Forzar):      {RED}lserver -k <nombre>{RESET} 💀{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Consola / Terminal:  {ORANGE}lserver -e <nombre>{RESET} (Ctrl+C para salir, Flechas soportadas){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET}")
        
        # Seccion 2: Grupos
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}2. SISTEMA DE GRUPOS 👥{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Crear grupo:         {GOLD}lserver -g <grupo> -c{RESET} (Interactiva: te preguntará nodos){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Apagar todo:         {RED}lserver -g <grupo> -a{RESET} (Detiene todos los nodos del grupo){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Encender todo:       {GREEN}lserver -g <grupo> -s{RESET} (Inicia todos los nodos del grupo){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Añadir/Quitar nodo:  {ORANGE}lserver -g <grupo> --add <nodo>{RESET} / {GRAY}--remove <nodo>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Listar grupos:       {GOLD}lserver -g list{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET}")
        
        # Seccion 3: Funciones Avanzadas
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}3. FUNCIONES AVANZADAS Y AUTOMATIZACIÓN ⚙️{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Panel Web Privado:   {GOLD}lserver web start 8080{RESET} 🌐 (Usa {GRAY}lserver web password{RESET}{WHITE}){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Auto-Heal (Revivir): {ORANGE}lserver -a <nodo>{RESET} ❤️ (Revive si crashea){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Reinicio Diario:     {ORANGE}lserver -r <nodo> HH:MM{RESET} ⏰ (Ej: {GRAY}lserver -r lobby 04:00{RESET}{WHITE}){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Editar start.sh:     {ORANGE}lserver -o <nodo>{RESET} ✏️{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Activar Vigilante:   {GOLD}lserver daemon start{RESET} 🛡️ (Requerido para Auto-Heal/Reinicios){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Cambiar Idioma:      {GOLD}lserver -t{RESET} 🌐 (Selector de idioma interactivo){RESET}")
        print(f"{LIGHT_ORANGE}║{RESET}")
        
        # Seccion 4: Alertas
        print(f"{LIGHT_ORANGE}║{RESET} {CYAN}4. ALERTAS WEBHOOK (DISCORD/TELEGRAM) 🔔{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Configurar:          {GOLD}lserver webhook set <URL>{RESET}")
        print(f"{LIGHT_ORANGE}║{RESET} {WHITE} Probar alerta:       {GREEN}lserver webhook test{RESET}")
        
        print(f"{LIGHT_ORANGE}╚══════════════════════════════════════════════════════════════════════════════╝{RESET}\n")


def print_help():
    from lserver.core import list_all_nodes
    list_all_nodes()

def log_success(msg):
    print(f"{GREEN}[SUCCESS]{RESET} {msg}")

def log_info(msg):
    print(f"{WHITE}[INFO]{RESET} {msg}")

def log_error(msg):
    print(f"{RED}[ERROR]{RESET} {msg}")

def error_exit(msg):
    log_error(msg)
    sys.exit(1)
