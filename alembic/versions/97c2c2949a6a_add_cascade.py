"""add cascade

Revision ID: 97c2c2949a6a
Revises: aa0f11451203
Create Date: 2023-10-27 19:24:36.944957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97c2c2949a6a'
down_revision: Union[str, None] = 'aa0f11451203'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_task_association_task_id_fkey', 'user_task_association', type_='foreignkey')
    op.drop_constraint('user_task_association_user_id_fkey', 'user_task_association', type_='foreignkey')
    op.create_foreign_key(None, 'user_task_association', 'tasks', ['task_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'user_task_association', 'users', ['user_id'], ['user_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_task_association', type_='foreignkey')
    op.drop_constraint(None, 'user_task_association', type_='foreignkey')
    op.create_foreign_key('user_task_association_user_id_fkey', 'user_task_association', 'users', ['user_id'], ['user_id'])
    op.create_foreign_key('user_task_association_task_id_fkey', 'user_task_association', 'tasks', ['task_id'], ['id'])
    # ### end Alembic commands ###