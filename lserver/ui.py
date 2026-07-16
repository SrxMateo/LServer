import sys

# Códigos ANSI para colores
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
    print_box_line(f"  {GOLD}lserver -c <nodo>{RESET}    {ORANGE}Crear un nodo (carpeta y configuración).{RESET}", 63)
    print_box_line(f"  {GOLD}lserver -x <nodo>{RESET}    {ORANGE}Borrar el nodo y su directorio.{RESET}", 54)
    print_box_line(f"  {GOLD}lserver -a <nodo>{RESET}    {ORANGE}Alternar Auto-Heal (Watchdog).{RESET}", 53)
    print_box_line(f"  {GOLD}lserver -b <nodo>{RESET}    {ORANGE}Opciones de Backup (Manual/Automático).{RESET}", 62)
    print_box_line(f"  {GOLD}lserver daemon start{RESET} {ORANGE}Arranca el vigilante en background.{RESET}", 58)
    print_box_line(f"  {GOLD}lserver daemon stop{RESET}  {ORANGE}Detiene el vigilante.{RESET}", 44)
    print_box_line(f"  {GOLD}lserver -l{RESET}           {ORANGE}Mostrar Dashboard con nodos creados.{RESET}", 59)
    print_box_line(f"  {GOLD}lserver -e <nodo>{RESET}    {ORANGE}Consola interactiva del nodo (Ctrl+C para salir).{RESET}", 73)
    print_box_line(f"  {GOLD}lserver -v{RESET}           {ORANGE}Mostrar la versión de LServer.{RESET}", 53)
    print(f"{c_border}╠══════════════════════════════════════════════════════════════════════════════╣{RESET}")
    def pad_col(prefix_spaces, text_color, text, reset_color, width):
        visual_len = len(prefix_spaces) + len(text)
        pad_len = width - visual_len
        if pad_len < 0:
            text = text[:(width - len(prefix_spaces) - 3)] + "..."
            pad_len = 0
        return f"{prefix_spaces}{text_color}{text}{reset_color}" + (" " * pad_len)

    print_box_line(f" {YELLOW}LSERVER NODES STATUS{RESET}", 21)
    
    # Column widths: 22, 22, 30. Separators = 2. Total = 76.
    ticks = (" " * 22) + f"{LIGHT_ORANGE}╷{RESET}" + (" " * 22) + f"{LIGHT_ORANGE}╷{RESET}"
    print_box_line(ticks, 46)
    
    h1 = pad_col("  ", GOLD, "Status", RESET, 22)
    h2 = pad_col(" ", GOLD, "Service (Node)", RESET, 22)
    h3 = pad_col(" ", GOLD, "Path", RESET, 30)
    print_box_line(f"{h1}{LIGHT_ORANGE}│{RESET}{h2}{LIGHT_ORANGE}│{RESET}{h3}", 76)
    
    sep = f"{LIGHT_ORANGE}╶{'─'*21}┼{'─'*22}┼{'─'*29}╴{RESET}"
    print_box_line(sep, 76)
    
    if not nodes:
        d1 = pad_col("  ", GRAY, "- vacío -", RESET, 22)
        d2 = pad_col(" ", GRAY, "No hay nodos creados", RESET, 22)
        d3 = pad_col(" ", GRAY, "- usa lserver -c <nodo> -", RESET, 30)
        print_box_line(f"{d1}{LIGHT_ORANGE}│{RESET}{d2}{LIGHT_ORANGE}│{RESET}{d3}", 76)
    else:
        for name, data in nodes.items():
            running = is_running_func(name)
            if running:
                d1 = pad_col("  ", GREEN, "● ONLINE", RESET, 22)
            else:
                d1 = pad_col("  ", RED, "× OFFLINE", RESET, 22)
            
            heal_icon = "❤ " if data.get('is_critical') else ""
            backup_icon = "💾 " if data.get('backup_enabled') else ""
            d2 = pad_col(" ", GOLD, f"{heal_icon}{backup_icon}{name}", RESET, 22)
            d3 = pad_col(" ", ORANGE, data['path'], RESET, 30)
            
            print_box_line(f"{d1}{LIGHT_ORANGE}│{RESET}{d2}{LIGHT_ORANGE}│{RESET}{d3}", 76)

    print(f"{c_border}╚══════════════════════════════════════════════════════════════════════════════╝{RESET}")
    print("")

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
