"""Add role column to groups_tenants_table

Revision ID: 7aae863786af
Revises: 406821843b55
Create Date: 2017-10-04 11:10:48.227654

"""
from alembic import op
import sqlalchemy as sa
import manager_rest     # Adding this manually


# revision identifiers, used by Alembic.
revision = '7aae863786af'
down_revision = '406821843b55'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'groups_tenants',
        sa.Column('role_id', sa.Integer()),
    )
    op.create_foreign_key(
        'groups_tenants_role_id_fkey',
        'groups_tenants',
        'roles',
        ['role_id'],
        ['id'],
    )
    op.create_primary_key(
        'groups_tenants_pkey',
        'groups_tenants',
        ['group_id', 'tenant_id'],
    )


def downgrade():
    op.drop_constraint(
        'groups_tenants_pkey',
        'groups_tenants',
    )
    op.drop_constraint(
        'groups_tenants_role_id_fkey',
        'groups_tenants',
    )
    op.drop_column('groups_tenants', 'role_id')