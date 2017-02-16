revision = '7c8dfa3d56a9'
down_revision = '59574a5cc5e5'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('post_account_id_fkey', 'post', type_='foreignkey')
    op.create_foreign_key(None, 'post', 'account', ['account_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.create_foreign_key('post_account_id_fkey', 'post', 'user', ['account_id'], ['id'])
    ### end Alembic commands ###
