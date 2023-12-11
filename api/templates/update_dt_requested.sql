-- # Overview
-- update dt_requested for a given text_id

UPDATE texts 
SET dt_requested = '{{ dt_requested }}'
WHERE text_id = {{ text_id }}
;