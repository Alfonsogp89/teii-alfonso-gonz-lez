<!-- markdownlint-disable MD013 -->
# Tecnologías Específicas en Ingeniería Informática • Configuración de Visual Studio Code
<!-- markdownlint-enable MD013 -->

- [Tecnologías Específicas en Ingeniería Informática • Configuración de Visual Studio Code](#tecnologías-específicas-en-ingeniería-informática--configuración-de-visual-studio-code)
  - [Instalación y configuración de Visual Studio Code](#instalación-y-configuración-de-visual-studio-code)
    - [Instalación](#instalación)
    - [Interfaz](#interfaz)
    - [Extensiones](#extensiones)
    - [Personalización](#personalización)
  - [Edición y ejecución de código Python con Visual Studio Code](#edición-y-ejecución-de-código-python-con-visual-studio-code)
  - [Depuración de código Python con Visual Studio Code](#depuración-de-código-python-con-visual-studio-code)
  - [Procesamiento de argumentos de línea de comandos en Python](#procesamiento-de-argumentos-de-línea-de-comandos-en-python)
  - [Referencias](#referencias)
    - [Python](#python)
    - [Visual Studio Code](#visual-studio-code)
    - [Markdown](#markdown)

___

## Instalación y configuración de Visual Studio Code

### Instalación

Visual Studio Code se puede descargar
[aquí](https://code.visualstudio.com/download). En Linux, se puede instalar de
varias formas diferentes:

<!-- markdownlint-disable MD013 -->
| Formato                                | Instrucciones                                                  |
| -------------------------------------- | -------------------------------------------------------------- |
| Paquete `.deb` (Ubuntu)                | `sudo apt install ./<VSCODEFILE>.deb`                          |
| Paquete `.rpm` (Fedora)                | `sudo yum install ./<VSCODEFILE>.rpm`                          |
| Contenedor `.tar.gz` (Ubuntu y Fedora) | `tar xzvf ./<VSCODEFILE>.tar.gz ; cd <VSCODEDIR>/bin ; ./code` |
| Paquete Snap                           | `sudo snap install --classic code`                             |
<!-- markdownlint-enable MD013 -->

:pushpin: También es posible instalar Visual Studio Code, tanto en Ubuntu como
en Fedora, utilizando el *repositorio* y *clave* correspondientes. Para más
detalles, véase [Visual Studio Code on
Linux](https://code.visualstudio.com/docs/setup/linux).

Visual Studio Code soporta un modo *portable* que permite crear y mantener su
configuración y extensiones en un directorio independiente. Este modo sólo está
soportado en la instalación mediante un archivo contenedor `.tar.gz`. Para
activar el modo *portable*, hay que crear un subdirectorio `data` dentro del
directorio de Visual Studio Code:

```none
|- <VSCODEDIR>
|   |- bin
|   |   |- code (ejecutable)
|   |- data
|   |   |- user-data
|   |   |   |- User
|   |   |   |   |- settings.json (configuración)
|   |   |   |   |- ...
|   |   |- extensions (extensiones)
|   |   |   |- ms-python.python-...
|   |   |   |- ...
|   |- ...
```

:pushpin: En la versión *portable* de Visual Studio Code que usaremos en esta
asignatura, puede resultar conveniente desactivar las actualizaciones automáticas.
Para más detalles, véase [How do I opt out of VS Code
auto-updates?](https://code.visualstudio.com/docs/supporting/FAQ#_how-do-i-opt-out-of-vs-code-autoupdates).

### Interfaz

Configuración de Visual Studio Code para el idioma español:

<!-- markdownlint-disable MD013 -->
| Menú                                    | Acción                               |
| --------------------------------------- | ------------------------------------ |
| View : Command Palette (`Ctrl+Mayús+P`) | Configure Display Language (Español) |
<!-- markdownlint-enable MD013 -->

Principales componentes de la interfaz de usuario de Visual Studio Code:

- Barra de Actividades: Explorador, Búsqueda, Ejecución y Extensiones. Se puede
  ocultar/mostrar con `Ctrl+B`.
- Editor con soporte para pestañas y múltiples áreas de edición.
- Terminal. Se puede ocultar/mostrar con `Ctrl+J` o ``Ctrl+` ``.
- Barra de Estado: Información sobre errores y edición.

Cada acción en Visual Studio Code corresponde a un comando que se puede ejecutar
utilizando la Paleta de Comandos (Ver : Paleta de comandos o `Ctrl+Mayús+P`) o
directamente mediante un atajo de teclado.

<!-- markdownlint-disable MD013 -->
| Menú                                 | Acción                                            | Atajo de teclado  |
| ------------------------------------ | ------------------------------------------------- | ----------------- |
| Ayuda   : Bienvenido                 | Ayuda: Bienvenido                                 |                   |
| Ayuda   : Área de juegos interactiva | Ayuda: Área de juegos del editor interactivo      |                   |
| Ayuda   : Documentación              | Ayuda: Documentación                              |                   |
| Archivo : Preferencias               | Preferencias: Abrir métodos abreviados de teclado | `Ctrl+K` `Ctrl+S` |
| Ver     : Paleta de comandos         | Mostrar todos los comandos                        | `Ctrl+Shift+P`    |
<!-- markdownlint-enable MD013 -->

### Extensiones

Configuración de Visual Studio Code para el lenguaje de programación Python:

| Extensión | Autor     |
| --------- | --------- |
| Python    | Microsoft |
| Flake8    | Microsoft |
| Mypy      | Microsoft |
| autopep8  | Microsoft |
| isort (*) | Microsoft |

Extensiones usadas para la preparación del material de esta asignatura:

| Extensión               | Autor        |
| ----------------------- | ------------ |
| Git Graph               | mhutchie     |
| GitHub Markdown Preview | Matt Bierner |
| GitHub Theme            | GitHub       |
| Markdown All in One     | Yu Zhang     |
| markdownlint            | David Anson  |
| ReWrap Revived          | Drew Nutter  |
| vscode-icons (*)        | Microsoft    |

Otras extensiones populares:

| Extensión              | Autor     |
| ---------------------- | --------- |
| Remote Development (*) | Microsoft |
| Live Share         (*) | Microsoft |
| Docker             (*) | Microsoft |
| ...                    | ...       |

`(*)` *Nota:* Todas las extensiones anteriores no marcadas con `(*)` están ya
por defecto instaladas en la copia original del VScode portable descargable del
AV, aunque por supuesto podéis instalar posteriormente las adicionales que
deseéis.

### Personalización

<!-- markdownlint-disable MD013 -->
| Menú                         | Acción                                                        | Atajo de teclado  |
| ---------------------------- | ------------------------------------------------------------- | ----------------- |
| Archivo : Preferencias       | Preferencias : Abrir configuración de usuario                 | `CTRL+,`          |
| Ver     : Paleta de Comandos | Preferencias : Abrir configuración de usuario (JSON)          |                   |
| Ver     : Paleta de Comandos | Preferencias : Abrir configuración del aŕea de trabajo (JSON) |                   |
| Archivo : Preferencias       | Preferencias : Tema : Tema de color                           | `CTRL+K` `CTRL+T` |
| Archivo : Preferencias       | Preferencias : Tema : Tema de icono de archivo                |                   |
<!-- markdownlint-enable MD013 -->

:pushpin: La configuración se guarda en
`VSCode-linux-x64/data/user-data/User/settings.json` si se usa la versión
portable de Visual Studio Code, o en `.vscode/settings.json` dentro de la
carpeta abierta en caso contrario.

## Edición y ejecución de código Python con Visual Studio Code

Funcionalidad de edición más destacada:

- Emparejamiento de paréntesis y llaves
- Plegado de código
- Selección de columnas (`Mayús+Alt` y Selección)
- Formato de documento (`Ctrl+Mayús+I`)
- Formato de selección (`Ctrl+K Ctrl+F`)
- *Intellisense*
- Edición multi-cursor (`Alt+Click`)
- Reubicación de selección (Selección y `Alt+Up/Down`)
- Añadir comentario (`Ctrl+K Ctrl+C`)
- Quitar comentario (`Ctrl+K Ctrl+U`)
- Modo *Zen* (`Ctrl+K Z`)

Para más detalles, véanse
[Basic Editing](https://code.visualstudio.com/docs/editor/codebasics) y
[Tips and Tricks](https://code.visualstudio.com/docs/getstarted/tips-and-tricks).

Para ejecutar el ejemplo `hello.py`, se tiene que:

1. Abrir `hello.py` en el editor.

2. Pulsar `Ctrl+F5` o :arrow_forward:.

:pushpin: La configuración para ejecución y depuración de archivos Python se
guarda en `.vscode/launch.json` dentro de la carpeta abierta.

## Depuración de código Python con Visual Studio Code

A su vez, para depurar el ejemplo `hello.py` paso a paso, hay que:

1. Crear un punto de interrupción en `if __name__ == "__main__":`.

2. Pulsar `F5`.

En la parte izquierda podemos ver el valor de las variables y funciones tanto
locales como globales, las expresiones definidas por el usuario, la pila de
llamadas y los puntos de interrupción. En la parte superior tenemos la Barra de
Depuración que nos ofrece las opciones de Continuar, Depurar paso a paso por
procedimientos, Depurar paso a paso por instrucciones, Salir de la depuración
del procedimiento, Continuar y Detener.

Más adelante se explicará en detalle como depurar y caracterizar el rendimiento
de código Python.

## Procesamiento de argumentos de línea de comandos en Python

El ejemplo `parse_getopt.py` admite las opciones `"[-o OUTPUT] [-v] [-h]"`
utilizando el módulo `getopt`.

Para añadir argumentos a la línea de órdenes,

1. Agrega una configuración para archivos Python: `Ejecutar : Agregar
configuración : Python Debugger : Archivo de Python`

1. Edita el archivo `launch.json` e incluye la línea `args` en la configuración
"Depurador de Python: Archivo actual":

```json
        {
            "name": "Depurador de Python: Archivo actual",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "args": [                        <-- Añade/modifica este array
                "-h"
            ],
            "justMyCode": true
        }
```

En Python, hay módulos como `argparse` o `click` que facilitan el procesamiento
de argumentos de la línea de órdenes. Por ejemplo, véanse `parse_argparse.py` y
`parse_click.py`.

- [ ] Depura el código de `parse_getopt.py` cuando los argumentos de la línea de
  órdenes son `"-o output.txt -v"`.
- [ ] Modifica el código de `parse_getopt.py`, `parse_argparse.py` y
  `parse_click.py` para que las opciones admitidas  sean: `"[-f] [-i INPUT] [-o
  OUTPUT] [-v] [-h]"`. **No se deben admitir parámetros adicionales**.

## Referencias

### Python

- [Python](https://www.python.org/)
  - [Python Documentation by Version](https://www.python.org/doc/versions/)
    - [getopt](https://docs.python.org/3.8/library/getopt.html)
    - [argparse](https://docs.python.org/3.8/library/argparse.html)
  - [Alternative Python Implementations](https://www.python.org/download/alternatives/)
- [Python Package Index (PyPI)](https://pypi.org)
  - [click](https://pypi.org/project/click/)

### Visual Studio Code

- [Visual Studio Code Introductory Videos](https://code.visualstudio.com/docs/getstarted/introvideos)
- [Python in Visual Studio Code](https://code.visualstudio.com/docs/languages/python)
- [Getting Started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial)
- [Debugging in VS Code](https://code.visualstudio.com/docs/python/debugging)
- [Portable Mode](https://code.visualstudio.com/docs/editor/portable)
- [Visual Studio Code Keyboard Shortcuts](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-linux.pdf)

### Markdown

- [Markdown and Visual Studio Code](https://code.visualstudio.com/Docs/languages/markdown)
- [Markdown Guide](https://www.markdownguide.org/)
- [markdown.es](https://markdown.es/)
- [Dillinger](https://dillinger.io/)
