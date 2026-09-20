"""add ebooks and audio resources tables

Revision ID: e73a21bc9842
Revises: ca5e93ee39f1
Create Date: 2026-09-20
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e73a21bc9842"
down_revision = "ca5e93ee39f1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    # 1. ebooks table
    if "ebooks" not in existing_tables:
        op.create_table(
            "ebooks",
            sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
            sa.Column("title", sa.String(255), nullable=False),
            sa.Column("author", sa.String(100), nullable=True),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("category", sa.String(100), nullable=True),
            sa.Column("badge_label", sa.String(100), nullable=True),
            sa.Column("format_label", sa.String(100), nullable=True),
            sa.Column("page_count", sa.Integer(), nullable=True),
            sa.Column("cover_image_url", sa.String(512), nullable=True),
            sa.Column("download_url", sa.String(512), nullable=False),
            sa.Column("file_size_bytes", sa.BigInteger(), nullable=True),
            sa.Column("download_count", sa.Integer(), default=0, nullable=False),
            sa.Column("is_featured", sa.Boolean(), default=False, nullable=False),
            sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        )
        op.create_index("ix_ebooks_id", "ebooks", ["id"])
        op.create_index("ix_ebooks_category", "ebooks", ["category"])
        op.create_index("ix_ebooks_is_featured", "ebooks", ["is_featured"])

    # 2. audio_resources table
    if "audio_resources" not in existing_tables:
        op.create_table(
            "audio_resources",
            sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
            sa.Column("title", sa.String(255), nullable=False),
            sa.Column("author", sa.String(100), nullable=True),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("category", sa.String(100), nullable=True),
            sa.Column("badge_label", sa.String(100), nullable=True),
            sa.Column("parts_count", sa.Integer(), nullable=True),
            sa.Column("duration_seconds", sa.Integer(), nullable=True),
            sa.Column("duration_text", sa.String(64), nullable=True),
            sa.Column("cover_image_url", sa.String(512), nullable=True),
            sa.Column("audio_url", sa.String(512), nullable=False),
            sa.Column("file_size_bytes", sa.BigInteger(), nullable=True),
            sa.Column("listen_count", sa.Integer(), default=0, nullable=False),
            sa.Column("is_featured", sa.Boolean(), default=False, nullable=False),
            sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        )
        op.create_index("ix_audio_resources_id", "audio_resources", ["id"])
        op.create_index("ix_audio_resources_category", "audio_resources", ["category"])
        op.create_index("ix_audio_resources_is_featured", "audio_resources", ["is_featured"])


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if "audio_resources" in existing_tables:
        op.drop_table("audio_resources")
    if "ebooks" in existing_tables:
        op.drop_table("ebooks")
