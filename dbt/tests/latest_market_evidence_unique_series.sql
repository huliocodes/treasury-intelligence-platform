select
    instrument_id,
    market_id,
    access_route_id,
    evidence_type,
    measure,
    count(*) as row_count

from {{ ref('latest_market_evidence') }}

group by
    instrument_id,
    market_id,
    access_route_id,
    evidence_type,
    measure

having count(*) > 1
