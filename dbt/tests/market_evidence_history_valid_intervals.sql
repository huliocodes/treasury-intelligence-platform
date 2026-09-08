select
    evidence_id,
    valid_from,
    valid_to

from {{ ref('market_evidence_history') }}

where valid_to is not null
  and valid_to <= valid_from
