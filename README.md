# Cálculo de Pensión de Vejez en Colombia

Calculadora de pensión de vejez para el Régimen de Prima Media en Colombia, desarrollada en Python.

## Creadores del proyecto

- Thomas Leon Torres
- Andres Felipe Zora

## Tabla de contenido

- [Descripción del proyecto](#descripción-del-proyecto)
- [Tecnologías](#tecnologías)
- [Arquitectura](#arquitectura)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Interfaz de usuario](#interfaz-de-usuario)
- [Entradas](#entradas)
- [Proceso](#proceso)
- [Salidas](#salidas)
- [Pruebas unitarias](#pruebas-unitarias)
- [Ejecución de la aplicación](#ejecución-de-la-aplicación)
- [Versión de Python](#versión-de-python)
- [Dependencias y entorno](#dependencias-y-entorno)
- [Control de versiones](#control-de-versiones)

---

## Descripción del proyecto

El proyecto consiste en una calculadora de pensión de vejez para el Régimen de Prima Media en Colombia.

La aplicación permite ingresar los datos necesarios de una persona y calcular el valor estimado de su pensión, teniendo en cuenta:

- IBC de los últimos 10 años.
- IBC de toda la vida laboral.
- Salario mínimo legal vigente.
- Semanas cotizadas.
- Edad.
- Sexo.

El sistema también realiza validaciones sobre los datos ingresados y genera las excepciones correspondientes cuando los datos no son válidos o no se cumplen los requisitos necesarios para realizar el cálculo.

---

## Tecnologías

El proyecto está desarrollado utilizando:

- **Python 3**
- **unittest** para las pruebas unitarias.
- **Git** para el control de versiones.
- **GitHub** para alojar el repositorio.

El proyecto utiliza principalmente funcionalidades de la biblioteca estándar de Python, por lo que no requiere librerías externas para su funcionamiento.

---

## Arquitectura

El proyecto utiliza una arquitectura basada en la separación de responsabilidades entre el **Modelo (Model)** y la **Vista (View)**.

### Model

La capa `model` contiene la lógica de negocio de la aplicación.

En esta capa se encuentran:

- El cálculo de la pensión.
- El cálculo del IBL.
- El cálculo de la relación entre IBL y SMLMV.
- El cálculo de la tasa de reemplazo.
- El cálculo de las semanas adicionales.
- Las validaciones de los datos.
- Las excepciones utilizadas por el sistema.
- La estructura `DatosPension`, utilizada para agrupar los datos necesarios para realizar el cálculo.

Ubicación:

```text
src/model/
```

Archivo principal:

```text
src/model/logica_pension.py
```

### View

La capa `view` contiene la interfaz de usuario.

Actualmente se utiliza una interfaz de consola (CLI), donde el usuario ingresa los datos y posteriormente recibe los resultados del cálculo.

Ubicación:

```text
src/view/console/
```

La vista se encarga principalmente de:

- Solicitar los datos al usuario.
- Enviar los datos a la lógica de negocio.
- Recibir el resultado.
- Mostrar los resultados en consola.
- Mostrar los mensajes de error correspondientes.

La vista no realiza directamente los cálculos internos de la pensión.

### Controller

El proyecto contempla el directorio `controller` para la capa encargada de coordinar las diferentes partes de la aplicación.

Ubicación:

```text
src/controller/

El directorio `src` debe estar marcado como **Sources Root** en el
IDE de Pycharm, para que Python pueda reconocer correctamente los módulos del
proyecto y resolver los imports.

Para que Visual Studio Code reconozca correctamente los módulos
ubicados dentro de `src`, "El directorio src se configura como ruta de búsqueda de módulos 
de Python en Visual Studio Code."

En `.vscode/settings.json`:

```json
{
    "python.analysis.extraPaths": ["./src"]
}
Calculadora_Pensional/  (SOLO VISUAL STUDIO CODE)
│
├── .vscode/
│   ├── settings.json
│   └── launch.json
│
├── src/
│   ├── __init__.py
│   │
│   ├── model/
│   │   ├── __init__.py
│   │   └── logica_pension.py
│   │
│   ├── view/
│   │   └── console/
│   │       └── main.py
│   │
│   └── controller/
│       ├── __init__.py
│
├── tests/
│   ├── __init__.py
│   └── test_pension.py
│
├── doc/
│   ├── Entrevista.ogg
│   └── trabajofinalcasosdeprueba.xlsx
│
├── .gitignore
└── README.md
```

La separación de responsabilidades permite mantener la lógica de negocio independiente de la interfaz de usuario, facilitando el mantenimiento, las pruebas y futuras modificaciones del proyecto.

---

## Estructura del proyecto

La estructura principal del proyecto es la siguiente:

```text
Proyecto_calculadora_pensional/
│
├── src/  -> Sources Root
│   ├── model/
│   │   ├── __init__.py
│   │   └── logica_pension.py
│   │
│   ├── view/
│   │   └── console/
│   │       └── main.py
│   │
│   └── controller/
│
├── tests/
│   └── test_pension.py
│
├── README.md
└── .gitignore
```

La estructura permite separar claramente el código de la aplicación (`src`) de las pruebas automatizadas (`tests`).

---

## Interfaz de usuario

La aplicación cuenta con una interfaz de consola (CLI).

Al iniciar la aplicación, el usuario debe ingresar los siguientes datos:

- IBC de los últimos 10 años.
- IBC de toda la vida laboral.
- Salario mínimo legal vigente.
- Semanas cotizadas.
- Edad.
- Sexo.

Después de ingresar los datos, el sistema realiza las validaciones correspondientes y, si los datos son válidos, muestra los resultados del cálculo.

Entre los resultados mostrados se encuentran:

- IBL calculado.
- Relación entre IBL y SMLMV.
- Porcentaje base.
- Semanas adicionales.
- Incremento.
- Porcentaje total.
- Pensión estimada.

---

## Entradas

El cálculo necesita los siguientes datos:

### IBC de los últimos 10 años

Corresponde al ingreso base de cotización utilizado como referencia para el período de los últimos 10 años.

### IBC de toda la vida laboral

Corresponde al ingreso base de cotización utilizado como referencia durante toda la vida laboral.

El sistema utiliza ambos valores para determinar el ingreso base de liquidación que resulte más favorable.

### Salario mínimo legal vigente

Es el salario mínimo utilizado como referencia para realizar el cálculo de la pensión.

Este valor debe ser mayor que cero.

### Semanas cotizadas

Corresponde al número total de semanas cotizadas por la persona durante su vida laboral.

Para tener derecho al cálculo de la pensión se requieren como mínimo:

- 1300 semanas.

### Edad

Corresponde a la edad de la persona al momento de solicitar la pensión.

Las edades mínimas utilizadas por el sistema son:

- 57 años para mujeres.
- 62 años para hombres.

### Sexo

Se utiliza para determinar la edad mínima requerida.

Los valores utilizados por la aplicación son:

- `M` para hombre.
- `F` para mujer.

---

## Proceso

El cálculo se realiza mediante varias etapas.

### 1. Validación de los datos

Antes de realizar el cálculo, el sistema verifica que los datos ingresados sean válidos.

Entre las validaciones realizadas se encuentran:

- Las semanas no pueden ser negativas.
- El IBL no puede ser negativo.
- El IBL no puede ser cero.
- El salario mínimo legal vigente no puede ser negativo.
- El salario mínimo legal vigente no puede ser cero.
- Se deben cumplir las semanas mínimas requeridas.
- Se debe cumplir la edad mínima correspondiente.

Si alguno de estos datos no es válido, el sistema genera la excepción correspondiente y muestra un mensaje de error.

### 2. Verificación del derecho a la pensión

La persona debe cumplir simultáneamente:

- Tener al menos 1300 semanas cotizadas.
- Haber alcanzado la edad mínima correspondiente.

Las edades mínimas utilizadas son:

- 57 años para mujeres.
- 62 años para hombres.

Si alguno de estos requisitos no se cumple, el cálculo se detiene y se muestra el error correspondiente.

### 3. Cálculo del IBL

El sistema determina el ingreso base de liquidación a partir de los valores ingresados de IBC.

Se tienen en cuenta:

- El IBC de los últimos 10 años.
- El IBC de toda la vida laboral.

Se utiliza el valor correspondiente según las reglas definidas para el cálculo de la aplicación.

### 4. Cálculo de la relación con el salario mínimo

Se calcula cuántos salarios mínimos representa el IBL.

La relación se obtiene mediante:

```text
IBL / SMLMV
```

### 5. Cálculo de la tasa de reemplazo

La tasa de reemplazo parte de un porcentaje base de 65,5%.

La tasa puede disminuir dependiendo de la cantidad de salarios mínimos que representa el IBL.

La tasa base tiene un límite mínimo de 55%.

Cuando existen semanas cotizadas adicionales a las 1300 semanas mínimas, se puede aumentar la tasa de reemplazo.

Por cada bloque completo de 50 semanas adicionales, se incrementa la tasa en 1,5 puntos porcentuales.

Las semanas adicionales que no completen un bloque de 50 semanas no generan un incremento.

La tasa de reemplazo final tiene un límite máximo de 80%.

### 6. Cálculo de la pensión

Finalmente, se calcula el valor de la pensión utilizando el IBL y la tasa de reemplazo.

La fórmula general utilizada es:

```text
Pensión = IBL × tasa de reemplazo
```

La pensión no puede ser inferior a un salario mínimo legal vigente.

Por esta razón, si el resultado obtenido es menor al salario mínimo, se utiliza el salario mínimo como valor final de la pensión.

---

## Salidas

El sistema produce uno de los siguientes resultados.

### Cálculo exitoso

Si los datos son válidos y se cumplen los requisitos, el sistema muestra:

- IBL calculado.
- Relación con el salario mínimo.
- Tasa base.
- Semanas adicionales.
- Incremento.
- Tasa total.
- Valor estimado de la pensión.

### Error de validación

Si alguno de los datos no es válido o no se cumplen los requisitos para acceder a la pensión, el sistema muestra un mensaje de error indicando el problema.

Entre los errores contemplados se encuentran:

- Semanas insuficientes.
- Semanas negativas.
- IBL igual a cero.
- IBL negativo.
- Salario mínimo legal vigente igual a cero.
- Salario mínimo legal vigente negativo.
- Edad insuficiente.
- Valores de entrada que no sean numéricos.

---

## Pruebas unitarias

Las pruebas automatizadas se encuentran en:

```text
tests/test_pension.py
```

El proyecto utiliza el módulo estándar de Python:

```text
unittest
```

Las pruebas cubren diferentes escenarios del cálculo, incluyendo:

- Casos normales.
- Semanas insuficientes.
- Semanas negativas.
- IBL igual a cero.
- IBL negativo.
- Salario mínimo igual a cero.
- Salario mínimo negativo.
- Edad insuficiente.
- Edad mínima para mujeres.
- Edad mínima para hombres.
- Tasa de reemplazo mínima del 55%.
- Tasa de reemplazo máxima del 80%.
- Semanas adicionales.
- Bloques incompletos de semanas adicionales.
- Garantía de pensión mínima.

### Ejecutar las pruebas

Desde la carpeta raíz del proyecto se puede ejecutar:

```bash
python -m unittest discover -s tests -v
```

El parámetro `-v` permite mostrar de manera detallada el resultado de cada prueba.

Si todas las pruebas son correctas, el sistema mostrará que las pruebas fueron ejecutadas satisfactoriamente.

---

## Ejecución de la aplicación

Para ejecutar la interfaz de consola, se debe abrir una terminal ubicada en la carpeta raíz del proyecto.

Ejecutar:

```bash
python src/view/console/main.py
```

Al ejecutar el programa aparecerá la interfaz de consola y se solicitarán los datos necesarios para realizar el cálculo.

Ejemplo:

```text
==================================================
       CALCULADORA PENSIONAL
==================================================

Ingrese los siguientes datos:

IBC de los últimos 10 años:
IBC de toda la vida laboral:
Salario mínimo legal vigente:
Semanas cotizadas:
Edad:
Sexo (M/F):
```

Después de ingresar los datos, el sistema mostrará los resultados o el mensaje de error correspondiente.

---

## Versión de Python

Se requiere Python 3 para ejecutar el proyecto.

Se recomienda utilizar Python 3.10 o superior.

Para comprobar la versión instalada:

```bash
python --version
```

Ejemplo:

```text
Python 3.10.x
```

---

## Dependencias y entorno

El proyecto utiliza principalmente funcionalidades de la biblioteca estándar de Python.

No se requieren librerías externas para ejecutar la aplicación.

Las pruebas automatizadas utilizan:

```text
unittest
```

`unittest` forma parte de la biblioteca estándar de Python, por lo que no es necesario instalarlo mediante pip.

Para ejecutar el proyecto solamente es necesario tener instalada una versión compatible de Python.

---

## Control de versiones

El proyecto utiliza Git como sistema de control de versiones y GitHub como plataforma para alojar y gestionar el repositorio.

Git permite realizar un seguimiento de los cambios realizados en el código y mantener diferentes versiones del proyecto durante su desarrollo.
