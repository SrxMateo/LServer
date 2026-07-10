<div align="center">
  <img src="assets/logo.png" alt="LServer CLI Logo" width="300">
  <br/>

  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=24&pause=1000&color=0E75B6&center=true&vCenter=true&width=600&lines=LServer+CLI+-+Server+Management;Ultimate+Control+for+SysAdmins;Zero-Trust+Security+Built-in;Powered+by+Lumax+Corp" alt="Typing SVG" />

  <p>
    <a href="https://lumax.lat"><img src="https://img.shields.io/badge/Powered_by-Lumax_Corp-0e75b6?style=for-the-badge&logo=google-earth&logoColor=white" alt="Lumax Corp"></a>
    <img src="https://img.shields.io/badge/Status-Active_Development-brightgreen?style=for-the-badge" alt="Status">
    <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/License-MIT-purple?style=for-the-badge" alt="License">
  </p>
</div>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png" width="100%">
</p>

## 🚀 ¿Qué es LServer CLI?

Se acabó el tener que buscar procesos huérfanos, perder tiempo con configuraciones complejas o escribir comandos largos y tediosos. **LServer CLI** es una herramienta de élite desarrollada para dueños de servidores y administradores de sistemas que exigen **velocidad, estabilidad y control absoluto**.

Con **LServer**, puedes encender, apagar, visualizar y administrar múltiples "nodos" (instancias de servidores o aplicaciones) con una interfaz de terminal increíblemente elegante, impulsada por tecnología de monitoreo en tiempo real.

<br/>

## 🔥 Arquitectura & Características

<div align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,sqlite,linux,bash,docker,nginx&perline=6" />
  </a>
</div>

*   **Motor SQLite Asíncrono**: Transacciones seguras (ACID) mediante patrón Singleton. Adiós a la corrupción de archivos JSON; LServer maneja miles de operaciones con fiabilidad militar.
*   **Vigilante Inteligente (Daemon)**: Un proceso fantasma en segundo plano de 0% CPU que vigila tus servidores. 
    *   **Auto-Heal (❤)**: Si tu servidor crashea por falta de RAM o errores, el vigilante lo resucita automáticamente.
    *   **Auto-Backups (💾)**: Copias de seguridad automáticas a las 03:00 AM, aislando tus datos en archivos `.tar.gz` ultra-comprimidos.
*   **Seguridad Zero-Trust**: Inyección de comandos, Path Traversal y ataques por Regex completamente bloqueados mediante sanitizadores estrictos y consultas SQL preparadas.
*   **Estadísticas Nativas en Vivo**: Observa el consumo de CPU, RAM y Disco duro directamente en el hermoso Dashboard dorado.

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png" width="100%">
</p>

## ⚡ Instalación Mágica en 1 Clic

No pierdas tiempo con instalaciones manuales. Hemos preparado un script de autoconfiguración para sistemas Linux modernos (Ubuntu, Debian, CentOS, etc.).

Abre tu consola y pega este único comando:

```bash
curl -sL https://raw.githubusercontent.com/SrxMateo/LServer/main/install.sh | bash
```

¡Eso es todo! El instalador se encargará de clonar el código, instalar las dependencias necesarias y dejar el comando global `lserver` listo para la acción.

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png" width="100%">
</p>

## 🛠️ Panel de Control y Arsenal de Comandos

Para ver tu centro de comando, simplemente escribe `lserver`. Te encontrarás con un Panel de Control majestuoso.

| Comando | Descripción |
| :--- | :--- |
| `lserver -p <nodo>` | **Encender (Power)**: Arranca el servidor de inmediato y lo mantiene 24/7. |
| `lserver -d <nodo>` | **Detener**: Envía la orden de apagado seguro al nodo para no perder datos. |
| `lserver -k <nodo>` | **Kill (Forzado)**: Destruye el proceso al instante. Ideal para nodos congelados. |
| `lserver -c <nodo>` | **Crear**: Levanta un nodo nuevo (prepara la carpeta y su configuración). |
| `lserver -x <nodo>` | **Borrar**: Elimina el nodo y limpia completamente su directorio del sistema. |
| `lserver -a <nodo>` | **Auto-Heal**: Activa/Desactiva el resucitador automático del Daemon (❤). |
| `lserver -b <nodo>` | **Backups**: Menú interactivo para crear respaldos manuales o automáticos 24h (💾). |
| `lserver daemon start` | **Iniciar Vigilante**: Activa el motor de LServer en background. |
| `lserver daemon stop` | **Detener Vigilante**: Apaga los servicios de monitoreo. |
| `lserver -l` | **Listar**: Carga el Dashboard y la tabla de todos tus servidores creados. |
| `lserver -e <nodo>` | **Entrar**: Ingresa al log en vivo del servidor. *(Usa `Ctrl+C` para salir sin detenerlo)* |

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png" width="100%">
</p>

## 💡 Ejemplos Rápidos de Producción

**1. Creando tu primer servidor de producción:**
```bash
lserver -c MiAppBackend
lserver -p MiAppBackend
```
*¡Listo! Tu aplicación estará corriendo en segundo plano protegida de cierres inesperados.*

**2. Revisando el estado de toda tu red:**
```bash
lserver
```
*Aparecerá el Dashboard informándote qué nodo está ONLINE y cuál está OFFLINE.*

<br/>

<div align="center">
  <h3>🤝 Desarrollo & Soporte</h3>
  <p><b>LServer</b> es un proyecto de código abierto forjado en los laboratorios de <b>Lumax Studio</b>.</p>
  <a href="https://lumax.lat"><img src="https://img.shields.io/badge/Visitar_Sitio_Oficial-www.lumax.lat-0e75b6?style=for-the-badge&logo=google-chrome" /></a>
  <br/><br/>
  <p><small>© 2026 SrxMateo & Lumax Studio. Construido con pasión y precisión.</small></p>
</div>
