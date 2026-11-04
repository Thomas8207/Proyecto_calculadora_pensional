# Calculadora Pensional - Régimen de Prima Media (Colombia)

Calculadora de pensión de vejez para el Régimen de Prima Media en Colombia,
desarrollada en Python con **tres interfaces de usuario (web con Flask y Blueprints, consola y GUI con
Kivy)** que comparten la misma lógica de negocio y persistencia en **PostgreSQL**.

## Enlaces del Proyecto Web

- **Aplicación Web Desplegada en Render:** https://proyecto-calculadora-pensional.onrender.com/
- **Repositorio Oficial:** https://github.com/Thomas8207/Proyecto_calculadora_pensional

## Creadores del proyecto

- **Thomas Leon Torres**
- **Andres Felipe Zora**

## Creadores del Gui
- **Samuel Alejandro Marroquín Garcés**
- **Juan Pablo Gaviria Franco**
- **Repositorio (fork original GUI):** https://github.com/SamuelMarroquin2009-12/Proyecto_calculadora_pensional

## Descripción del proyecto

La aplicación permite ingresar los datos de una persona y calcular el valor
estimado de su pensión de vejez, teniendo en cuenta:

- IBC de los últimos 10 años.
- IBC de toda la vida laboral.
- Salario mínimo legal vigente (SMLMV).
- Semanas cotizadas.
- Edad.
- Sexo.

El sistema valida los datos, genera excepciones personalizadas cuando los
datos no son válidos y muestra mensajes de error amigables al usuario en todas
sus interfaces (web, consola y GUI).

Además, los cálculos se guardan en una base de datos PostgreSQL en Render y
pueden consultarse por cédula.

## Arquitectura

El proyecto usa una arquitectura **Modelo - Controlador - Vista (MVC)**:

| Capa | Ubicación | Responsabilidad |
|------|-----------|-----------------|
| Modelo | `src/model/logica_pension.py` | Cálculo de la pensión, IBL, tasa de reemplazo, validaciones y excepciones |
| Modelo (BD) | `src/model/persona.py`, `src/model/calculo_pension.py` | Clases que representan las tablas `persona` y `calculopension` |
| Modelo (BD) | `src/model/conexion.py` | Administra la conexión transaccional a PostgreSQL con variables de entorno o `secret_config.py` |
| Controlador | `src/controller/pension_controller.py` | Coordina vistas y modelo; traduce excepciones a mensajes amigables; formatea resultados |
| Controlador | `src/controller/historial_controller.py` | Crea y borra tablas, inserta y busca cálculos en la base de datos |
| Vista (Web) | `src/view/web/app.py`, `src/view/web/vista_pension.py` y `templates/` | Aplicación web construida con **Blueprints de Flask**, menús, formularios y resultados |
| Vista (consola) | `src/view/console/console.py` y `src/view/console/historial_console.py` | Menú de consola: calcular, guardar, buscar historial y crear tablas |
| Vista (GUI) | `src/view/gui/gui.py` | Interfaz gráfica con Kivy |

La **lógica de negocio vive únicamente en el modelo**; la web, la consola y la GUI la
comparten a través de los mismos controladores. Ninguna vista realiza cálculos por su cuenta.

### Estructura de carpetas

```
Proyecto_calculadora_pensional/
│
├── main.py                    -> Punto de entrada (GUI, PyInstaller, Buildozer)
├── requirements.txt           -> Dependencias para producción y local (Flask, psycopg2-binary, gunicorn)
├── buildozer.spec             -> Configuración para app Android
├── .gitignore                 -> Excluye venv, binarios y secret_config.py
│
├── doc/
│   └── trabajofinalcasosdeprueba.xlsx
│
├── sql/
│   ├── crear_tablas.sql      -> Crea las tablas persona y calculopension
│   ├── borrar_tablas.sql     -> Borra las tablas
│   ├── insertar_calculo.sql  -> Ejemplo de INSERT para probar a mano
│   └── buscar_calculo.sql    -> Ejemplo de SELECT para probar a mano
│
├── src/
│   ├── secret_config_sample.py  -> Plantilla (secret_config.py es local y no se sube)
│   ├── model/
│   │   ├── logica_pension.py
│   │   ├── persona.py
│   │   ├── calculo_pension.py
│   │   └── conexion.py
│   ├── controller/
│   │   ├── pension_controller.py
│   │   └── historial_controller.py
│   └── view/
│       ├── console/
│       │   ├── console.py
│       │   └── historial_console.py
│       ├── gui/
│       │   └── gui.py
│       └── web/
│           ├── app.py           -> Servidor Flask que registra el Blueprint
│           └── vista_pension.py -> Blueprint con las rutas (/insertar, /buscar, /crear_tablas)
│
├── templates/
│   ├── menu_principal_calculadora.html -> Vista de inicio (menú, inserción, búsqueda y creación de tablas)
│   └── resultados_pension.html         -> Vista de resultados de pensión e historial
│
├── tests/
│   ├── test_pension.py              -> Pruebas del modelo (casos del Excel)
│   ├── test_controller.py           -> Pruebas del controlador
│   ├── test_gui.py                  -> Pruebas de la GUI
│   ├── test_historial_controller.py -> Pruebas de base de datos
│   └── test_web.py                  -> Pruebas unitarias de las rutas y vistas web
│
└── README.md
```

## Entradas

- **IBC últimos 10 años** y **IBC toda la vida laboral** (pesos): el sistema
  usa el valor más favorable como IBL.
- **Salario mínimo legal vigente**: debe ser mayor que cero.
- **Semanas cotizadas**: mínimo 1300 para tener derecho a pensión. Debe
  ser un número entero (`1300` es válido, `1300.5` se rechaza con un
  mensaje amigable).
- **Edad**: mínimo 57 años (mujeres) o 62 años (hombres). También debe
  ser un número entero.
- **Sexo**: `M` (hombre) o `F` (mujer).
- **Cédula** y **nombre** (para guardar en la base de datos): la cédula
  debe tener únicamente dígitos y el nombre no puede estar vacío.

## Proceso

1. **Validación**: IBL no negativo ni cero, SMLMV positivo, semanas no
   negativas y >= 1300, edad mínima según sexo, sexo válido.
2. **IBL**: `max(IBC últimos 10 años, IBC toda la vida)`.
3. **Relación IBL/SMLMV**: cuántos salarios mínimos representa el IBL.
4. **Tasa base**: 65,5% menos 0,5 puntos por cada salario mínimo, con piso del 55%.
5. **Incremento**: +1,5 puntos por cada bloque completo de 50 semanas adicionales.
6. **Tasa total**: tasa base + incremento, con tope del 80%.
7. **Pensión**: `IBL × tasa total`, con garantía de un salario mínimo.

## Salidas

IBL calculado, relación con el SMLMV, porcentaje base, semanas adicionales,
incremento, porcentaje total y **pensión estimada**. En caso de datos
inválidos se muestra un mensaje de error amigable que indica **qué pasó, por qué pasó y cómo se soluciona**.

---

## Aplicación Web (Flask + MVC + Render)

La aplicación web traslada toda la funcionalidad del proyecto a un entorno de navegador cumpliendo con los estándares de arquitectura modular.

### Funcionalidades Web Disponibles
1. **Menú de Inicio Unificado:** Acceso centralizado a todas las acciones desde `/`.
2. **Opción para Crear Tablas:** Botón en el menú que ejecuta la inicialización de la estructura relacional (`persona` y `calculopension`) en PostgreSQL.
3. **Insertar y Calcular Pensión:** Formulario interactivo que valida campos, procesa las reglas de pensión y almacena el registro en la base de datos.
4. **Buscar Historial:** Consulta del historial de cálculos asociados a un número de cédula, ordenados cronológicamente.

### Instrucciones para Ejecutar con una Base de Datos en Blanco

1. **Configurar el archivo de conexión:**
   Crear el archivo `src/secret_config.py` con las credenciales de la base de datos PostgreSQL vacía:
   ```python
   DB_HOST = "localhost"              # O el host de Render
   DB_NAME = "nombre_bd_en_blanco"
   DB_USER = "usuario"
   DB_PASSWORD = "password"
   DB_PORT = "5432"
   DB_SSLMODE = "disable"             # Usar "require" si es en la nube (Render)
   ```

2. **Iniciar la aplicación web localmente:**
   ```bash
   python -m src.view.web.app
   ```
   Abra `http://127.0.0.1:5000/` en el navegador.

3. **Creación inicial de tablas:**
   En la interfaz web inicial, haga clic en el botón **"Crear Tablas en la Base de Datos"**. El sistema ejecutará las sentencias DDL correspondientes creando las tablas sin necesidad de configurar scripts SQL manuales.

---

## Cómo alineé el proyecto con el clean_code.md del profesor

Después de revisar mi código contra `clean_code.md` de
https://github.com/ProfeBill/cheat-sheets hice estos cambios concretos:

1. **Type hints en todas las funciones**, tanto en parámetros como en el
   valor de retorno (`def calcular_ibl(ibc_ultimos_10: float, ibc_toda_vida: float) -> float`),
   en el modelo, el controlador, la consola y la GUI.
2. **Parámetros nombrados al invocar funciones**, por ejemplo
   `controlador.construir_datos(ibc_ultimos_10=..., ibc_toda_vida=..., ...)`
   en lugar de pasar los valores solo por posición.
3. **Excepciones con contexto**: creé una excepción base
   `ErrorCalculoPension` de la que heredan todas las excepciones de negocio.
   Cada excepción ahora explica **qué pasó, por qué pasó, con qué valor
   ocurrió y cómo se soluciona**.
4. **Se dejó de usar `except Exception` como manejo principal**: la consola
   y las vistas capturan excepciones específicas antes de cualquier captura general.
5. **Funciones más cortas y con una sola responsabilidad**: delegación en métodos privados y controladores dedicados.
6. **Uso de Blueprints en Flask**: separación estricta entre la configuración del servidor web (`app.py`) y las rutas operativas (`vista_pension.py`).

---

## Funcionalidad extra (en mis palabras)

Además de lo pedido en el enunciado, le agregué dos cosas a la GUI que no
vimos en clase:

**1. Simulador "¿qué pasa si cotizo más semanas?"**
Es un `Slider` de Kivy que aparece después de calcular una pensión. A
medida que uno mueve el control, la app recalcula la pensión en tiempo
real sumando esas semanas a las que ya cotizó.

**2. Guardar el resultado en un archivo**
Agregué un botón "GUARDAR EN ARCHIVO" que escribe el resultado (con fecha y
hora) en un archivo de texto utilizando `self.user_data_dir`.

---

## Ejecución

Requisito: **Python 3.10+**. Instalar dependencias:

```bash
pip install -r requirements.txt
```

### Aplicación Web (Local)

```bash
python -m src.view.web.app
```
Acceder en el navegador a: `http://127.0.0.1:5000/`

Para entorno de producción local con Gunicorn:
```bash
gunicorn src.view.web.app:app
```

### Interfaz gráfica (Kivy)

```bash
python src/view/gui/gui.py
```
o desde la raíz:
```bash
python main.py
```

### Interfaz de consola

```bash
python src/view/console/console.py
```

---

## Pruebas unitarias

Para ejecutar la suite completa de pruebas:

```bash
pytest -v
```
o mediante `unittest`:
```bash
python -m unittest discover -s tests -v
```

- `tests/test_pension.py`: Valida los casos matemáticos del modelo.
- `tests/test_controller.py`: Pruebas unitarias sobre los controladores.
- `tests/test_historial_controller.py`: Pruebas de integración con PostgreSQL (creación de tablas, inserción y consultas).
- `tests/test_web.py`: Pruebas sobre los endpoints y respuestas HTML del Blueprint de Flask.

---

## Base de datos (PostgreSQL en Render)

El historial de cálculos se guarda en PostgreSQL, en las tablas `persona`
y `calculopension` (una persona puede tener muchos cálculos).

### 1. Crear la base de datos
En Render, crear una base PostgreSQL y copiar sus datos de conexión
(host, puerto, nombre de la base, usuario y contraseña).

### 2. Configurar la conexión
1. Copiar `src/secret_config_sample.py` como `src/secret_config.py`.
2. Reemplazar los valores de ejemplo por los datos de su base.
3. **No subir `secret_config.py` al repositorio**: está en `.gitignore`.

### 3. Crear y administrar las tablas
- **Vía Web:** Pulsando el botón **"Crear Tablas en la Base de Datos"** desde la página de inicio.
- **Vía Consola:** Opción 4 del menú de consola.
- **Vía SQL:** Ejecutando los scripts `sql/crear_tablas.sql` o `sql/borrar_tablas.sql`.

---

## Cómo compilar y ejecutar el ejecutable de Windows (paso a paso)

1. Abrir una terminal en Windows en la raíz del proyecto.
2. Activar el entorno virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Instalar PyInstaller y dependencias:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```
4. Compilar:
   ```bash
   pyinstaller --onefile --windowed --name CalculadoraPensional main.py
   ```
5. El ejecutable queda en `dist\CalculadoraPensional.exe`.

---

## Cómo compilar y ejecutar el APK de Android (paso a paso)

### A. Preparar el entorno (WSL con Ubuntu)
1. Instalar WSL:
   ```bash
   wsl --install Ubuntu-22.04
   ```
2. Instalar paquetes necesarios:
   ```bash
   sudo apt update && sudo apt -y upgrade
   sudo apt install -y python3-pip git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   pip3 install --user --upgrade buildozer Cython==0.29.33 virtualenv
   ```

### B. Compilación
Dentro del repositorio clonado en WSL:
```bash
buildozer -v android debug
```
El archivo `.apk` resultante se genera en la carpeta `bin/`.

---

## Libro de casos de prueba

El archivo `doc/trabajofinalcasosdeprueba.xlsx` (casos normales, extraordinarios y de error) se corresponde con las pruebas automatizadas del proyecto.

## Control de versiones

Proyecto versionado con Git y alojado en GitHub. Las fases de consola, base de datos relacional en PostgreSQL, interfaz gráfica y aplicación web con Blueprints de Flask se integraron manteniendo la suite de pruebas unitarias operativa en todo momento.