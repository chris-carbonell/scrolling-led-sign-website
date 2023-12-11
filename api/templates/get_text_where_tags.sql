-- # Overview
-- get text based on tags if provided

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

        WHERE dt_requested IS NULL  -- not requested yet
        {% if parsed_tags is not none %}
            AND tt = ANY(ARRAY[{{ parsed_tags }}])
        {% endif %}

        ORDER BY dt_entered {{ 'ASC' if asc == true else 'DESC' }}        
    )

SELECT
    text_id
    , text

FROM matches

LIMIT 1
;