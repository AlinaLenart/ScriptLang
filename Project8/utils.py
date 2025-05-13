def is_error_code(code):
    try:
        code = int(code)
        return 400 <= code <= 599
    except (ValueError, TypeError):
        return False
