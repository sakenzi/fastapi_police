"""update-user

Revision ID: 7f9fe7d71f78
Revises: 51b8f2cb66d0
Create Date: 2025-03-06 14:04:49.591918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f9fe7d71f78'
down_revision: Union[str, None] = '51b8f2cb66d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
