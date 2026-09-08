CREATE TABLE IF NOT EXISTS market_evidence (
    evidence_id TEXT PRIMARY KEY,

    instrument_id TEXT NOT NULL,
    market_id TEXT,
    access_route_id TEXT,

    evidence_type TEXT NOT NULL
        CHECK (
            evidence_type IN (
                'market_return',
                'market_liquidity',
                'benchmark',
                'risk',
                'accessibility',
                'cost'
            )
        ),

    observed_at TIMESTAMPTZ NOT NULL,

    measure TEXT NOT NULL,
    numeric_value NUMERIC(24, 12),
    unit TEXT,

    source_reference TEXT NOT NULL,
    source_name TEXT,
    source_url TEXT,

    ingestion_run_id TEXT NOT NULL,

    raw_payload JSONB NOT NULL DEFAULT '{}'::jsonb,

    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS
    idx_market_evidence_instrument_type_observed
ON market_evidence (
    instrument_id,
    evidence_type,
    observed_at DESC
);

CREATE INDEX IF NOT EXISTS
    idx_market_evidence_market_observed
ON market_evidence (
    market_id,
    observed_at DESC
)
WHERE market_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS
    idx_market_evidence_ingestion_run
ON market_evidence (
    ingestion_run_id
);

COMMENT ON TABLE market_evidence IS
    'Append-only source evidence used by the treasury intelligence pipeline.';

COMMENT ON COLUMN market_evidence.evidence_id IS
    'Stable evidence identifier used to make ingestion retries idempotent.';

COMMENT ON COLUMN market_evidence.observed_at IS
    'Timestamp at which the underlying market or source fact was observed.';

COMMENT ON COLUMN market_evidence.ingested_at IS
    'Timestamp at which the pipeline persisted the evidence record.';

COMMENT ON COLUMN market_evidence.raw_payload IS
    'Raw normalized source payload retained for provenance and debugging.';
