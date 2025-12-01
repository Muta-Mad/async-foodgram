from fastapi import HTTPException, status


def not_found_error(name: str):
    """Вызывает 404 если объект не найден."""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'{name} с таким ID не существует.',
    )
