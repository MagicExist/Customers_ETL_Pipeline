-- Curated table uses typed columns and constraints expected after transformation.
CREATE TABLE customers (
 id SERIAL PRIMARY KEY,
 full_name VARCHAR(100),
 email VARCHAR(255) UNIQUE,
 phone VARCHAR(20),
 city VARCHAR(100),
 country VARCHAR(100),
 birth_date DATE,
 created_at TIMESTAMP,
 total_spent NUMERIC(10,2),
 is_active BOOLEAN
)
