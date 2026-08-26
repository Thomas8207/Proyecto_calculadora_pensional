Cálculo de Pensión de Vejez en Colombia (Régimen de Prima Media)

## Tabla de contenido
Creadores del proyecto:Thomas Leon Torres y Andres Felipe Zora

# Tecnologías y arquitectura

## Lenguaje utilizado

El proyecto está desarrollado en **Python**, utilizando una estructura modular para separar la lógica de negocio, la interfaz de usuario y las pruebas.

## Arquitectura

Se utiliza una arquitectura basada en la **separación Model/View (Modelo/Vista)**:

* **Model:** contiene la lógica principal del cálculo pensional y las excepciones del sistema. Se encuentra en `src/model/`, específicamente en `logica_pension.py`.
* **View:** contiene la interfaz de usuario de la aplicación. Se encuentra en `src/view/console/` y corresponde a una aplicación de consola.
* **Controller:** la estructura del proyecto contempla el directorio `src/controller/` para la capa de control y coordinación entre las diferentes partes de la aplicación.

Esta separación permite mantener la lógica de negocio independiente de la interfaz de usuario, facilitando el mantenimiento, las pruebas y futuras modificaciones del proyecto.

## Interfaz

La aplicación cuenta con una **interfaz de consola (CLI)**. El usuario introduce los datos necesarios para calcular la pensión, como:

* IBC de los últimos 10 años.
* IBC de toda la vida laboral.
* Salario mínimo legal vigente.
* Semanas cotizadas.
* Edad.
* Sexo.

Posteriormente, la aplicación muestra los resultados del cálculo, incluyendo el IBL, la relación con el salario mínimo, la tasa de reemplazo y la pensión estimada.

## Pruebas

Para las pruebas automatizadas se utiliza el framework **`unittest`**, incluido en la biblioteca estándar de Python.

Las pruebas se encuentran en:

```text
tests/
└── test_pension.py
```

Se validan tanto casos normales como casos excepcionales, incluyendo:

* Semanas cotizadas insuficientes.
* Semanas negativas.
* IBL igual a cero.
* IBL negativo.
* Salario mínimo igual a cero.
* Edad insuficiente.
* Edad mínima requerida.
* Tasa de reemplazo mínima del 55%.
* Tasa de reemplazo máxima del 80%.
* Semanas adicionales para incrementar la tasa de reemplazo.

Para ejecutar las pruebas:

```bash
python -m unittest discover -s tests -v
```

## Control de versiones

El proyecto utiliza **Git** como sistema de control de versiones y **GitHub** como plataforma para alojar y gestionar el repositorio.

Git permite realizar un seguimiento de los cambios realizados en el código y mantener diferentes versiones del proyecto durante su desarrollo.

## Versión de Python requerida

Se requiere **Python 3.x** para ejecutar el proyecto.

Se recomienda utilizar **Python 3.10 o superior**, ya que el proyecto utiliza anotaciones de tipo (`float`, `int`, `-> float`, etc.) y una estructura de paquetes compatible con versiones modernas de Python.

Para comprobar la versión instalada:

```bash
python --version
```

Ejemplo:

```text
Python 3.10.x
```




 
- [Entradas](#entradas)
- [Proceso](#proceso)
- [Salidas](#salidas)

Entradas
El cálculo necesita cinco datos de la persona que solicita la pensión:
-Ingreso Base de Liquidación (IBL): es el promedio de los salarios que la persona cotizó durante su vida laboral, ya ajustados por inflación (IPC) al año en que se hace el cálculo. La norma permite tomar como referencia los últimos 10 años de cotización o toda la vida laboral, lo que resulte más favorable para la persona.

-Salario Mínimo Legal Mensual Vigente (SMLMV): el salario mínimo del año en que se liquida la pensión. Este valor no lo elige la persona; es un dato de contexto que cambia cada año y que la norma usa como unidad de medida para saber "cuántos salarios mínimos" representa el ingreso de alguien.

-Semanas cotizadas: el número total de semanas que la persona aportó al sistema pensional a lo largo de su vida laboral.

-Edad: la edad de la persona en el momento en que solicita la pensión.

-Sexo: determina cuál es la edad mínima que aplica para tener derecho a la pensión.

Estos cinco datos son suficientes para resolver el cálculo completo; no se necesita ninguna otra información externa.

Proceso

El cálculo se resuelve en dos partes: primero se verifica si la persona tiene derecho a la pensión, y solo si lo tiene, se calcula el valor.

1. Verificar el derecho a la pensión. La persona debe cumplir dos condiciones al mismo tiempo: haber cotizado al menos 1.300 semanas, y haber cumplido la edad mínima según su sexo (57 años si es mujer, 62 años si es hombre). Si falta cualquiera de las dos condiciones, el proceso se detiene ahí y el sistema debe devolver un error explicando cuál requisito no se cumplió; no tiene sentido seguir calculando un valor de pensión para alguien que todavía no tiene derecho a ella.

La persona debe cumplir dos condiciones al mismo tiempo: haber cotizado al menos **1.300 semanas**, y haber cumplido la edad mínima según su sexo (**57 años** si es mujer, **62 años** si es hombre). Si falta cualquiera de las dos condiciones, el proceso se detiene ahí y el sistema devuelve un error explicando cuál requisito no se cumplió.
2. Calcular la tasa de reemplazo. Si la persona sí cumple los requisitos, se calcula qué porcentaje del IBL le corresponde recibir como pensión mensual (la "tasa de reemplazo"). Este porcentaje no es fijo: depende de qué tan alto es el ingreso de la persona y de cuántas semanas cotizó por encima del mínimo. La lógica es la siguiente:

Se calcula cuántos salarios mínimos representa el IBL (dividiendo el IBL entre el SMLMV).
A partir de ahí, la tasa de reemplazo parte de un 65,5% y disminuye 0,5% por cada salario mínimo adicional que representa el ingreso: entre más gana la persona, menor es el porcentaje que recibe sobre su IBL. Esta tasa base nunca puede bajar del 55%, sin importar qué tan alto sea el ingreso.
Si la persona cotizó más de las 1.300 semanas mínimas, la tasa aumenta 1,5 puntos porcentuales por cada bloque completo de 50 semanas adicionales. Los bloques incompletos (por ejemplo, 49 semanas de más) todavía no cuentan.
La tasa final —ya con el aumento por semanas adicionales incluido— nunca puede superar el 80%, sin importar cuántas semanas adicionales tenga la persona.

3. Calcular el valor de la pensión. El valor mensual de la pensión es el IBL multiplicado por la tasa de reemplazo obtenida en el paso anterior. Pero existe una garantía adicional: ninguna pensión reconocida puede ser inferior a 1 SMLMV. Si el resultado de la multiplicación da un valor menor al salario mínimo, se paga el salario mínimo en su lugar.
El valor mensual es `IBL × tasa de reemplazo`. Existe una garantía adicional: **ninguna pensión reconocida puede ser inferior a 1 SMLMV**. Si el resultado de la multiplicación da un valor menor al salario mínimo, se paga el salario mínimo en su lugar.

Salidas
El sistema debe producir uno de estos dos tipos de resultado:

-Si la persona cumple los requisitos: el valor mensual de la pensión, en pesos, ya con la garantía del mínimo aplicada si corresponde.

-Si la persona no cumple los requisitos, o si alguno de los datos de entrada es inválido (por ejemplo, un IBL o un SMLMV menor o igual a cero, o un número de semanas negativo): un mensaje de error que indique con precisión cuál fue el problema, en lugar de un valor numérico. Esto es intencional: el sistema no debe intentar "adivinar" o forzar un cálculo con datos que no tienen sentido.
