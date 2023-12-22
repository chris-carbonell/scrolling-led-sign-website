-- # Overview
-- get all texts for queue table

WITH

	-- tags
    -- unnest tags
    -- texts with NULL tags will not survive the CROSS JOIN
    tags AS (
		SELECT
			t.text_id
			, tag
		from texts t
		CROSS JOIN UNNEST(text_tags) AS tag
	)
	
	-- texts_tagged
    -- join unnested tags back onto texts
    -- so we can re-include texts with NULL tags
    , texts_tagged AS (
		SELECT
			texts.*
			, tags.tag
		FROM texts
		LEFT JOIN tags
		ON texts.text_id = tags.text_id
	)
	
	-- matches
    -- apply conditions
    , matches AS (
		SELECT DISTINCT
			t.text_id
		
		FROM texts_tagged t
		
        WHERE 1 = 1

        {% if requested == true %}
            AND t.dt_requested IS NOT NULL  -- requested already
        {% elif requested == false %}
            AND t.dt_requested IS NULL  -- not requested yet
        {% else %}
        {% endif %}

        {% if parsed_tags is not none %}
            AND tag = ANY(ARRAY[{{ parsed_tags }}])
        {% endif %}
	)

SELECT
    t.*

FROM texts t

INNER JOIN matches m
ON t.text_id = m.text_id

ORDER BY t.dt_entered {{ 'ASC' if asc == true else 'DESC' }}

LIMIT {{ 'ALL' if limit is none else limit }}
;