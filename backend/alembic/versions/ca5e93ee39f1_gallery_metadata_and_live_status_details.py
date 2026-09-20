"""gallery metadata and live status details

Adds gallery metadata columns (thumbnail/optimized variants, category, tags,
dimensions, file info, featured flag, updated_at) and live status detail
columns (event/broadcast titles, audio stream URL, artwork URL).

Idempotent: each ADD COLUMN / CREATE INDEX is guarded by an inspector check,
so the revision is a safe no-op on databases already created from the current
models (e.g. fresh ``create_all``), and backfills databases created from the
older schema.

Note: the inspector guards require a live connection, so offline
``--sql`` rendering is not supported for this revision; run upgrades online.

Revision ID: ca5e93ee39f1
Revises:
Create Date: 2026-09-20
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ca5e93ee39f1"
down_revision = None
branch_labels = None
depends_on = None


def _existing_columns(table_name: str) -> set:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if table_name not in inspector.get_table_names():
        return set()
    return {col["name"] for col in inspector.get_columns(table_name)}


def _indexed_columns(table_name: str) -> list:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if table_name not in inspector.get_table_names():
        return []
    return [sorted(idx["column_names"] or []) for idx in inspector.get_indexes(table_name)]


def _add_column_if_missing(table_name: str, column: sa.Column) -> None:
    if column.name not in _existing_columns(table_name):
        op.add_column(table_name, column)


def _add_required_column_if_missing(
    table_name: str,
    column_name: str,
    column_type: sa.types.TypeEngine,
    server_default: object,
    backfill_literal: str,
) -> None:
    """ADD a NOT NULL column with a server default.

    SQLite rejects ADD COLUMN with non-constant defaults (e.g.
    CURRENT_TIMESTAMP), so there the column is added nullable and existing
    rows are backfilled with an UPDATE instead. Postgres keeps the strict
    NOT NULL + server default definition matching the models.
    """
    if column_name in _existing_columns(table_name):
        return
    if op.get_bind().dialect.name == "sqlite":
        op.add_column(table_name, sa.Column(column_name, column_type, nullable=True))
        op.execute(
            sa.text(f"UPDATE {table_name} SET {column_name} = {backfill_literal} "
                    f"WHERE {column_name} IS NULL")
        )
    else:
        op.add_column(
            table_name,
            sa.Column(column_name, column_type, server_default=server_default, nullable=False),
        )


def _create_index_if_missing(index_name: str, table_name: str, columns: list) -> None:
    if sorted(columns) not in _indexed_columns(table_name):
        op.create_index(index_name, table_name, columns)


def upgrade() -> None:
    # -- live_status: detail fields surfaced by LivePlatformStatus -------------
    _add_column_if_missing("live_status", sa.Column("event_title", sa.String(255), nullable=True))
    _add_column_if_missing(
        "live_status", sa.Column("broadcast_title", sa.String(255), nullable=True)
    )
    _add_column_if_missing(
        "live_status", sa.Column("audio_stream_url", sa.String(512), nullable=True)
    )
    _add_column_if_missing(
        "live_status", sa.Column("channel_artwork_url", sa.String(512), nullable=True)
    )

    # -- gallery_images: metadata for filters + responsive variants ------------
    _add_column_if_missing(
        "gallery_images", sa.Column("thumbnail_url", sa.String(512), nullable=True)
    )
    _add_column_if_missing(
        "gallery_images", sa.Column("optimized_url", sa.String(512), nullable=True)
    )
    _add_column_if_missing("gallery_images", sa.Column("category", sa.String(100), nullable=True))
    _add_column_if_missing("gallery_images", sa.Column("tags", sa.String(255), nullable=True))
    _add_column_if_missing("gallery_images", sa.Column("width", sa.Integer(), nullable=True))
    _add_column_if_missing("gallery_images", sa.Column("height", sa.Integer(), nullable=True))
    _add_column_if_missing(
        "gallery_images", sa.Column("file_size_bytes", sa.BigInteger(), nullable=True)
    )
    _add_column_if_missing("gallery_images", sa.Column("format", sa.String(32), nullable=True))
    _add_required_column_if_missing(
        "gallery_images", "is_featured", sa.Boolean(), sa.false(), "0"
    )
    _add_required_column_if_missing(
        "gallery_images",
        "updated_at",
        sa.DateTime(timezone=True),
        sa.func.now(),
        "CURRENT_TIMESTAMP",
    )
    _create_index_if_missing("ix_gallery_images_category", "gallery_images", ["category"])
    _create_index_if_missing("ix_gallery_images_is_featured", "gallery_images", ["is_featured"])


def downgrade() -> None:
    bind = op.get_bind()
    is_sqlite = bind.dialect.name == "sqlite"

    def _drop_index_if_exists(index_name: str, table_name: str, columns: list) -> None:
        if sorted(columns) in _indexed_columns(table_name):
            if is_sqlite:
                # SQLite has no DROP INDEX IF EXISTS via op; batch mode handles it.
                with op.batch_alter_table(table_name) as batch_op:
                    batch_op.drop_index(index_name)
            else:
                op.drop_index(index_name, table_name=table_name)

    def _drop_column_if_exists(table_name: str, column_name: str) -> None:
        if column_name in _existing_columns(table_name):
            if is_sqlite:
                with op.batch_alter_table(table_name) as batch_op:
                    batch_op.drop_column(column_name)
            else:
                op.drop_column(table_name, column_name)

    _drop_index_if_exists("ix_gallery_images_is_featured", "gallery_images", ["is_featured"])
    _drop_index_if_exists("ix_gallery_images_category", "gallery_images", ["category"])

    for column_name in (
        "updated_at",
        "is_featured",
        "format",
        "file_size_bytes",
        "height",
        "width",
        "tags",
        "category",
        "optimized_url",
        "thumbnail_url",
    ):
        _drop_column_if_exists("gallery_images", column_name)

    for column_name in (
        "channel_artwork_url",
        "audio_stream_url",
        "broadcast_title",
        "event_title",
    ):
        _drop_column_if_exists("live_status", column_name)
