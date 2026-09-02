from __future__ import annotations

from treasury_intelligence.analytics.allocation_selection import (
    AllocationOpportunity,
)

from treasury_intelligence.analytics.recommendation_candidates import (
    build_btf_2027_08_11_recommendation_candidate,
    build_btf_recommendation_candidate,
    build_bubill_2027_08_18_recommendation_candidate,
    build_bubill_recommendation_candidate,
    build_ernx_recommendation_candidate,
    build_franklin_euro_short_maturity_recommendation_candidate,
    build_ishares_govt_0_1yr_recommendation_candidate,
)


ALLOCATION_OPPORTUNITIES = (
    AllocationOpportunity(
        key="ernx",
        label="ERNX",
        candidate_builder=(
            build_ernx_recommendation_candidate
        ),
    ),
    AllocationOpportunity(
        key="franklin_euro_short_maturity",
        label="Franklin Euro Short Maturity",
        candidate_builder=(
            build_franklin_euro_short_maturity_recommendation_candidate
        ),
    ),
    AllocationOpportunity(
        key="ishares_govt_0_1yr",
        label="iShares € Govt Bond 0-1yr",
        candidate_builder=(
            build_ishares_govt_0_1yr_recommendation_candidate
        ),
    ),
    AllocationOpportunity(
        key="btf",
        label="French BTF Mar",
        candidate_builder=(
            build_btf_recommendation_candidate
        ),
    ),
    AllocationOpportunity(
        key="btf_aug_2027",
        label="French BTF Aug",
        candidate_builder=(
            build_btf_2027_08_11_recommendation_candidate
        ),
    ),
    AllocationOpportunity(
        key="bubill",
        label="German Bubill Jul",
        candidate_builder=(
            build_bubill_recommendation_candidate
        ),
    ),
    AllocationOpportunity(
        key="bubill_aug_2027",
        label="German Bubill Aug",
        candidate_builder=(
            build_bubill_2027_08_18_recommendation_candidate
        ),
    ),
)
