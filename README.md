Cálculo de Pensión de Vejez en Colombia (Régimen de Prima Media)

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

2. Calcular la tasa de reemplazo. Si la persona sí cumple los requisitos, se calcula qué porcentaje del IBL le corresponde recibir como pensión mensual (la "tasa de reemplazo"). Este porcentaje no es fijo: depende de qué tan alto es el ingreso de la persona y de cuántas semanas cotizó por encima del mínimo. La lógica es la siguiente:

Se calcula cuántos salarios mínimos representa el IBL (dividiendo el IBL entre el SMLMV).
A partir de ahí, la tasa de reemplazo parte de un 65,5% y disminuye 0,5% por cada salario mínimo adicional que representa el ingreso: entre más gana la persona, menor es el porcentaje que recibe sobre su IBL. Esta tasa base nunca puede bajar del 55%, sin importar qué tan alto sea el ingreso.
Si la persona cotizó más de las 1.300 semanas mínimas, la tasa aumenta 1,5 puntos porcentuales por cada bloque completo de 50 semanas adicionales. Los bloques incompletos (por ejemplo, 49 semanas de más) todavía no cuentan.
La tasa final —ya con el aumento por semanas adicionales incluido— nunca puede superar el 80%, sin importar cuántas semanas adicionales tenga la persona.

3. Calcular el valor de la pensión. El valor mensual de la pensión es el IBL multiplicado por la tasa de reemplazo obtenida en el paso anterior. Pero existe una garantía adicional: ninguna pensión reconocida puede ser inferior a 1 SMLMV. Si el resultado de la multiplicación da un valor menor al salario mínimo, se paga el salario mínimo en su lugar.

Salidas
El sistema debe producir uno de estos dos tipos de resultado:

-Si la persona cumple los requisitos: el valor mensual de la pensión, en pesos, ya con la garantía del mínimo aplicada si corresponde.

-Si la persona no cumple los requisitos, o si alguno de los datos de entrada es inválido (por ejemplo, un IBL o un SMLMV menor o igual a cero, o un número de semanas negativo): un mensaje de error que indique con precisión cuál fue el problema, en lugar de un valor numérico. Esto es intencional: el sistema no debe intentar "adivinar" o forzar un cálculo con datos que no tienen sentido.
