-- Raw table keeps source values as text so inconsistent formats can be landed first.
CREATE TABLE customers (
 id SERIAL PRIMARY KEY,
 full_name VARCHAR(30),
 email VARCHAR(255),
 phone VARCHAR(20),
 city VARCHAR(100),
 country VARCHAR(100),
 birth_date VARCHAR(100),
 created_at VARCHAR(100),
 total_spent VARCHAR(100),
 is_active VARCHAR(5)
)

-- Sample source rows intentionally include nulls, mixed casing, duplicates, and bad formats.

INSERT INTO customers (
    full_name,
    email,
    phone,
    city,
    country,
    birth_date,
    created_at,
    total_spent,
    is_active
)
VALUES
('  Juan Pérez ', 'JUAN.PEREZ@EMAIL.COM ', '3001234567', 'medellin', 'colombia', '1999-05-14', '2026-03-01 10:15:00', '150000.50', 'yes'),

('maria gomez', 'maria.gmail.com', ' 301-555-8899 ', 'Bogotá ', 'Colombia', '14/08/2001', '2026/03/02 08:00:00', '98000', 'true'),

('Carlos Ruiz', NULL, NULL, 'cali', 'colombia', NULL, '2026-03-02 11:30:00', NULL, '1'),

('   Ana   Torres   ', 'ana.torres@email.com', 'abc123', 'MEDELLIN', 'COLOMBIA', '2000-11-30', 'March 3, 2026 14:20:00', '-5000', 'no'),

('', 'pedro.lopez@email.com', '3009991111', NULL, 'colombia', '2002-02-29', '2026-03-03 09:45:00', '20000.999', 'False'),

('Laura Moreno', 'laura.moreno@email.com ', '+57 300 888 7777', 'Barranquilla', 'Colombia ', '1998/07/21', '2026-03-03T16:10:00', '0', 'TRUE'),

('Juan Pérez', 'juan.perez@email.com', '3001234567', 'Medellín', 'Colombia', '1999-05-14', '2026-03-04 10:15:00', '150000.50', 'yes'),

('Sofía Ramírez', 'sofia.ramirez@email', '300-000-0000', 'Cartagena', 'Colombia', '2003-12-01', NULL, 'not available', NULL),

('Andres Felipe', 'andres.felipe@email.com', '   ', '   cucuta', 'colombia', '1997-01-09', '2026-03-05 07:00:00', '45000', '0'),

('Luisa Fernández', 'LUISA@EMAIL.COM', '3204445566', 'Bogota', 'COL', '2004-06-18', '2026-03-05 18:25:00', '75000.5', 'Yes');
