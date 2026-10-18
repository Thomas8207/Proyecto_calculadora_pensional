SELECT p.cedula, p.nombre, c.fecha, c.semanas_cotizadas,
       c.edad, c.sexo, c.ibl, c.tasa_total, c.pension
FROM calculopension c
JOIN persona p ON p.id = c.persona_id
WHERE p.cedula = '123456'
ORDER BY c.id DESC;