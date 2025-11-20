"""merge heads

Revision ID: 7a90e97b270c
Revises: 2cbecb1f49b7, 56df70aac723
Create Date: 2025-11-17 17:48:15.891996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a90e97b270c'
down_revision: Union[str, Sequence[str], None] = ('2cbecb1f49b7', '56df70aac723')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
