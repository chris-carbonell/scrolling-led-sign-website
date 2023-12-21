def parse_tags(tags: str | None):
    '''
    convert "a,b, c" to "'a', 'b', 'c'"
    for use with ARRAY[]
    '''
    if tags:
        tags_where = ["'" + tag.strip() + "'" for tag in tags.split(",")]
        return ", ".join(tags_where)
    else:
        return None