"""initial database

Revision ID: 5be52a5b9180
Revises: 
Create Date: 2017-01-27 16:27:10.107522

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.types import Text

# revision identifiers, used by Alembic.
revision = '5be52a5b9180'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('expected_stream',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('method', sa.String(), nullable=False),
                    sa.Column('expected_rate', sa.Float(), nullable=False),
                    sa.Column('warn_interval', sa.Integer(), nullable=False),
                    sa.Column('fail_interval', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name', 'method')
                    )

    op.create_table('pending_update',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('message', postgresql.JSON(astext_type=Text()), nullable=False),
                    sa.Column('error_count', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('reference_designator',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )

    op.create_table('deployed_stream',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('reference_designator_id', sa.Integer(), nullable=False),
                    sa.Column('expected_stream_id', sa.Integer(), nullable=False),
                    sa.Column('particle_count', sa.Integer(), nullable=False),
                    sa.Column('last_seen', sa.DateTime(), nullable=False),
                    sa.Column('collected', sa.DateTime(), nullable=False),
                    sa.Column('expected_rate', sa.Float(), nullable=True),
                    sa.Column('warn_interval', sa.Integer(), nullable=True),
                    sa.Column('fail_interval', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['expected_stream_id'], ['expected_stream.id'], ),
                    sa.ForeignKeyConstraint(['reference_designator_id'], ['reference_designator.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('reference_designator_id', 'expected_stream_id')
                    )

    op.create_table('port_count',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('reference_designator_id', sa.Integer(), nullable=False),
                    sa.Column('collected_time', sa.DateTime(), nullable=False),
                    sa.Column('byte_count', sa.Integer(), nullable=True),
                    sa.Column('seconds', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['reference_designator_id'], ['reference_designator.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('stream_condition',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('stream_id', sa.Integer(), nullable=False),
                    sa.Column('last_status_time', sa.DateTime(), nullable=False),
                    sa.Column('last_status', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['stream_id'], ['deployed_stream.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('stream_id')
                    )


def downgrade():
    op.drop_table('stream_condition')
    op.drop_table('port_count')
    op.drop_table('deployed_stream')
    op.drop_table('reference_designator')
    op.drop_table('pending_update')
    op.drop_table('expected_stream')
