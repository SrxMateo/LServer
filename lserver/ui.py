import sys

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
    
    def print_box_line(text, visual_length):
        padding = 78 - visual_length
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
    print_box_line(f" {YELLOW}OPCIONES DISPONIBLES:{RESET}", 22)
    print_box_line(f"  {GOLD}lserver -p <nodo>{RESET}    {ORANGE}Encender el servidor y mantenerlo 24/7.{RESET}", 62)
    print_box_line(f"  {GOLD}lserver -d <nodo>{RESET}    {ORANGE}Detener el nodo de forma segura.{RESET}", 55)
    print_box_line(f"  {GOLD}lserver -k <nodo>{RESET}    {ORANGE}Matar el proceso del servidor (forzado).{RESET}", 63)
    print_box_line(f"  {GOLD}lserver -c <nodo>{RESET}    {ORANGE}Crear un nodo (carpeta y configuracion).{RESET}", 63)
    print_box_line(f"  {GOLD}lserver -x <nodo>{RESET}    {ORANGE}Borrar el nodo y su directorio.{RESET}", 54)
    print_box_line(f"  {GOLD}lserver -a <nodo>{RESET}    {ORANGE}Alternar Auto-Heal (Watchdog).{RESET}", 53)
    print_box_line(f"  {GOLD}lserver -b <nodo>{RESET}    {ORANGE}Opciones de Backup (Manual/Automatico).{RESET}", 62)
    print_box_line(f"  {GOLD}lserver -r <nodo> HH:MM{RESET} {ORANGE}Reinicio programado diario.{RESET}", 52)
    print_box_line(f"  {GOLD}lserver -e <nodo>{RESET}    {ORANGE}Consola interactiva (Ctrl+C para salir).{RESET}", 63)
    print_box_line(f"  {GOLD}lserver -o <nodo>{RESET}    {ORANGE}Editar el start.sh del nodo.{RESET}", 51)
    print_box_line(f"  {GOLD}lserver group{RESET}        {ORANGE}Gestionar grupos de nodos.{RESET}", 42)
    print_box_line(f"  {GOLD}lserver webhook{RESET}      {ORANGE}Configurar alertas Discord/Telegram.{RESET}", 54)
    print_box_line(f"  {GOLD}lserver daemon start{RESET} {ORANGE}Arranca el vigilante en background.{RESET}", 58)
    print_box_line(f"  {GOLD}lserver daemon stop{RESET}  {ORANGE}Detiene el vigilante.{RESET}", 44)
    print_box_line(f"  {GOLD}lserver web start{RESET}    {ORANGE}Abre el panel web privado.{RESET}", 45)
    print_box_line(f"  {GOLD}lserver update{RESET}       {ORANGE}Buscar actualizaciones de LServer.{RESET}", 51)
    print_box_line(f"  {GOLD}lserver -l{RESET}           {ORANGE}Mostrar Dashboard con nodos creados.{RESET}", 59)
    print_box_line(f"  {GOLD}lserver -v{RESET}           {ORANGE}Mostrar la version de LServer.{RESET}", 53)
    print(f"{c_border}╠══════════════════════════════════════════════════════════════════════════════╣{RESET}")

    print_box_line(f" {YELLOW}LSERVER NODES STATUS{RESET}", 21)
    
    # Header de la tabla con nuevas columnas
    hdr = f"  {GOLD}{'Status':<10}{RESET} {GOLD}{'Nodo':<14}{RESET} {GOLD}{'CPU':>5}{RESET} {GOLD}{'RAM':>6}{RESET} {GOLD}{'Puerto':>8}{RESET} {GOLD}{'Uptime':>10}{RESET}"
    print_box_line(hdr, 59)
    sep_line = f"  {LIGHT_ORANGE}{'─'*74}{RESET}"
    print_box_line(sep_line, 76)

    if not nodes:
        print_box_line(f"  {GRAY}No hay nodos creados. Usa: lserver -c <nombre>{RESET}", 49)
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
            print_box_line(row, 59)

    print(f"{c_border}╚══════════════════════════════════════════════════════════════════════════════╝{RESET}")
    print("")

def get_node_func_safe(name, data):
    """Helper seguro para obtener info del nodo."""
    import os
    pid_file = os.path.join(data.get('path', ''), 'server.pid')
    if os.path.exists(pid_file):
        return True
    return False

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
