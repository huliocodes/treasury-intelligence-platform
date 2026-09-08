with evidence as (

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

    from {{ ref('stg_market_evidence') }}

),

with_validity as (

    select
        *,

        lead(observed_at) over (
            partition by
                instrument_id,
                coalesce(market_id, ''),
                coalesce(access_route_id, ''),
                evidence_type,
                measure
            order by
                observed_at,
                ingested_at,
                evidence_id
        ) as valid_to

    from evidence

)

select
    evidence_id,

    instrument_id,
    market_id,
    access_route_id,

    evidence_type,
    measure,

    observed_at as valid_from,
    valid_to,

    observed_date,

    numeric_value,
    unit,

    source_reference,
    source_name,
    source_url,

    ingestion_run_id,
    raw_payload,
    ingested_at,

    valid_to is null as is_current

from with_validity
