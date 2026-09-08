select
    evidence_id,

    instrument_id,
    market_id,
    access_route_id,

    evidence_type,

    observed_at,
    observed_at::date as observed_date,

    measure,

    numeric_value,
    unit,

    source_reference,
    source_name,
    source_url,

    ingestion_run_id,

    raw_payload,

    ingested_at

from {{ source('treasury_raw', 'market_evidence') }}
