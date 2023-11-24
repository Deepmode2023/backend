"""create table spaced_repetitions

Revision ID: f2fd2400f645
Revises: d12e4ad52c1d
Create Date: 2023-11-21 12:39:16.214632

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2fd2400f645'
down_revision: Union[str, None] = 'd12e4ad52c1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spaced_repetition',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slug', sa.String(length=20), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('count_repetition', sa.Integer(), nullable=True),
    sa.Column('date_repitition', sa.DateTime(timezone=True), nullable=False),
    sa.Column('date_last_repetition', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('shared_preference_user_id_fkey', 'shared_preference', type_='foreignkey')
    op.create_foreign_key(None, 'shared_preference', 'users', ['user_id'], ['user_id'], ondelete='CASCADE')
    op.drop_constraint('words_user_id_fkey', 'words', type_='foreignkey')
    op.create_foreign_key(None, 'words', 'users', ['user_id'], ['user_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'words', type_='foreignkey')
    op.create_foreign_key('words_user_id_fkey', 'words', 'users', ['user_id'], ['user_id'])
    op.drop_constraint(None, 'shared_preference', type_='foreignkey')
    op.create_foreign_key('shared_preference_user_id_fkey', 'shared_preference', 'users', ['user_id'], ['user_id'])
    op.drop_table('spaced_repetition')
    # ### end Alembic commands ###
