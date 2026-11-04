-- SQLite starter schema for complaint tickets.
-- Run this when we reach the persistence phase.

CREATE TABLE IF NOT EXISTS complaints (
    ticket_id TEXT PRIMARY KEY,
    complaint_text TEXT NOT NULL,
    category TEXT NOT NULL,
    priority TEXT NOT NULL CHECK (priority IN ('low', 'medium', 'high')),
    status TEXT NOT NULL DEFAULT 'open'
        CHECK (status IN ('open', 'in_progress', 'resolved', 'closed')),
    suggested_resolution TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
