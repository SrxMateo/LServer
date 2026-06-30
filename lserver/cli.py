import sys
import argparse
from lserver import __version__
from lserver.ui import print_help
from lserver.core import (
    create_node, start_node, stop_node, kill_node,
    enter_node, list_all_nodes, delete_node,
    toggle_critical, handle_backup, start_daemon, stop_daemon
)
from lserver.daemon import run_daemon

def main():
    if len(sys.argv) == 1:
        list_all_nodes()
        sys.exit(0)

    # Subcomando daemon nativo
    if sys.argv[1] == "daemon":
        if len(sys.argv) > 2:
            if sys.argv[2] == "start":
                start_daemon()
                sys.exit(0)
            elif sys.argv[2] == "stop":
                stop_daemon()
                sys.exit(0)
        print("Uso: lserver daemon start|stop")
        sys.exit(1)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-p', '--start', metavar='NODO', help='Encender servidor y mantenerlo 24/7')
    parser.add_argument('-d', '--stop', metavar='NODO', help='Detener el nodo')
    parser.add_argument('-k', '--kill', metavar='NODO', help='Matar el server si se corrompió')
    parser.add_argument('-c', '--create', metavar='NODO', help='Crear un server/carpeta')
    parser.add_argument('-x', '--delete', metavar='NODO', help='Borrar el nodo')
    parser.add_argument('-l', '--list', action='store_true', help='Mostrar la lista de nodos')
    parser.add_argument('-e', '--enter', metavar='NODO', help='Entrar al nodo asignado')
    parser.add_argument('-a', '--autoheal', metavar='NODO', help='Activar/Desactivar Auto-Heal (Watchdog)')
    parser.add_argument('-b', '--backup', metavar='NODO', help='Gestión de Backups (Manual/Automático)')
    parser.add_argument('-v', '--version', action='store_true', help='Mostrar versión')
    parser.add_argument('-h', '--help', action='store_true', help='Mostrar ayuda')
    parser.add_argument('--run-daemon', action='store_true', help=argparse.SUPPRESS)

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
        create_node(args.create)
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

    # Si ingresaron argumentos inválidos
    print_help()
    sys.exit(1)

if __name__ == "__main__":
    main()
