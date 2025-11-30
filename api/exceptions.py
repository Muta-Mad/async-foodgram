from fastapi import HTTPException, status


def not_found_error(result, message):
    """Вызывает 404 если объект не найден."""
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )
