-- # Overview
-- add/insert text data

INSERT INTO texts (
    dt_entered, 
    client_host, 
    text_source, 
    text_tags, 
    text
    ) 

VALUES (
    '{{ dt_entered }}',
    '{{ client_host }}',
    '{{ text_source }}',
    ARRAY[{{ parsed_tags }}],
    '{{ text }}'
)
;