"""empty message

Revision ID: f0e369183184
Revises: f22525a15eff
Create Date: 2022-07-19 21:44:20.855326

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f0e369183184'
down_revision = 'f22525a15eff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('INCOME', 'EXPENSE', 'ACCOUNT', name='categorytype'), nullable=False),
    sa.Column('starting_balance', sa.Numeric(precision=16, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'name', name='user_category_uc')
    )
    op.create_index(op.f('ix_category_user_id'), 'category', ['user_id'], unique=False)
    op.create_table('transaction',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('category_from_id', sa.Integer(), nullable=False),
    sa.Column('category_to_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=16, scale=2), nullable=False),
    sa.Column('type', sa.Enum('INCOME', 'EXPENSE', 'TRANSFER', name='transactiontype'), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['category_from_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['category_to_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transaction_category_from_id'), 'transaction', ['category_from_id'], unique=False)
    op.create_index(op.f('ix_transaction_category_to_id'), 'transaction', ['category_to_id'], unique=False)
    op.create_index(op.f('ix_transaction_created'), 'transaction', ['created'], unique=False)
    op.create_index(op.f('ix_transaction_user_id'), 'transaction', ['user_id'], unique=False)
    op.alter_column('user', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_index(op.f('ix_transaction_user_id'), table_name='transaction')
    op.drop_index(op.f('ix_transaction_created'), table_name='transaction')
    op.drop_index(op.f('ix_transaction_category_to_id'), table_name='transaction')
    op.drop_index(op.f('ix_transaction_category_from_id'), table_name='transaction')
    op.drop_table('transaction')
    op.drop_index(op.f('ix_category_user_id'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###
