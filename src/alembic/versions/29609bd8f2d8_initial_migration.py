"""initial migration

Revision ID: 29609bd8f2d8
Revises: 
Create Date: 2024-11-01 14:28:51.528965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29609bd8f2d8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('diver_profiles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('full_name', sa.String(length=100), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_diver_profiles_id'), 'diver_profiles', ['id'], unique=False)
    op.create_table('master_brands',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('label', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_master_brands_id'), 'master_brands', ['id'], unique=False)
    op.create_table('master_colors',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('label', sa.String(length=50), nullable=False),
    sa.Column('hex_code', sa.String(length=10), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_master_colors_id'), 'master_colors', ['id'], unique=False)
    op.create_table('master_dive_preferences',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('label', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_master_dive_preferences_id'), 'master_dive_preferences', ['id'], unique=False)
    op.create_table('master_dive_sites',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('label', sa.String(length=100), nullable=False),
    sa.Column('latitude', sa.DECIMAL(precision=10, scale=8), nullable=False),
    sa.Column('longitude', sa.DECIMAL(precision=11, scale=8), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_master_dive_sites_id'), 'master_dive_sites', ['id'], unique=False)
    op.create_table('master_dive_types',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('label', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_master_dive_types_id'), 'master_dive_types', ['id'], unique=False)
    op.create_table('master_gears',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('label', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_master_gears_id'), 'master_gears', ['id'], unique=False)
    op.create_table('master_licenses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('issuer', sa.String(length=50), nullable=False),
    sa.Column('alias', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_master_licenses_id'), 'master_licenses', ['id'], unique=False)
    op.create_table('master_love_tos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('label', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_master_love_tos_id'), 'master_love_tos', ['id'], unique=False)
    op.create_table('master_marine_lifes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('label', sa.String(length=100), nullable=False),
    sa.Column('image_url', sa.String(length=1000), nullable=False),
    sa.Column('image_credit', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_master_marine_lifes_id'), 'master_marine_lifes', ['id'], unique=False)
    op.create_table('master_previous_dive_sites',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('label', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_master_previous_dive_sites_id'), 'master_previous_dive_sites', ['id'], unique=False)
    op.create_table('onboarding_profiles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=True),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', 'PREFER_NOT_TO_SAY', 'ATTACK_APACHE_HELICOPTER', name='genderenum'), nullable=True),
    sa.Column('start_diving', sa.Date(), nullable=True),
    sa.Column('last_time_diving', sa.Date(), nullable=True),
    sa.Column('current_logs', sa.Integer(), nullable=True),
    sa.Column('last_certification', sa.Enum('OPEN_WATER', 'ADVANCED_OPEN_WATER', 'RESCUE_DIVER', 'DIVE_MASTER', 'DIVE_INSTRUCTOR', name='certificationenum'), nullable=True),
    sa.Column('certification_issuer', sa.Enum('PADI', 'SSI', 'POSSI', 'OTHER', name='certificationissuerenum'), nullable=True),
    sa.Column('want_to_see', sa.Enum('CORALS', 'MACRO', 'PELAGIC', 'OTHER', name='wanttoseeenum'), nullable=True),
    sa.Column('dive_current_condition', sa.Enum('INDEPENDENT', 'NEED_HELP', 'PREFER_NOT_DIVE', 'OTHER', name='diveconditionenum'), nullable=True),
    sa.Column('bottom_time', sa.Enum('UNDER_30', 'BETWEEN_31_40', 'BETWEEN_41_50', 'BETWEEN_51_60', 'MORE_THAN_60', 'OTHER', name='bottomtimeenum'), nullable=True),
    sa.Column('trouble_equalizing', sa.Enum('NEVER', 'SOMETIMES', 'OFTEN', 'ALWAYS', 'OTHER', name='troubleequalizingenum'), nullable=True),
    sa.Column('photographer', sa.Boolean(), nullable=True),
    sa.Column('information', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_onboarding_profiles_id'), 'onboarding_profiles', ['id'], unique=False)
    op.create_index(op.f('ix_onboarding_profiles_user_id'), 'onboarding_profiles', ['user_id'], unique=False)
    op.create_table('dive_logs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('diver_profile_id', sa.Integer(), nullable=False),
    sa.Column('master_dive_site_id', sa.Integer(), nullable=False),
    sa.Column('master_dive_type_id', sa.Integer(), nullable=False),
    sa.Column('dive_suit', sa.Enum('DRY_SUIT', 'WET_SUIT', 'OTHER', name='divesuitenum'), nullable=True),
    sa.Column('dive_log_date', sa.DateTime(), nullable=False),
    sa.Column('time_in', sa.Time(), nullable=True),
    sa.Column('time_out', sa.Time(), nullable=True),
    sa.Column('max_depth', sa.SmallInteger(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['diver_profile_id'], ['diver_profiles.id'], ),
    sa.ForeignKeyConstraint(['master_dive_site_id'], ['master_dive_sites.id'], ),
    sa.ForeignKeyConstraint(['master_dive_type_id'], ['master_dive_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dive_logs_id'), 'dive_logs', ['id'], unique=False)
    op.create_table('dive_preferences',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('diver_profile_id', sa.Integer(), nullable=False),
    sa.Column('master_dive_preference_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['diver_profile_id'], ['diver_profiles.id'], ),
    sa.ForeignKeyConstraint(['master_dive_preference_id'], ['master_dive_preferences.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('diver_profile_id', 'master_dive_preference_id', name='uix_diver_master_preference')
    )
    op.create_index(op.f('ix_dive_preferences_id'), 'dive_preferences', ['id'], unique=False)
    op.create_table('diver_additional_data',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('diver_profile_id', sa.Integer(), nullable=False),
    sa.Column('total_dive_log', sa.Integer(), nullable=False),
    sa.Column('total_visited_dive_site', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['diver_profile_id'], ['diver_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_diver_additional_data_id'), 'diver_additional_data', ['id'], unique=False)
    op.create_table('diver_licenses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('diver_profile_id', sa.Integer(), nullable=False),
    sa.Column('master_license_id', sa.Integer(), nullable=False),
    sa.Column('certification_number', sa.String(length=100), nullable=False),
    sa.Column('certificate_date', sa.Date(), nullable=True),
    sa.Column('birth_date_license', sa.Date(), nullable=True),
    sa.Column('instructor_name', sa.String(length=100), nullable=True),
    sa.Column('instructor_number', sa.Integer(), nullable=True),
    sa.Column('store_name', sa.String(length=100), nullable=True),
    sa.Column('store_number', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['diver_profile_id'], ['diver_profiles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['master_license_id'], ['master_licenses.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_diver_licenses_id'), 'diver_licenses', ['id'], unique=False)
    op.create_table('favorite_marine_lifes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('diver_profile_id', sa.Integer(), nullable=False),
    sa.Column('master_marine_life_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['diver_profile_id'], ['diver_profiles.id'], ),
    sa.ForeignKeyConstraint(['master_marine_life_id'], ['master_marine_lifes.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('diver_profile_id', 'master_marine_life_id', name='uix_diver_master_favorite_marine_life')
    )
    op.create_index(op.f('ix_favorite_marine_lifes_id'), 'favorite_marine_lifes', ['id'], unique=False)
    op.create_table('master_gears_brands',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('master_gear_id', sa.Integer(), nullable=False),
    sa.Column('master_brand_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['master_brand_id'], ['master_brands.id'], ),
    sa.ForeignKeyConstraint(['master_gear_id'], ['master_gears.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_master_gears_brands_id'), 'master_gears_brands', ['id'], unique=False)
    op.create_table('profile_love_tos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('onboarding_profile_id', sa.Integer(), nullable=False),
    sa.Column('master_love_to_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['master_love_to_id'], ['master_love_tos.id'], ),
    sa.ForeignKeyConstraint(['onboarding_profile_id'], ['onboarding_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profile_love_tos_id'), 'profile_love_tos', ['id'], unique=False)
    op.create_table('profile_previous_dive_sites',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('onboarding_profile_id', sa.Integer(), nullable=False),
    sa.Column('master_previous_dive_site_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['master_previous_dive_site_id'], ['master_previous_dive_sites.id'], ),
    sa.ForeignKeyConstraint(['onboarding_profile_id'], ['onboarding_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profile_previous_dive_sites_id'), 'profile_previous_dive_sites', ['id'], unique=False)
    op.create_table('diver_gears',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('diver_profile_id', sa.Integer(), nullable=False),
    sa.Column('master_gears_brand_id', sa.Integer(), nullable=False),
    sa.Column('master_color_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['diver_profile_id'], ['diver_profiles.id'], ),
    sa.ForeignKeyConstraint(['master_color_id'], ['master_colors.id'], ),
    sa.ForeignKeyConstraint(['master_gears_brand_id'], ['master_gears_brands.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_diver_gears_id'), 'diver_gears', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_diver_gears_id'), table_name='diver_gears')
    op.drop_table('diver_gears')
    op.drop_index(op.f('ix_profile_previous_dive_sites_id'), table_name='profile_previous_dive_sites')
    op.drop_table('profile_previous_dive_sites')
    op.drop_index(op.f('ix_profile_love_tos_id'), table_name='profile_love_tos')
    op.drop_table('profile_love_tos')
    op.drop_index(op.f('ix_master_gears_brands_id'), table_name='master_gears_brands')
    op.drop_table('master_gears_brands')
    op.drop_index(op.f('ix_favorite_marine_lifes_id'), table_name='favorite_marine_lifes')
    op.drop_table('favorite_marine_lifes')
    op.drop_index(op.f('ix_diver_licenses_id'), table_name='diver_licenses')
    op.drop_table('diver_licenses')
    op.drop_index(op.f('ix_diver_additional_data_id'), table_name='diver_additional_data')
    op.drop_table('diver_additional_data')
    op.drop_index(op.f('ix_dive_preferences_id'), table_name='dive_preferences')
    op.drop_table('dive_preferences')
    op.drop_index(op.f('ix_dive_logs_id'), table_name='dive_logs')
    op.drop_table('dive_logs')
    op.drop_index(op.f('ix_onboarding_profiles_user_id'), table_name='onboarding_profiles')
    op.drop_index(op.f('ix_onboarding_profiles_id'), table_name='onboarding_profiles')
    op.drop_table('onboarding_profiles')
    op.drop_index(op.f('ix_master_previous_dive_sites_id'), table_name='master_previous_dive_sites')
    op.drop_table('master_previous_dive_sites')
    op.drop_index(op.f('ix_master_marine_lifes_id'), table_name='master_marine_lifes')
    op.drop_table('master_marine_lifes')
    op.drop_index(op.f('ix_master_love_tos_id'), table_name='master_love_tos')
    op.drop_table('master_love_tos')
    op.drop_index(op.f('ix_master_licenses_id'), table_name='master_licenses')
    op.drop_table('master_licenses')
    op.drop_index(op.f('ix_master_gears_id'), table_name='master_gears')
    op.drop_table('master_gears')
    op.drop_index(op.f('ix_master_dive_types_id'), table_name='master_dive_types')
    op.drop_table('master_dive_types')
    op.drop_index(op.f('ix_master_dive_sites_id'), table_name='master_dive_sites')
    op.drop_table('master_dive_sites')
    op.drop_index(op.f('ix_master_dive_preferences_id'), table_name='master_dive_preferences')
    op.drop_table('master_dive_preferences')
    op.drop_index(op.f('ix_master_colors_id'), table_name='master_colors')
    op.drop_table('master_colors')
    op.drop_index(op.f('ix_master_brands_id'), table_name='master_brands')
    op.drop_table('master_brands')
    op.drop_index(op.f('ix_diver_profiles_id'), table_name='diver_profiles')
    op.drop_table('diver_profiles')
    # ### end Alembic commands ###