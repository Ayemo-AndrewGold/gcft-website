# Agent State & Context

## Current Objective
- [x] YouTube Data API v3 Integration:
  - [x] Quota-efficient uploads playlist sync (1 quota unit) via `playlistItems.list`.
  - [x] Live stream detection via `search.list?eventType=live` with in-memory caching and DB persistence/fallback.
  - [x] Unified `/live` endpoint returning both Mixlr (audio) and YouTube (video) with `active_platform`.
  - [x] Computed `watch_url` and `embed_url` properties on `VideoRead` schema.
  - [x] Background jobs in APScheduler (periodic recording sync + windowed service hours live check).
  - [x] Admin manual override support on `PUT /live/status`.
- [x] Archives & Media Library (Option 2):
  - [x] `EBook` model and CRUD/upload endpoints (`/ebooks`) with Cloudinary raw file storage and download counters.
  - [x] `AudioResource` model and CRUD/upload endpoints (`/audio-resources`) with Cloudinary audio storage and listen counters.
  - [x] Unified `GET /library/featured` aggregator delivering Audio Books, E-Books, and YouTube Videos in a single sub-50ms request.
  - [x] Graceful fallback to recent Mixlr podcast broadcasts if no curated audiobooks are seeded.
  - [x] Alembic migration `e73a21bc9842` for `ebooks` and `audio_resources`.
  - [x] Full automated test suite (29/29 tests passing across all suites).

## Compressed Context (Do Not Re-Read These Files)
- `app/models/ebook.py`: EBook model with title, author, badges, page_count, format_label, cover/download URLs, download_count, is_featured.
- `app/models/audio_resource.py`: AudioResource model with narrator/author, badge_label, parts_count, duration, audio_url, listen_count, is_featured.
- `app/services/ebook_service.py`: BaseService implementation for EBook with Cloudinary `raw` uploads for PDF/EPUB.
- `app/services/audio_resource_service.py`: BaseService implementation for AudioResource with Cloudinary `video` uploads for MP3.
- `app/services/library_service.py`: Aggregator service querying top featured items across EBook, AudioResource, and Video.
- `app/routers/ebooks.py`: Routes for `/ebooks` including `/upload` and `/{id}/download`.
- `app/routers/audio_resources.py`: Routes for `/audio-resources` including `/upload` and `/{id}/listen`.
- `app/routers/library.py`: Route for `/library/featured`.
- `tests/test_library.py`: 6 tests for EBooks, AudioResources, and the unified featured feed.

## Database & Cloudinary Status
- Supabase PostgreSQL: Alembic migration `e73a21bc9842` ready.
- Cloudinary: Credentials in `.env` configured for `gcft_gallery`, `gcft_ebooks`, and `gcft_audio`.
