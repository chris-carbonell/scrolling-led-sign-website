-- # Overview
-- get all texts for queue table

WITH

    -- matches
    -- get text_id that matches tags
    matches AS (
        SELECT DISTINCT
            text_id
            , dt_entered
            , text

        FROM texts
        CROSS JOIN UNNEST(text_tags) AS tt

        {% if parsed_tags is not none %}
            WHERE tt = ANY(ARRAY[{{ parsed_tags }}])
        {% endif %}
    )

SELECT
    t.*

FROM texts t

INNER JOIN matches m
ON t.text_id = m.text_id

ORDER BY dt_entered {{ 'ASC' if asc == true else 'DESC' }}

LIMIT {{ limit if limit is not none else 'ALL' }}
;