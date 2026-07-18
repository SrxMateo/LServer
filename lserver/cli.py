"""CLI principal de LServer v3."""
import sys
import os
import argparse
from lserver import __version__
from lserver.ui import print_help, log_info, log_success, log_error, error_exit
from lserver.core import (
    create_node, start_node, stop_node, kill_node,
    enter_node, list_all_nodes, delete_node,
    toggle_critical, handle_backup, start_daemon, stop_daemon,
    validate_node_name
)
from lserver.daemon import run_daemon

def main():
    if len(sys.argv) == 1:
        list_all_nodes()
        sys.exit(0)

    # --- Subcomandos nativos (sin argparse) ---
    cmd = sys.argv[1]
    
    # lserver daemon start|stop
    if cmd == "daemon":
        if len(sys.argv) > 2:
            if sys.argv[2] == "start":
                start_daemon()
                sys.exit(0)
            elif sys.argv[2] == "stop":
                stop_daemon()
                sys.exit(0)
        print("Uso: lserver daemon start|stop")
        sys.exit(1)
    
    # lserver update
    if cmd == "update":
        from lserver.updater import check_update
        check_update()
        sys.exit(0)
    
    # lserver webhook set|remove|test <url>
    if cmd == "webhook":
        from lserver.alerts import set_webhook, remove_webhook, get_webhook, send_alert
        if len(sys.argv) > 2:
            sub = sys.argv[2]
            if sub == "set" and len(sys.argv) > 3:
                set_webhook(sys.argv[3])
                sys.exit(0)
            elif sub == "remove":
                remove_webhook()
                sys.exit(0)
            elif sub == "test":
                url = get_webhook()
                if url:
                    send_alert("Test", "LServer webhook funcionando correctamente.")
                    log_success("Alerta de prueba enviada.")
                else:
                    log_error("No hay webhook configurado. Usa: lserver webhook set <url>")
                sys.exit(0)
            elif sub == "status":
                url = get_webhook()
                if url:
                    log_info(f"Webhook activo: {url}")
                else:
                    log_info("No hay webhook configurado.")
                sys.exit(0)
        print("Uso: lserver webhook set <url> | remove | test | status")
        sys.exit(1)
    
    # lserver group create|add|remove|delete|start|stop|list
    if cmd == "group":
        from lserver.groups import (create_group, delete_group, add_to_group,
                                     remove_from_group, start_group, stop_group, show_groups)
        if len(sys.argv) > 2:
            sub = sys.argv[2]
            if sub == "create" and len(sys.argv) > 3:
                create_group(sys.argv[3])
                sys.exit(0)
            elif sub == "delete" and len(sys.argv) > 3:
                delete_group(sys.argv[3])
                sys.exit(0)
            elif sub == "add" and len(sys.argv) > 4:
                add_to_group(sys.argv[3], sys.argv[4])
                sys.exit(0)
            elif sub == "remove" and len(sys.argv) > 4:
                remove_from_group(sys.argv[3], sys.argv[4])
                sys.exit(0)
            elif sub == "start" and len(sys.argv) > 3:
                start_group(sys.argv[3])
                sys.exit(0)
            elif sub == "stop" and len(sys.argv) > 3:
                stop_group(sys.argv[3])
                sys.exit(0)
            elif sub == "list":
                show_groups()
                sys.exit(0)
        print("Uso: lserver group create|delete|add|remove|start|stop|list <args>")
        sys.exit(1)
    
    # lserver web start|stop|password
    if cmd == "web":
        from lserver.web.server import start_web_server, stop_web_server, run_web_server
        from lserver.web.auth import set_password, has_credentials
        if len(sys.argv) > 2:
            sub = sys.argv[2]
            if sub == "start":
                port = int(sys.argv[3]) if len(sys.argv) > 3 else 9090
                start_web_server(port)
                sys.exit(0)
            elif sub == "stop":
                stop_web_server()
                sys.exit(0)
            elif sub == "password":
                import getpass
                user = input("Usuario: ")
                pw = getpass.getpass("Contrasena: ")
                pw2 = getpass.getpass("Confirmar contrasena: ")
                if pw != pw2:
                    error_exit("Las contrasenas no coinciden.")
                set_password(user, pw)
                log_success(f"Credenciales configuradas para '{user}'.")
                sys.exit(0)
        print("Uso: lserver web start [puerto] | stop | password")
        sys.exit(1)
    
    # lserver --run-web (uso interno)
    if cmd == "--run-web":
        from lserver.web.server import run_web_server
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 9090
        run_web_server(port)
        sys.exit(0)
    
    # --- Flags con argparse ---
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-p', '--start', metavar='NODO', help='Encender servidor')
    parser.add_argument('-d', '--stop', metavar='NODO', help='Detener el nodo')
    parser.add_argument('-k', '--kill', metavar='NODO', help='Matar el server')
    parser.add_argument('-c', '--create', metavar='NODO', help='Crear un nodo')
    parser.add_argument('-x', '--delete', metavar='NODO', help='Borrar el nodo')
    parser.add_argument('-l', '--list', action='store_true', help='Lista de nodos')
    parser.add_argument('-e', '--enter', metavar='NODO', help='Consola interactiva')
    parser.add_argument('-a', '--autoheal', metavar='NODO', help='Toggle Auto-Heal')
    parser.add_argument('-b', '--backup', metavar='NODO', help='Gestion de Backups')
    parser.add_argument('-r', '--restart', metavar='NODO', help='Reinicio programado')
    parser.add_argument('-o', '--open', metavar='NODO', help='Editar start.sh')
    parser.add_argument('-v', '--version', action='store_true', help='Version')
    parser.add_argument('-h', '--help', action='store_true', help='Ayuda')
    parser.add_argument('--run-daemon', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--template', metavar='TIPO', default=None, help='Plantilla al crear nodo')

    args, unknown = parser.parse_known_args()

    if args.run_daemon:
        run_daemon()
        sys.exit(0)

    if args.version:
        print(f"LServer v{__version__}")
        sys.exit(0)

    if args.help:
        print_help()
        sys.exit(0)

    if args.list:
        list_all_nodes()
        sys.exit(0)

    if args.create:
        name = args.create
        template = args.template
        if template:
            from lserver.templates import get_template, list_templates
            if template not in list_templates():
                error_exit(f"Plantilla '{template}' no existe. Disponibles: {', '.join(list_templates())}")
            # Crear nodo con plantilla
            validate_node_name(name)
            from lserver.state import get_node as state_get_node
            if state_get_node(name):
                error_exit(f"El nodo '{name}' ya existe.")
            current_dir = os.getcwd()
            node_path = os.path.join(current_dir, name)
            if not os.path.exists(node_path):
                os.makedirs(node_path)
                log_success(f"Directorio creado en {node_path}")
            
            start_script = os.path.join(node_path, "start.sh")
            with open(start_script, "w") as f:
                f.write(get_template(template))
            os.chmod(start_script, 0o755)
            log_info(f"Plantilla '{template}' aplicada a {start_script}")
            
            from lserver.state import add_node as state_add_node
            state_add_node(name, node_path, "./start.sh")
            log_success(f"Nodo '{name}' creado con plantilla '{template}'.")
        else:
            create_node(name)
        sys.exit(0)

    if args.start:
        start_node(args.start)
        sys.exit(0)

    if args.stop:
        stop_node(args.stop)
        sys.exit(0)

    if args.kill:
        kill_node(args.kill)
        sys.exit(0)

    if args.delete:
        delete_node(args.delete)
        sys.exit(0)

    if args.enter:
        enter_node(args.enter)
        sys.exit(0)

    if args.autoheal:
        toggle_critical(args.autoheal)
        sys.exit(0)

    if args.backup:
        handle_backup(args.backup)
        sys.exit(0)

    if args.restart:
        name = args.restart
        validate_node_name(name)
        from lserver.state import get_node as state_get_node, set_node_restart_time
        node = state_get_node(name)
        if not node:
            error_exit(f"El nodo '{name}' no existe.")
        
        # El tiempo viene como argumento adicional
        if unknown and len(unknown) > 0:
            time_str = unknown[0]
            # Validar formato HH:MM
            import re
            if not re.match(r'^\d{2}:\d{2}$', time_str):
                error_exit("Formato invalido. Usa HH:MM (ej: 04:00)")
            set_node_restart_time(name, time_str)
            log_success(f"Reinicio programado para '{name}' todos los dias a las {time_str}.")
        else:
            # Si no hay hora, mostrar/desactivar
            current = node.get('restart_time', '')
            if current:
                log_info(f"Reinicio programado actual para '{name}': {current}")
                ans = input("Deseas desactivarlo? (s/N): ")
                if ans.lower() == 's':
                    set_node_restart_time(name, '')
                    log_success(f"Reinicio programado desactivado para '{name}'.")
            else:
                log_info(f"No hay reinicio programado para '{name}'.")
                log_info("Uso: lserver -r <nodo> HH:MM")
        sys.exit(0)

    if args.open:
        name = args.open
        validate_node_name(name)
        from lserver.state import get_node as state_get_node
        node = state_get_node(name)
        if not node:
            error_exit(f"El nodo '{name}' no existe.")
        start_script = os.path.join(node['path'], 'start.sh')
        if not os.path.exists(start_script):
            error_exit(f"No existe start.sh en {node['path']}")
        # Usar nano, si no esta disponible, vi
        editor = "nano"
        if os.system("which nano > /dev/null 2>&1") != 0:
            editor = "vi"
        os.system(f"{editor} {start_script}")
        sys.exit(0)

    # Si ingresaron argumentos invalidos
    print_help()
    sys.exit(1)

if __name__ == "__main__":
    main()
