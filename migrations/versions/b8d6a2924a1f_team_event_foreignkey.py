"""Team event foreignkey.

Revision ID: b8d6a2924a1f
Revises: 8d2ac14e0d02
Create Date: 2024-08-23 21:52:12.562662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'b8d6a2924a1f'
down_revision: Union[str, None] = '8d2ac14e0d02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###