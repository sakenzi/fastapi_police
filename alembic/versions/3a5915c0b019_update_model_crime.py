"""update model crime

Revision ID: 3a5915c0b019
Revises: f189d884cd84
Create Date: 2025-03-12 14:18:32.189504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry
import geoalchemy2

# revision identifiers, used by Alembic.
revision: str = '3a5915c0b019'
down_revision: Union[str, None] = 'f189d884cd84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('crimes', sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True))
    op.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_indexes 
                WHERE indexname = 'idx_crimes_geom'
            ) THEN
                CREATE INDEX idx_crimes_geom ON crimes USING GIST (geom);
            END IF;
        END $$;
    """)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_crimes_geom', table_name='crimes', postgresql_using='gist')
    op.drop_column('crimes', 'geom')
    # ### end Alembic commands ###
