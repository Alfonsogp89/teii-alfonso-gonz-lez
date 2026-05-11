import marimo

__generated_with = "0.21.1"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    mo.md("# Introducción a Marimo")
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(f"""
        ## Marimo es un archivo Python

        Marimo guarda los proyectos como scripts de Python estándar, mientras que los notebooks tradicionales utilizan el formato JSON. Al ser código puro, se **facilita la revisión**, el **control de versiones con Git** y la **ejecución directa desde la terminal**.
    
        Es más, sabemos que en los notebooks tradicionales, las salidas de código y los gráficos se guardan dentro del propio archivo `.ipynb`, lo que suele generar conflictos al usar Git. Marimo **solo almacena el código fuente** en el archivo `.py`: la ejecución y sus resultados visuales no modifican el script original.

        Si necesitáramos compartir el documento con los resultados ya generados, Marimo permite **exportar el proyecto** como un archivo HTML independiente o como una aplicación basada en WebAssembly (WASM).
        """),
            mo.callout(
                mo.md(r"""
            **¿Cómo gestiona Markdown?** 
            El texto en Markdown se incluye directamente dentro del código Python mediante la función `mo.md()`, sin necesidad de crear un tipo de celda específico. Al visualizar el documento en el editor, puedes **ocultar el código de cualquier celda** para que solo se muestre el texto renderizado.
            """),
                kind="info",
            ),
        ], gap=0
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _titulo = mo.md("## Puesta en marcha\nLa instalación y ejecución de Marimo se gestiona directamente desde la línea de comandos.")

    _acordeon = mo.accordion({
        "1. Instalación y edición": mo.md(r"""
        Se utiliza el gestor de paquetes estándar:
        ```bash
        pip install marimo
        ```
        Para crear un nuevo proyecto o abrir uno existente en el editor web:
        ```bash
        marimo edit nombre_archivo.py
        ```
        """),
        "2. Modo producción (WebApp)": mo.md(r"""
        Si el objetivo es desplegar el documento como una aplicación web interactiva (ocultando el código fuente):
        ```bash
        marimo run nombre_archivo.py
        ```
        """),
        "3. Conversión desde Jupyter": mo.md(r"""
        Convertir un Jupyter notebook tradicional a marimo:
        ```bash
        marimo convert jupyter_notebook.ipynb > app_marimo.py
        ```
        """),
        "4. Tutoriales": mo.md(r"""
        Lanzar tutoriales interactivos integrados:
        ```bash
        marimo tutorial --help
        ```
        """)
    })

    # Renderizamos ambos elementos apilados verticalmente
    mo.vstack([_titulo, _acordeon])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Ejecución reactiva
    """)
    return


@app.cell
def _(mo):
    slider = mo.ui.slider(1, 22)
    return (slider,)


@app.cell(hide_code=True)
def _(mo, slider):
    mo.md(f"""
    Marimo emplea un modelo de **ejecución reactiva**.

    Esto significa que, a diferencia de los notebooks tradicionales, los notebooks de Marimo se ejecutan automáticamente cuando modificas el código o interactúas con elementos de la interfaz, como este deslizador: {slider}

    {"**" + ", ".join(map(str, range(slider.value))) + "**"}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Marimo analiza las celdas y modela las dependencias entre ellas: cada vez que se ejecuta una celda que define una variable global, Marimo ejecuta automáticamente todas las celdas que hacen referencia a dicha variable.
    """)
    return


@app.cell(hide_code=True)
def _(changed, mo):
    _mensaje = (
        mo.callout(
            mo.md(
                f"**¡Bien hecho!** Has activado la reactividad. `changed` ahora es `{changed}`."
            ),
            kind="success",
        )
        if changed
        else mo.callout(
            mo.md(
                "**Pruébalo:** En la celda inferior, cambia en el código el valor de `changed` a `True` y ejecútala. Verás cómo este mensaje se actualiza solo."
            ),
            kind="neutral",
        )
    )
    _mensaje
    return


@app.cell
def _():
    changed = False
    return (changed,)


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(r"""
        Para que esto funcione, Marimo **no permite definir la misma variable global en más de una celda**. 
    
        Por ello, es recomendable encapsular la lógica en funciones, clases o módulos de Python para minimizar el número de variables globales. Además, las variables que comienzan con un guion bajo se consideran "privadas" para la celda, lo que permite definirlas en múltiples celdas sin conflictos. 
    """),
        kind="warn",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _texto = mo.ui.text(label="Nombre:", placeholder="Escribe aquí...")
    _lenguaje = mo.ui.dropdown(options=["Python", "C++", "R", "Julia"], label="Lenguaje:")
    _fecha = mo.ui.date(label="Fecha de inicio:")
    _switch = mo.ui.switch(label="Modo oscuro")

    _escaparate = mo.md(f"""
    ## Más controles interactivos (`mo.ui`)

    Además del deslizador, Marimo dispone de todos los elementos clásicos para construir aplicaciones de datos y cuadros de mando. Puedes incrustarlos de forma muy fluida dentro de tus explicaciones por texto:

    - **Entrada de texto:** {_texto}
    - **Menú desplegable:** {_lenguaje}
    - **Selector de fecha:** {_fecha}
    - **Interruptor:** {_switch}

    *Cada vez que el usuario interactúa con cualquiera de ellos, las celdas que dependan de sus valores se reejecutarán automáticamente.*
    """)

    _escaparate
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Flujo de ejecución

    En Marimo, el orden visual de las celdas en el documento no determina el orden en que se ejecuta el código. El entorno gestiona la ejecución basándose en las relaciones entre las variables, construyendo automáticamente un grafo de dependencias.

    * **Independencia espacial:** Puedes colocar una celda que utiliza una variable por encima de la celda que la define sin que esto genere un error; Marimo resolverá el orden correcto de ejecución.
    * **Propagación de cambios:** Cuando modificas el código de una celda o interactúas con un componente visual que altera una variable, el sistema identifica y reejecuta únicamente las celdas que dependen (directa o indirectamente) de esa variable.
    * **Consistencia garantizada:** Este modelo asegura que todas las salidas en pantalla y el estado interno de la memoria estén siempre sincronizados, eliminando la posibilidad de obtener resultados erróneos por ejecutar celdas en un orden incorrecto. Esto reduce la necesidad de reiniciar el kernel para limpiar variables fantasma.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Marimo y Pandas
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Marimo tiene mucha interacción directa con librerías de análisis y visualización de datos como Pandas, Polars, Altair o Plotly. Esto nos permite renderizar `DataFrames` como tablas exploratorias o mostrar gráficos interactivos sin necesidad de configurar extensiones adicionales.
    """)
    return


@app.cell
def _():
    import pandas as pd

    # Cargamos el dataframe
    planetas = pd.read_csv("data/planets.csv")
    return (planetas,)


@app.cell
def _(mo, planetas):
    mo.vstack(
        [
            mo.md("""
            ### 1. Visualización por defecto
            Al devolver un `DataFrame` al final de una celda, Marimo lo renderiza automáticamente como una tabla interactiva. 
            Prueba a ordenar por columnas, usar la lupa, activar el explorador por filas o columnas...
            """),
            planetas,
        ]
    )
    return


@app.cell
def _(mo, planetas):
    _metodos = planetas["method"].dropna().unique().tolist()

    selector_metodo = mo.ui.dropdown(options=_metodos, value="Radial Velocity")
    slider_ano = mo.ui.slider(start=1989, stop=2014, step=1, value=2008, show_value=True)

    _instrucciones = mo.md(f"""
    ### 2. Filtrado y agrupación reactiva (con código)

    Podemos usar los componentes visuales para crear parámetros que alimenten nuestro código de Pandas en tiempo real.

    - Selecciona el método de descubrimiento: {selector_metodo}
    - Selecciona a partir de qué año: {slider_ano}
    """)

    _instrucciones
    return selector_metodo, slider_ano


@app.cell
def _(mo, planetas, selector_metodo, slider_ano):
    # 1. Filtramos usando las variables reactivas de la celda superior
    _filtrado = planetas[
        (planetas["method"] == selector_metodo.value) & 
        (planetas["year"] >= slider_ano.value)
    ]

    # 2. Agrupamos por año (Groupby) para contar planetas
    _agrupado = _filtrado.groupby("year")["number"].sum().reset_index()
    _agrupado.columns = ["Año", "Total de planetas descubiertos"]

    # 3. Mostramos los resultados
    mo.vstack([
        mo.md(f"**Resultados (Total encontrados: {len(_filtrado)}):**"),
        _agrupado
    ])
    return


@app.cell
def _(mo):
    mo.md("""
    ### 3. El Transformador Interactivo (`mo.ui.dataframe`)

    Esta es una de las herramientas más potentes de Marimo. Permite inyectar un componente para aplicar operaciones de Pandas (como **Filtros**, **Group By**, **Sort** o **Select**) directamente desde la interfaz visual y sin programar. Es más, genera el código en Python necesario para ejecutar dichas acciones de manera manual.
    """)
    return


@app.cell
def _(mo, planetas):
    # Este componente genera el menú interactivo para manipular el DataFrame
    transformador = mo.ui.dataframe(planetas)
    transformador
    return (transformador,)


@app.cell
def _(mo, transformador):
    mo.vstack([
        mo.md("Lo mejor de todo es que el resultado visual se guarda reactivamente como un `DataFrame` real (`transformador.value`), listo para ser procesado, entrenado o visualizado en cualquier otra celda posterior:"),
        transformador.value.head()
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    _titulo = mo.md(r"""
    ## Tutoriales en Marimo online

    [Estos tutoriales](https://docs.marimo.io/examples/) **son muy buenos**. Al abrirlos, se genera un marimo integrado en la propia web con el que se puede jugar fácilmente. A continuación adjuntamos los que pueden ser de mayor interés:
    """)

    _acordeon_tutoriales = mo.accordion({
        "1. Ejecución de celdas": mo.md(r"""
        * [Ejecución básica de Marimo](https://docs.marimo.io/examples/running_cells/basics/)
        * [Detener la ejecución de ciertas celdas](https://docs.marimo.io/examples/running_cells/stop/)
        * [Ejecutar celdas al clickar en botones](https://docs.marimo.io/examples/running_cells/run_button/)
        * [Actualizar celdas después de un tiempo](https://docs.marimo.io/examples/running_cells/refresh/)
        """),
        "2. Salidas de celdas": mo.md(r"""
        * [Salidas de celdas](https://docs.marimo.io/examples/outputs/basic_output/)
        * [Markdown básico](https://docs.marimo.io/examples/outputs/basic_markdown/)
        * [Mostrar vídeos y media](https://docs.marimo.io/api/media/)
        * [Mostrar plots](https://docs.marimo.io/examples/outputs/plots/)
        * [Mostrar salida con condicional](https://docs.marimo.io/examples/outputs/conditional_output/)
        * [Mostrar múltiples salidas en una sola celda](https://docs.marimo.io/examples/outputs/multiple_outputs/)
        """),
        "3. Pandas": mo.md(r"""
        * [Visor de DataFrame interactivo](https://docs.marimo.io/examples/outputs/dataframes/)
        * [Seleccionar columnas de un DataFrame](https://docs.marimo.io/api/inputs/table/)
        * [DataFrame editable](https://docs.marimo.io/api/inputs/data_editor/)
        * [DataFrame transformer interactivo](https://docs.marimo.io/api/inputs/dataframe/)
        """)
    })

    mo.vstack([_titulo, _acordeon_tutoriales])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Documentación

    * [Página oficial de Marimo](https://marimo.io/)
    * [QuickStart](https://docs.marimo.io/getting_started/quickstart/)
    * [Más tutoriales](https://github.com/Haleshot/marimo-tutorials)
    * [Documentación de los distintos tipos de inputs](https://docs.marimo.io/api/inputs/)
    """)
    return


if __name__ == "__main__":
    app.run()
