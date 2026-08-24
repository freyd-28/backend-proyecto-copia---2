from flask import request

def paginate_query(query, default_limit=10, max_limit=100):
    """
    Toma una consulta de SQLAlchemy y aplica paginación basada en los query params de la petición.
    """
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', default_limit))
    except ValueError:
        page = 1
        limit = default_limit

    page = max(1, page)
    limit = max(1, min(limit, max_limit))

    total_items = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all()
    total_pages = (total_items + limit - 1) // limit if limit > 0 else 0

    return {
        'items': items,
        'pagination': {
            'total_items': total_items,
            'total_pages': total_pages,
            'current_page': page,
            'limit': limit,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }