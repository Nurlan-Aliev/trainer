"""relationship

Revision ID: e6b9d5d3aef0
Revises: 236a2f42bf53
Create Date: 2025-12-05 21:40:32.776207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6b9d5d3aef0'
down_revision: Union[str, Sequence[str], None] = '236a2f42bf53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
