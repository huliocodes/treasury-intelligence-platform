with latest as (

    select
        instrument_id,
        market_id,
        access_route_id,
        evidence_type,
        measure,
        observed_at

    from {{ ref('latest_market_evidence') }}

),

max_observed as (

    select
        instrument_id,
        market_id,
        access_route_id,
        evidence_type,
        measure,
        max(observed_at) as max_observed_at

    from {{ ref('stg_market_evidence') }}

    group by
        instrument_id,
        market_id,
        access_route_id,
        evidence_type,
        measure

)

select
    latest.instrument_id,
    latest.market_id,
    latest.access_route_id,
    latest.evidence_type,
    latest.measure,
    latest.observed_at,
    max_observed.max_observed_at

from latest

inner join max_observed
    on latest.instrument_id = max_observed.instrument_id
   and latest.market_id is not distinct from max_observed.market_id
   and latest.access_route_id is not distinct from max_observed.access_route_id
   and latest.evidence_type = max_observed.evidence_type
   and latest.measure = max_observed.measure

where latest.observed_at <> max_observed.max_observed_at
