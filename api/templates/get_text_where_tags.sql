-- # Overview
-- get text based on tags if provided

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
		SELECT
			t.text_id
			, t.text
		
		FROM texts_tagged t
		
		WHERE t.dt_requested IS NULL  -- not requested yet
        {% if parsed_tags is not none %}
            AND tag = ANY(ARRAY[{{ parsed_tags }}])
        {% endif %}
		
		ORDER BY dt_entered {{ 'ASC' if asc == true else 'DESC' }}        
	)
	
SELECT
	*
FROM matches
LIMIT 1
;