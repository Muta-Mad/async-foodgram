from typing import Annotated

from pydantic import StringConstraints


USERNAME = Annotated[
    str,
    StringConstraints(
        max_length=150,
        pattern=r'^[\w.@+-]+$'
    )
]