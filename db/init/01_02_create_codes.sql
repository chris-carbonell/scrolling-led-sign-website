CREATE TABLE IF NOT EXISTS codes (
    code_id SERIAL PRIMARY KEY,
    dt_entered TIMESTAMP WITH TIME ZONE,
    code VARCHAR(255),
    is_admin BOOLEAN
);