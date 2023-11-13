def calculate_pagination_page(limmit: int, skip: int, pagination: int = 0):
    if skip <= 0 or skip < limmit:
        return pagination
    pagination += 1
    return calculate_pagination_page(
        limmit=limmit, skip=skip-limmit, pagination=pagination)
