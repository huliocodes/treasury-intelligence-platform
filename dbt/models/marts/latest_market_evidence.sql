with ranked as (

    select
        evidence_id,

        instrument_id,
        market_id,
        access_route_id,

        evidence_type,
        measure,

        observed_at,
        observed_date,

        numeric_value,
        unit,

        source_reference,
        source_name,
        source_url,

        ingestion_run_id,
        raw_payload,
        ingested_at,

        row_number() over (
            partition by
                instrument_id,
                coalesce(market_id, ''),
                coalesce(access_route_id, ''),
                evidence_type,
                measure
            order by
                observed_at desc,
                ingested_at desc,
                evidence_id desc
        ) as evidence_rank

    from {{ ref('stg_market_evidence') }}

)

select
    evidence_id,

    instrument_id,
    market_id,
    access_route_id,

    evidence_type,
    measure,

    observed_at,
    observed_date,

    numeric_value,
    unit,

    source_reference,
    source_name,
    source_url,

    ingestion_run_id,
    raw_payload,
    ingested_at

from ranked

where evidence_rank = 1
