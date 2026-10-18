INSERT INTO persona (cedula, nombre)
VALUES ('123456', 'Ana Pérez');

INSERT INTO calculopension (
    persona_id, ibc_ultimos_10, ibc_toda_vida, salario_minimo_legal,
    semanas_cotizadas, edad, sexo, ibl, tasa_total, pension, fecha
)
VALUES (
    (SELECT id FROM persona WHERE cedula = '123456'),
    9800000, 10000000, 2000000,
    1300, 65, 'M', 10000000, 63, 6300000, NOW()
);