select
    instrument_id,
    market_id,
    access_route_id,
    evidence_type,
    measure,
    count(*) filter (
        where is_current
    ) as current_rows

from {{ ref('market_evidence_history') }}

group by
    instrument_id,
    market_id,
    access_route_id,
    evidence_type,
    measure

having count(*) filter (
    where is_current
) <> 1
