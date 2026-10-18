CREATE TABLE persona (
    id SERIAL PRIMARY KEY,
    cedula VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE calculopension (
    id SERIAL PRIMARY KEY,
    persona_id INTEGER NOT NULL REFERENCES persona (id) ON DELETE CASCADE,
    ibc_ultimos_10 DOUBLE PRECISION NOT NULL,
    ibc_toda_vida DOUBLE PRECISION NOT NULL,
    salario_minimo_legal INTEGER NOT NULL,
    semanas_cotizadas INTEGER NOT NULL,
    edad INTEGER NOT NULL,
    sexo VARCHAR(1) NOT NULL,
    ibl DOUBLE PRECISION NOT NULL,
    tasa_total DOUBLE PRECISION NOT NULL,
    pension DOUBLE PRECISION NOT NULL,
    fecha TIMESTAMP NOT NULL
);