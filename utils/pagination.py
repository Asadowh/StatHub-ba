def paginate(query, page: int = 1, limit: int = 20):
    page = max(page, 1)
    offset = (page - 1) * limit
    return query.offset(offset).limit(limit)
