-- # Overview
-- get text based on tags if provided

SELECT
    text_id
    , text

FROM texts
CROSS JOIN UNNEST(text_tags) AS tt

WHERE dt_requested IS NULL  -- not requested yet
{% if parsed_tags is not none %}
    AND tt = ANY(ARRAY[{{ parsed_tags }}])
{% endif %}

ORDER BY dt_entered {{ order }}
;