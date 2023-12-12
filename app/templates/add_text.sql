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

    {% if parsed_tags is not none %}
        ARRAY[{{ parsed_tags }}],
    {% else %}
        NULL,
    {% endif %}

    '{{ text }}'
)
;