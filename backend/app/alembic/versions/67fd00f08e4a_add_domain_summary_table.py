"""Add domain summary table

Revision ID: 67fd00f08e4a
Revises: e2412789c190
Create Date: 2024-03-12 12:28:38.079251

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '67fd00f08e4a'
down_revision = 'e2412789c190'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('domainsummary',
    sa.Column('ted_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('uniprot_acc', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('md5_domain', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('consensus_level', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('chopping', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('nres_domain', sa.Integer(), nullable=False),
    sa.Column('num_segments', sa.Integer(), nullable=False),
    sa.Column('plddt', sa.Float(), nullable=False),
    sa.Column('num_helix_strand_turn', sa.Integer(), nullable=False),
    sa.Column('num_helix', sa.Integer(), nullable=False),
    sa.Column('num_strand', sa.Integer(), nullable=False),
    sa.Column('num_helix_strand', sa.Integer(), nullable=False),
    sa.Column('num_turn', sa.Integer(), nullable=False),
    sa.Column('proteome_id', sa.Integer(), nullable=False),
    sa.Column('cath_label', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('cath_assignment_level', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('cath_assignment_method', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('packing_density', sa.Float(), nullable=False),
    sa.Column('norm_rg', sa.Float(), nullable=False),
    sa.Column('tax_common_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('tax_scientific_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('tax_lineage', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('ted_id')
    )
    op.create_index(op.f('ix_domainsummary_consensus_level'), 'domainsummary', ['consensus_level'], unique=False)
    op.create_index(op.f('ix_domainsummary_md5_domain'), 'domainsummary', ['md5_domain'], unique=False)
    op.create_index(op.f('ix_domainsummary_proteome_id'), 'domainsummary', ['proteome_id'], unique=False)
    op.create_index(op.f('ix_domainsummary_tax_scientific_name'), 'domainsummary', ['tax_scientific_name'], unique=False)
    op.create_index(op.f('ix_domainsummary_uniprot_acc'), 'domainsummary', ['uniprot_acc'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_domainsummary_uniprot_acc'), table_name='domainsummary')
    op.drop_index(op.f('ix_domainsummary_tax_scientific_name'), table_name='domainsummary')
    op.drop_index(op.f('ix_domainsummary_proteome_id'), table_name='domainsummary')
    op.drop_index(op.f('ix_domainsummary_md5_domain'), table_name='domainsummary')
    op.drop_index(op.f('ix_domainsummary_consensus_level'), table_name='domainsummary')
    op.drop_table('domainsummary')
    # ### end Alembic commands ###
