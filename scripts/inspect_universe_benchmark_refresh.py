from __future__ import annotations

from treasury_intelligence.analytics import (
    universe_candidates as universe,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.sources.ecb import (
    EstrObservation,
)


TEST_ESTR = EstrObservation(
    reference_date="2099-12-31",
    rate_pct=7.777,
)


def main() -> None:
    captured = {
        "xeon": [],
        "amundi": [],
        "icash": [],
    }

    original_xeon_snapshot = (
        universe.build_xeon_snapshot
    )

    original_amundi_snapshot = (
        universe
        .build_amundi_smart_overnight_snapshot
    )

    original_icash_snapshot = (
        universe.get_icash_snapshot
    )

    original_fetch_recent_estr = (
        universe.fetch_recent_estr
    )

    original_aave_builder_factory = (
        universe._build_aave_candidate_builder
    )

    def recording_xeon_snapshot(
        estr_rate_pct: float,
        estr_reference_date: str,
    ):
        captured["xeon"].append(
            (
                estr_rate_pct,
                estr_reference_date,
            )
        )

        return original_xeon_snapshot(
            estr_rate_pct=estr_rate_pct,
            estr_reference_date=(
                estr_reference_date
            ),
        )

    def recording_amundi_snapshot(
        estr_rate_pct: float,
        estr_reference_date: str,
    ):
        captured["amundi"].append(
            (
                estr_rate_pct,
                estr_reference_date,
            )
        )

        return original_amundi_snapshot(
            estr_rate_pct=estr_rate_pct,
            estr_reference_date=(
                estr_reference_date
            ),
        )

    def recording_icash_snapshot(
        estr_rate_pct: float,
        estr_reference_date: str,
    ):
        captured["icash"].append(
            (
                estr_rate_pct,
                estr_reference_date,
            )
        )

        return original_icash_snapshot(
            estr_rate_pct=estr_rate_pct,
            estr_reference_date=(
                estr_reference_date
            ),
        )

    universe.build_xeon_snapshot = (
        recording_xeon_snapshot
    )

    universe.build_amundi_smart_overnight_snapshot = (
        recording_amundi_snapshot
    )

    universe.get_icash_snapshot = (
        recording_icash_snapshot
    )

    try:
        print(
            "CASE 1 — EXPLICIT SHARED BENCHMARK"
        )
        print()

        xeon = (
            universe.build_xeon_universe_candidate(
                position_size_eur=100_000.0,
                mandate=MODEL_COMPANY_MANDATE,
                estr_observation=TEST_ESTR,
            )
        )

        amundi = (
            universe.build_amundi_universe_candidate(
                position_size_eur=100_000.0,
                mandate=MODEL_COMPANY_MANDATE,
                estr_observation=TEST_ESTR,
            )
        )

        icash = (
            universe.build_icash_universe_candidate(
                position_size_eur=100_000.0,
                mandate=MODEL_COMPANY_MANDATE,
                estr_observation=TEST_ESTR,
            )
        )

        expected = (
            TEST_ESTR.rate_pct,
            TEST_ESTR.reference_date,
        )

        assert captured["xeon"] == [
            expected
        ]

        assert captured["amundi"] == [
            expected
        ]

        assert captured["icash"] == [
            expected
        ]

        print(
            f"Reference date:               "
            f"{TEST_ESTR.reference_date}"
        )

        print(
            f"Rate:                         "
            f"{TEST_ESTR.rate_pct:.3f}%"
        )

        print(
            f"XEON benchmark inputs:        "
            f"{captured['xeon'][0]}"
        )

        print(
            f"Amundi benchmark inputs:      "
            f"{captured['amundi'][0]}"
        )

        print(
            f"ICASH benchmark inputs:       "
            f"{captured['icash'][0]}"
        )

        print(
            f"XEON candidate status:        "
            f"{xeon.candidate_status}"
        )

        print(
            f"Amundi candidate status:      "
            f"{amundi.candidate_status}"
        )

        print(
            f"ICASH candidate status:       "
            f"{icash.candidate_status}"
        )

        print()
        print("-" * 100)
        print()

        print(
            "CASE 2 — UNIVERSE FETCHES €STR ONCE"
        )
        print()

        fetch_count = 0

        def fake_fetch_recent_estr(
            limit: int = 5,
        ):
            nonlocal fetch_count

            fetch_count += 1

            assert limit == 1

            return [
                TEST_ESTR
            ]

        def fake_aave_builder_factory():
            def unused_aave_builder(
                position_size_eur: float,
                mandate,
            ):
                raise AssertionError(
                    "Aave builder should not be invoked "
                    "during benchmark-context construction."
                )

            return unused_aave_builder

        universe.fetch_recent_estr = (
            fake_fetch_recent_estr
        )

        universe._build_aave_candidate_builder = (
            fake_aave_builder_factory
        )

        opportunities = (
            universe
            .build_model_company_opportunity_universe()
        )

        assert fetch_count == 1

        opportunities_by_key = {
            opportunity.key: opportunity
            for opportunity in opportunities
        }

        assert "xeon" in opportunities_by_key
        assert "amundi" in opportunities_by_key
        assert "icash" in opportunities_by_key

        print(
            f"€STR fetch count:             "
            f"{fetch_count}"
        )

        print(
            f"Universe opportunity count:   "
            f"{len(opportunities)}"
        )

        print(
            "Shared benchmark binding:     "
            "XEON / Amundi / ICASH"
        )

        print()
        print("-" * 100)
        print()

        print(
            "CASE 3 — BOUND BUILDERS REUSE "
            "UNIVERSE BENCHMARK"
        )
        print()

        captured["xeon"].clear()
        captured["amundi"].clear()
        captured["icash"].clear()

        opportunities_by_key[
            "xeon"
        ].candidate_builder(
            100_000.0,
            MODEL_COMPANY_MANDATE,
        )

        opportunities_by_key[
            "amundi"
        ].candidate_builder(
            100_000.0,
            MODEL_COMPANY_MANDATE,
        )

        opportunities_by_key[
            "icash"
        ].candidate_builder(
            100_000.0,
            MODEL_COMPANY_MANDATE,
        )

        assert fetch_count == 1

        assert captured["xeon"] == [
            expected
        ]

        assert captured["amundi"] == [
            expected
        ]

        assert captured["icash"] == [
            expected
        ]

        print(
            f"€STR fetch count after builds: "
            f"{fetch_count}"
        )

        print(
            "XEON reused shared benchmark:  yes"
        )

        print(
            "Amundi reused shared benchmark: yes"
        )

        print(
            "ICASH reused shared benchmark: yes"
        )

        print()
        print(
            "All Milestone 15A benchmark "
            "freshness assertions passed."
        )

    finally:
        universe.build_xeon_snapshot = (
            original_xeon_snapshot
        )

        universe.build_amundi_smart_overnight_snapshot = (
            original_amundi_snapshot
        )

        universe.get_icash_snapshot = (
            original_icash_snapshot
        )

        universe.fetch_recent_estr = (
            original_fetch_recent_estr
        )

        universe._build_aave_candidate_builder = (
            original_aave_builder_factory
        )


if __name__ == "__main__":
    main()
