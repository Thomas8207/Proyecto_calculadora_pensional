# Cálculo de Pensión de Vejez en Colombia

Calculadora de pensión de vejez para el Régimen de Prima Media, desarrollada en Python.

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

La aplicación permite ingresar los datos necesarios de una persona y calcular el valor estimado de su pensión, teniendo en cuenta las semanas cotizadas, la edad, el sexo, los ingresos base de cotización y el salario mínimo legal vigente.

El sistema también realiza validaciones sobre los datos ingresados y genera excepciones cuando no se cumplen los requisitos necesarios para realizar el cálculo.

---

## Tecnologías

El proyecto está desarrollado utilizando:

- **Python 3**
- **unittest** para las pruebas unitarias
- **Git** para el control de versiones
- **GitHub** para alojar el repositorio

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
