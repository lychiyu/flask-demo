"""empty message

Revision ID: 287332cf8d8f
Revises: 
Create Date: 2017-11-29 11:32:43.637000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '287332cf8d8f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('newscate',
    sa.Column('cate_id', sa.Integer(), nullable=False),
    sa.Column('cate_name', sa.String(length=50), nullable=False),
    sa.Column('cate_title', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('cate_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=60), nullable=False),
    sa.Column('user_password', sa.String(length=30), nullable=False),
    sa.Column('user_nickname', sa.String(length=50), nullable=False),
    sa.Column('user_email', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('news',
    sa.Column('news_id', sa.Integer(), nullable=False),
    sa.Column('news_date', sa.DateTime(), nullable=False),
    sa.Column('news_content', sa.Text(), nullable=False),
    sa.Column('news_title', sa.String(length=100), nullable=False),
    sa.Column('news_excerpt', sa.Text(), nullable=False),
    sa.Column('news_status', sa.String(length=20), nullable=False),
    sa.Column('news_modified', sa.DateTime(), nullable=False),
    sa.Column('news_category', sa.Integer(), nullable=False),
    sa.Column('news_author', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['news_author'], ['user.user_id'], ),
    sa.ForeignKeyConstraint(['news_category'], ['newscate.cate_id'], ),
    sa.PrimaryKeyConstraint('news_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('news')
    op.drop_table('user')
    op.drop_table('newscate')
    # ### end Alembic commands ###
