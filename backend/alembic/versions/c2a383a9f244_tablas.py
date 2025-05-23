"""tablas 

Revision ID: c2a383a9f244
Revises: 
Create Date: 2025-03-22 17:21:07.509691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2a383a9f244'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alergias',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('nombre', sa.String(255), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('nombre')
                    )
    op.create_table('categorias',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('nombre', sa.String(255), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('nombre')
                    )
    op.create_table('ingredientes',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('nombre', sa.String(255), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('nombre')
                    )
    op.create_table('recetas',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('titulo', sa.String(255), nullable=False),
                    sa.Column('descripcion', sa.Text(), nullable=False),
                    sa.Column('pasos', sa.Text(), nullable=False),
                    sa.Column('categoria_id', sa.Integer(), nullable=True),
                    sa.Column('imagen', sa.String(255), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['categoria_id'], ['categorias.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_recetas_titulo'),
                    'recetas', ['titulo'], unique=False)
    op.create_table('receta_alergias',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('receta_id', sa.Integer(), nullable=True),
                    sa.Column('alergia_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['alergia_id'], ['alergias.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['receta_id'], ['recetas.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('recetas_ingredientes',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('receta_id', sa.Integer(), nullable=True),
                    sa.Column('ingrediente_id', sa.Integer(), nullable=True),
                    sa.Column('cantidad', sa.String(255), nullable=False),
                    sa.Column('unidad', sa.String(255), nullable=False),
                    sa.ForeignKeyConstraint(['ingrediente_id'], [
                        'ingredientes.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['receta_id'], ['recetas.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('valoraciones',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('recetas_id', sa.Integer(), nullable=True),
                    sa.Column('puntuacion', sa.Integer(), nullable=False),
                    sa.Column('comentarios', sa.Text(), nullable=True),
                    sa.Column('fecha', sa.TIMESTAMP(), nullable=False),
                    sa.CheckConstraint('puntuacion BETWEEN 1 AND 5',
                                       name='chk_puntuacion'),
                    sa.ForeignKeyConstraint(
                        ['recetas_id'], ['recetas.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('valoraciones')
    op.drop_table('recetas_ingredientes')
    op.drop_table('receta_alergias')
    op.drop_index(op.f('ix_recetas_titulo'), table_name='recetas')
    op.drop_table('recetas')
    op.drop_table('ingredientes')
    op.drop_table('categorias')
    op.drop_table('alergias')
    # ### end Alembic commands ###
