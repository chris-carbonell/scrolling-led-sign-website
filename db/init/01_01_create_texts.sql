CREATE TABLE IF NOT EXISTS texts (
    text_id SERIAL PRIMARY KEY,
    dt_entered TIMESTAMP WITH TIME ZONE,
    dt_requested TIMESTAMP WITH TIME ZONE,
    client_host VARCHAR(16),
    text_source VARCHAR(255),
    name VARCHAR(255),
    text_tags VARCHAR(255) ARRAY,
    text TEXT
);