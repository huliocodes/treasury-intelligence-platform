from __future__ import annotations

from treasury_intelligence.models.discovery_screening import (
    DiscoveryOpportunity,
)


def build_expanded_discovery_catalog() -> tuple[
    DiscoveryOpportunity,
    ...,
]:
    """
    Build the structured Milestone 13 discovery catalog.

    This catalog contains discovery-stage opportunities only.

    Inclusion here does not mean:
    - recommendation ready
    - downstream eligible
    - risk acceptable
    - economically attractive
    - executable

    The generic discovery screening layer determines whether each
    implementation should be promoted to deeper research, held for
    accessibility evidence, or screened out.

    Existing V1 production candidates remain in the existing production
    universe pipeline and are not replaced by this catalog.
    """
    return (
        _slovenia_tz233(),
        _slovenia_sz163(),
        _slovenia_dz125(),
        _icash(),
        _blackrock_ics_core_acc(),
        _blackrock_ics_select(),
        _blackrock_ics_premier(),
        _ernx(),
        _franklin_euro_short_maturity(),
        _eur_government_0_1y_etf(),
        _german_bubill_bu0e436(),
        _german_bubill_bu0e444(),
        _french_btf_mar_2027(),
        _french_btf_aug_2027(),
        _dutch_dtc(),
        _belgian_treasury_certificate(),
        _austrian_treasury_bill(),
        _finnish_treasury_bill(),
        _eu_bill_nov_2026(),
        _eu_bill_feb_2027(),
        _eu_bill_aug_2027(),
        _esm_bill_nov_2026(),
        _blackrock_ics_tokenized_eur(),
        _aave_v3_base_eurc(),
        _morpho_philidor_eurc_prime(),
        _morpho_moonwell_eurc(),
        _pendle_eur_term_yield(),
        _icslo(),
    )


def _slovenia_tz233() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="slovenia_tbill_tz233",
        strategy_id="slovenia_sovereign_bills",
        implementation_id="tz233",
        display_name="Slovenia TZ233",
        full_name="Republic of Slovenia 3-Month Treasury Bill TZ233",
        category="direct_sovereign_bill",
        short_description=(
            "Short-term EUR Treasury bill issued directly by the "
            "Republic of Slovenia."
        ),
        economic_description=(
            "The treasury owns a direct short-term debt claim against "
            "the Republic of Slovenia."
        ),
        return_source=(
            "Discount yield earned as the Treasury bill converges "
            "toward redemption at maturity."
        ),
        currency="EUR",
        issuer_manager_protocol="Republic of Slovenia",
        possible_access_route=(
            "Primary auction through an eligible primary dealer or "
            "subsequent secondary-market access through Ljubljana "
            "Stock Exchange."
        ),
        slovenian_doo_access_status="verified",
        access_evidence_sufficient=True,
        discovery_priority="high",
        mandate_relevance="high",
        minimum_investment_eur=1_000.0,
        maturity_date="2026-12-10",
        source_summary=(
            "Republic of Slovenia 2026 Treasury-bill issuance schedule."
        ),
        notes=(
            "Scheduled for auction on 2026-09-08 with settlement "
            "2026-09-10. Current yield is not yet available."
        ),
    )


def _slovenia_sz163() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="slovenia_tbill_sz163",
        strategy_id="slovenia_sovereign_bills",
        implementation_id="sz163",
        display_name="Slovenia SZ163",
        full_name="Republic of Slovenia 6-Month Treasury Bill SZ163",
        category="direct_sovereign_bill",
        short_description=(
            "Short-term EUR Treasury bill issued directly by the "
            "Republic of Slovenia."
        ),
        economic_description=(
            "The treasury owns a direct short-term debt claim against "
            "the Republic of Slovenia."
        ),
        return_source=(
            "Discount yield earned as the Treasury bill converges "
            "toward redemption at maturity."
        ),
        currency="EUR",
        issuer_manager_protocol="Republic of Slovenia",
        possible_access_route=(
            "Primary auction through an eligible primary dealer or "
            "subsequent secondary-market access through Ljubljana "
            "Stock Exchange."
        ),
        slovenian_doo_access_status="verified",
        access_evidence_sufficient=True,
        discovery_priority="high",
        mandate_relevance="high",
        minimum_investment_eur=1_000.0,
        maturity_date="2027-03-11",
        source_summary=(
            "Republic of Slovenia 2026 Treasury-bill issuance schedule."
        ),
        notes=(
            "Scheduled for auction on 2026-09-08 with settlement "
            "2026-09-10. Current yield is not yet available."
        ),
    )


def _slovenia_dz125() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="slovenia_tbill_dz125",
        strategy_id="slovenia_sovereign_bills",
        implementation_id="dz125",
        display_name="Slovenia DZ125",
        full_name="Republic of Slovenia 12-Month Treasury Bill DZ125",
        category="direct_sovereign_bill",
        short_description=(
            "Short-term EUR Treasury bill issued directly by the "
            "Republic of Slovenia."
        ),
        economic_description=(
            "The treasury owns a direct short-term debt claim against "
            "the Republic of Slovenia."
        ),
        return_source=(
            "Discount yield earned as the Treasury bill converges "
            "toward redemption at maturity."
        ),
        currency="EUR",
        issuer_manager_protocol="Republic of Slovenia",
        possible_access_route=(
            "Primary auction through an eligible primary dealer or "
            "subsequent secondary-market access through Ljubljana "
            "Stock Exchange."
        ),
        slovenian_doo_access_status="verified",
        access_evidence_sufficient=True,
        discovery_priority="high",
        mandate_relevance="high",
        minimum_investment_eur=1_000.0,
        maturity_date="2027-09-09",
        source_summary=(
            "Republic of Slovenia 2026 Treasury-bill issuance schedule."
        ),
        notes=(
            "Scheduled for auction on 2026-09-08 with settlement "
            "2026-09-10. Current yield is not yet available."
        ),
    )


def _icash() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="icash_ljse",
        strategy_id="eur_money_market_fund",
        implementation_id="HRICAMFEUMM1",
        display_name="ICASH",
        full_name="InterCapital Euro Money Market UCITS ETF",
        category="money_market_etf",
        short_description=(
            "EUR money-market UCITS ETF listed on the Ljubljana "
            "Stock Exchange."
        ),
        economic_description=(
            "The treasury owns ETF units backed by a EUR money-market "
            "investment portfolio."
        ),
        return_source=(
            "Interest generated by the underlying short-term EUR "
            "money-market portfolio after product expenses."
        ),
        currency="EUR",
        issuer_manager_protocol="InterCapital",
        possible_access_route=(
            "IBKR corporate account via Ljubljana Stock Exchange."
        ),
        slovenian_doo_access_status="verified",
        access_evidence_sufficient=True,
        discovery_priority="high",
        mandate_relevance="high",
        source_summary=(
            "Ljubljana Stock Exchange listing and IBKR Ljubljana "
            "Stock Exchange market-access evidence."
        ),
        notes=(
            "Discovery access verified in Milestone 13C.3. Exact current "
            "yield, fund scale, liquidity, fees and €5 million execution "
            "capacity still require full analysis."
        ),
    )


def _blackrock_ics_core_acc() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="blackrock_ics_euro_core_acc",
        strategy_id="blackrock_ics_euro_liquidity",
        implementation_id="IE0005023910",
        display_name="BlackRock ICS Euro Liquidity Core Acc",
        full_name="BlackRock ICS Euro Liquidity Fund Core Acc",
        category="institutional_money_market_fund",
        short_description=(
            "Institutional EUR liquidity fund designed for corporate "
            "cash management."
        ),
        economic_description=(
            "The treasury owns fund shares backed by diversified "
            "short-term EUR money-market instruments and deposits."
        ),
        return_source=(
            "Interest earned by the underlying short-term portfolio "
            "after fund expenses."
        ),
        currency="EUR",
        issuer_manager_protocol="BlackRock",
        possible_access_route=(
            "Institutional fund subscription through an eligible "
            "distribution or custody route."
        ),
        slovenian_doo_access_status="plausible",
        access_evidence_sufficient=False,
        discovery_priority="high",
        mandate_relevance="high",
        minimum_investment_eur=1_000_000.0,
        maximum_plausible_allocation_eur=5_000_000.0,
        preliminary_yield_pct=2.21,
        yield_as_of="2026-08-31",
        liquidity_summary="Daily dealing with approximately T+1 settlement.",
        source_summary="BlackRock institutional liquidity fund materials.",
        notes=(
            "Exact Slovenian corporate subscription, distributor or "
            "custody route remains unresolved."
        ),
    )


def _blackrock_ics_select() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="blackrock_ics_euro_select",
        strategy_id="blackrock_ics_euro_liquidity",
        implementation_id="select_share_class",
        display_name="BlackRock ICS Euro Liquidity Select",
        full_name="BlackRock ICS Euro Liquidity Fund Select Share Class",
        category="institutional_money_market_fund",
        short_description=(
            "Higher-minimum institutional share class of the "
            "BlackRock EUR liquidity strategy."
        ),
        economic_description=(
            "The treasury would own a share class of the same underlying "
            "institutional EUR money-market fund."
        ),
        return_source=(
            "Interest generated by the underlying money-market portfolio "
            "after share-class expenses."
        ),
        currency="EUR",
        issuer_manager_protocol="BlackRock",
        possible_access_route="Institutional fund subscription.",
        slovenian_doo_access_status="plausible",
        access_evidence_sufficient=False,
        discovery_priority="low",
        mandate_relevance="high",
        minimum_investment_eur=100_000_000.0,
        preliminary_yield_pct=2.26,
        yield_as_of="2026-08-31",
        liquidity_summary="Daily dealing.",
        source_summary="BlackRock institutional liquidity fund materials.",
    )


def _blackrock_ics_premier() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="blackrock_ics_euro_premier",
        strategy_id="blackrock_ics_euro_liquidity",
        implementation_id="premier_share_class",
        display_name="BlackRock ICS Euro Liquidity Premier",
        full_name="BlackRock ICS Euro Liquidity Fund Premier Share Class",
        category="institutional_money_market_fund",
        short_description=(
            "Very-high-minimum institutional share class of the "
            "BlackRock EUR liquidity strategy."
        ),
        economic_description=(
            "The treasury would own a share class of the same underlying "
            "institutional EUR money-market fund."
        ),
        return_source=(
            "Interest generated by the underlying money-market portfolio "
            "after share-class expenses."
        ),
        currency="EUR",
        issuer_manager_protocol="BlackRock",
        possible_access_route="Institutional fund subscription.",
        slovenian_doo_access_status="plausible",
        access_evidence_sufficient=False,
        discovery_priority="low",
        mandate_relevance="high",
        minimum_investment_eur=500_000_000.0,
        preliminary_yield_pct=2.31,
        yield_as_of="2026-08-31",
        liquidity_summary="Daily dealing.",
        source_summary="BlackRock institutional liquidity fund materials.",
    )


def _ernx() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="ernx",
        strategy_id="eur_ultrashort_investment_grade_bonds",
        implementation_id="ernx_xetra",
        display_name="ERNX",
        full_name="iShares € Ultrashort Bond UCITS ETF",
        category="short_duration_bond_etf",
        short_description=(
            "Diversified ETF holding very short-duration "
            "investment-grade EUR bonds."
        ),
        economic_description=(
            "The treasury owns ETF shares backed by a diversified "
            "portfolio of short-duration fixed-income securities."
        ),
        return_source=(
            "Underlying bond income and price convergence less fund "
            "and execution costs."
        ),
        currency="EUR",
        issuer_manager_protocol="BlackRock / iShares",
        possible_access_route="IBKR corporate account via Xetra.",
        slovenian_doo_access_status="verified",
        access_evidence_sufficient=True,
        discovery_priority="high",
        mandate_relevance="high",
        maximum_plausible_allocation_eur=5_000_000.0,
        preliminary_yield_pct=2.91,
        yield_as_of="2026-08-28",
        liquidity_summary=(
            "Large UCITS ETF with position-aware liquidity already "
            "researched in V1."
        ),
        source_summary="Existing V1 ERNX evidence package.",
    )


def _franklin_euro_short_maturity() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="franklin_euro_short_maturity",
        strategy_id="eur_short_maturity_investment_grade_bonds",
        implementation_id="IE000STIHQB2",
        display_name="Franklin Euro Short Maturity",
        full_name="Franklin Euro Short Maturity UCITS ETF",
        category="short_duration_bond_etf",
        short_description=(
            "Actively managed ETF investing in short-maturity EUR "
            "fixed-income securities."
        ),
        economic_description=(
            "The treasury owns ETF shares backed by an actively managed "
            "portfolio of short-duration EUR bonds."
        ),
        return_source=(
            "Underlying bond interest and price movement less fund "
            "and execution costs."
        ),
        currency="EUR",
        issuer_manager_protocol="Franklin Templeton",
        possible_access_route=(
            "IBKR corporate account via Xetra, ticker FVSA."
        ),
        slovenian_doo_access_status="verified",
        access_evidence_sufficient=True,
        discovery_priority="high",
        mandate_relevance="high",
        preliminary_yield_pct=2.70,
        yield_as_of="2026-08-20",
        liquidity_summary=(
            "UCITS ETF with approximately €596 million fund scale "
            "at discovery."
        ),
        source_summary=(
            "Franklin Templeton exact share-class and Xetra listing "
            "evidence plus IBKR Xetra market access."
        ),
        notes=(
            "Discovery access verified in Milestone 13C.3. Position-aware "
            "liquidity, execution cost and realistic net return remain "
            "to be analyzed."
        ),
    )


def _eur_government_0_1y_etf() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="ishares_eur_government_0_1y",
        strategy_id="eur_short_sovereign_bond_basket",
        implementation_id="IE00B3FH7618",
        display_name="iShares € Govt Bond 0-1yr",
        full_name="iShares € Govt Bond 0-1yr UCITS ETF",
        category="short_duration_government_bond_etf",
        short_description=(
            "ETF holding a diversified portfolio of very short-maturity "
            "euro-area government bonds."
        ),
        economic_description=(
            "The treasury owns ETF shares backed primarily by "
            "short-duration EUR sovereign debt."
        ),
        return_source=(
            "Government bond income and price convergence less fund "
            "and execution costs."
        ),
        currency="EUR",
        issuer_manager_protocol="BlackRock / iShares",
        possible_access_route=(
            "IBKR corporate account via Xetra, symbol EUN6."
        ),
        slovenian_doo_access_status="verified",
        access_evidence_sufficient=True,
        discovery_priority="high",
        mandate_relevance="high",
        preliminary_yield_pct=2.62,
        yield_as_of="2026-08-27",
        liquidity_summary=(
            "UCITS sovereign-bond ETF with approximately €1.195 billion "
            "fund assets as of 2026-08-31."
        ),
        source_summary=(
            "BlackRock fund evidence, Deutsche Börse exact ISIN listing "
            "and IBKR Xetra market access."
        ),
        notes=(
            "Discovery access verified in Milestone 13C.3. Full "
            "position-aware liquidity, holdings risk and realistic "
            "return analysis remain outstanding."
        ),
    )


def _german_bubill_bu0e436() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="german_bubill_bu0e436",
        strategy_id="german_sovereign_bills",
        implementation_id="DE000BU0E436",
        display_name="German Bubill Jul 2027",
        full_name="Federal Republic of Germany Bubill DE000BU0E436",
        category="direct_sovereign_bill",
        short_description=(
            "Short-term EUR zero-coupon bill issued directly by Germany."
        ),
        economic_description=(
            "The treasury owns a direct debt claim against the "
            "Federal Republic of Germany."
        ),
        return_source=(
            "Discount yield earned as the bill converges toward "
            "redemption at maturity."
        ),
        currency="EUR",
        issuer_manager_protocol="Federal Republic of Germany",
        possible_access_route="IBKR Europe OTC bond market.",
        slovenian_doo_access_status="verified",
        access_evidence_sufficient=True,
        discovery_priority="high",
        mandate_relevance="high",
        maximum_plausible_allocation_eur=5_000_000.0,
        preliminary_yield_pct=2.647,
        yield_as_of="2026-08-24",
        maturity_date="2027-07-14",
        liquidity_summary=(
            "€5.5 billion outstanding at the V1 evidence date."
        ),
        source_summary="German Finance Agency and existing V1 evidence.",
    )


def _german_bubill_bu0e444() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="german_bubill_bu0e444",
        strategy_id="german_sovereign_bills",
        implementation_id="DE000BU0E444",
        display_name="German Bubill Aug 2027",
        full_name="Federal Republic of Germany Bubill DE000BU0E444",
        category="direct_sovereign_bill",
        short_description=(
            "Short-term EUR zero-coupon bill issued directly by Germany."
        ),
        economic_description=(
            "The treasury owns a direct debt claim against the "
            "Federal Republic of Germany."
        ),
        return_source=(
            "Discount yield earned as the bill converges toward "
            "redemption at maturity."
        ),
        currency="EUR",
        issuer_manager_protocol="Federal Republic of Germany",
        possible_access_route="IBKR Europe OTC bond market.",
        slovenian_doo_access_status="verified",
        access_evidence_sufficient=True,
        discovery_priority="high",
        mandate_relevance="high",
        preliminary_yield_pct=2.656,
        yield_as_of="2026-08-17",
        liquidity_summary=(
            "Approximately €3 billion issued at discovery; full "
            "secondary-market evidence remains to be assembled."
        ),
        source_summary="German Finance Agency auction evidence.",
    )


def _french_btf_mar_2027() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="french_btf_mar_2027",
        strategy_id="french_sovereign_bills",
        implementation_id="FR0129704153",
        display_name="French BTF Mar 2027",
        full_name="French Republic BTF FR0129704153",
        category="direct_sovereign_bill",
        short_description=(
            "Short-term EUR zero-coupon Treasury bill issued by France."
        ),
        economic_description=(
            "The treasury owns a direct debt claim against the "
            "French Republic."
        ),
        return_source=(
            "Discount yield earned as the bill converges toward "
            "redemption at maturity."
        ),
        currency="EUR",
        issuer_manager_protocol="French Republic",
        possible_access_route="IBKR Europe OTC bond market.",
        slovenian_doo_access_status="verified",
        access_evidence_sufficient=True,
        discovery_priority="high",
        mandate_relevance="high",
        maximum_plausible_allocation_eur=5_000_000.0,
        preliminary_yield_pct=2.697,
        yield_as_of="2026-08-31",
        maturity_date="2027-03-10",
        liquidity_summary=(
            "Multi-billion-euro sovereign bill with existing V1 "
            "position-aware liquidity evidence."
        ),
        source_summary="Agence France Trésor and existing V1 evidence.",
    )


def _french_btf_aug_2027() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="french_btf_aug_2027",
        strategy_id="french_sovereign_bills",
        implementation_id="FR0129704187",
        display_name="French BTF Aug 2027",
        full_name="French Republic BTF FR0129704187",
        category="direct_sovereign_bill",
        short_description=(
            "Short-term EUR zero-coupon Treasury bill issued by France."
        ),
        economic_description=(
            "The treasury owns a direct debt claim against the "
            "French Republic."
        ),
        return_source=(
            "Discount yield earned as the bill converges toward "
            "redemption at maturity."
        ),
        currency="EUR",
        issuer_manager_protocol="French Republic",
        possible_access_route="IBKR Europe OTC bond market.",
        slovenian_doo_access_status="verified",
        access_evidence_sufficient=True,
        discovery_priority="high",
        mandate_relevance="high",
        preliminary_yield_pct=2.860,
        yield_as_of="2026-08-31",
        maturity_date="2027-08-11",
        liquidity_summary=(
            "Approximately €6.237 billion was outstanding before the "
            "2026-08-31 reopening, which issued another €1.898 billion."
        ),
        source_summary=(
            "Agence France Trésor exact security and auction evidence "
            "plus existing V1 French-BTF corporate access route."
        ),
        notes=(
            "Discovery access verified in Milestone 13C.3. Full "
            "secondary-market execution, position-size liquidity and "
            "realistic net return still require analysis."
        ),
    )


def _dutch_dtc() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="netherlands_dtc_short_bill",
        strategy_id="netherlands_sovereign_bills",
        implementation_id="current_dtc_research_candidate",
        display_name="Netherlands DTC",
        full_name="Dutch Treasury Certificate Current Short-Dated Candidate",
        category="direct_sovereign_bill",
        short_description=(
            "Short-term EUR Treasury certificate issued by the Netherlands."
        ),
        economic_description=(
            "The treasury would own a direct debt claim against the "
            "State of the Netherlands."
        ),
        return_source=(
            "Discount yield earned through holding the certificate "
            "toward redemption."
        ),
        currency="EUR",
        issuer_manager_protocol="State of the Netherlands",
        possible_access_route=(
            "Institutional or corporate secondary-market bond route."
        ),
        slovenian_doo_access_status="unknown",
        access_evidence_sufficient=False,
        discovery_priority="high",
        mandate_relevance="high",
        source_summary="Dutch State Treasury Agency issuance calendar.",
        notes=(
            "Exact current security, current yield and Slovenian corporate "
            "secondary-market execution route remain unresolved."
        ),
    )


def _belgian_treasury_certificate() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="belgium_treasury_certificate",
        strategy_id="belgian_sovereign_bills",
        implementation_id="current_belgian_tc_research_candidate",
        display_name="Belgian Treasury Certificate",
        full_name="Kingdom of Belgium Short-Dated Treasury Certificate",
        category="direct_sovereign_bill",
        short_description=(
            "Short-term EUR Treasury certificate issued by Belgium."
        ),
        economic_description=(
            "The treasury would own a direct debt claim against the "
            "Kingdom of Belgium."
        ),
        return_source=(
            "Discount yield earned through holding the certificate "
            "toward redemption."
        ),
        currency="EUR",
        issuer_manager_protocol="Kingdom of Belgium",
        possible_access_route=(
            "Euronext Brussels, OTC or institutional secondary-market "
            "route through a suitable corporate broker."
        ),
        slovenian_doo_access_status="unknown",
        access_evidence_sufficient=False,
        discovery_priority="high",
        mandate_relevance="high",
        source_summary="Belgian Debt Agency issuance and market information.",
        notes=(
            "Secondary-market investability is established, but the exact "
            "Slovenian corporate broker route and specific current security "
            "remain unresolved."
        ),
    )


def _austrian_treasury_bill() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="austria_treasury_bill",
        strategy_id="austrian_sovereign_bills",
        implementation_id="current_austrian_atb_research_candidate",
        display_name="Austrian Treasury Bill",
        full_name="Republic of Austria Short-Dated Treasury Bill",
        category="direct_sovereign_bill",
        short_description=(
            "Short-term EUR Treasury bill issued by Austria."
        ),
        economic_description=(
            "The treasury would own a direct debt claim against the "
            "Republic of Austria."
        ),
        return_source=(
            "Discount yield earned through holding the bill toward "
            "redemption."
        ),
        currency="EUR",
        issuer_manager_protocol="Republic of Austria",
        possible_access_route=(
            "Institutional or corporate secondary-market bond route."
        ),
        slovenian_doo_access_status="unknown",
        access_evidence_sufficient=False,
        discovery_priority="high",
        mandate_relevance="high",
        source_summary="Austrian Treasury 2026 bill programme.",
        notes=(
            "Exact preferred bill, current economics and Slovenian corporate "
            "execution route remain unresolved."
        ),
    )


def _finnish_treasury_bill() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="finland_treasury_bill",
        strategy_id="finnish_sovereign_bills",
        implementation_id="current_finnish_bill_research_candidate",
        display_name="Finnish Treasury Bill",
        full_name="Republic of Finland Short-Dated Treasury Bill",
        category="direct_sovereign_bill",
        short_description=(
            "Short-term EUR Treasury bill issued by Finland."
        ),
        economic_description=(
            "The treasury would own a direct debt claim against the "
            "Republic of Finland."
        ),
        return_source=(
            "Discount yield earned through holding the bill toward "
            "redemption."
        ),
        currency="EUR",
        issuer_manager_protocol="Republic of Finland",
        possible_access_route=(
            "Institutional or corporate secondary-market bond route."
        ),
        slovenian_doo_access_status="unknown",
        access_evidence_sufficient=False,
        discovery_priority="medium",
        mandate_relevance="high",
        source_summary="Finnish State Treasury bill programme.",
        notes=(
            "Active EUR Treasury-bill issuance identified; exact "
            "current bill economics remain incomplete."
        ),
    )


def _eu_bill_nov_2026() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="eu_bill_nov_2026",
        strategy_id="eu_supranational_bills",
        implementation_id="EU000A4EJ3Q5",
        display_name="EU-Bill Nov 2026",
        full_name="European Union Bill EU000A4EJ3Q5",
        category="supranational_bill",
        short_description=(
            "Short-term EUR debt issued directly by the European Union."
        ),
        economic_description=(
            "The treasury owns a direct short-term debt claim against "
            "the European Union."
        ),
        return_source=(
            "Discount yield earned as the bill converges toward "
            "redemption at maturity."
        ),
        currency="EUR",
        issuer_manager_protocol="European Union",
        possible_access_route=(
            "Secondary-market bond access through a suitable "
            "corporate broker or dealer."
        ),
        slovenian_doo_access_status="unknown",
        access_evidence_sufficient=False,
        discovery_priority="high",
        mandate_relevance="high",
        preliminary_yield_pct=2.400,
        yield_as_of="2026-08-05",
        maturity_date="2026-11-06",
        source_summary="European Commission EU-Bill auction results.",
        notes=(
            "Institutional market is established, but the exact Slovenian "
            "corporate secondary-market execution route remains unresolved."
        ),
    )


def _eu_bill_feb_2027() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="eu_bill_feb_2027",
        strategy_id="eu_supranational_bills",
        implementation_id="EU000A4EPCJ1",
        display_name="EU-Bill Feb 2027",
        full_name="European Union Bill EU000A4EPCJ1",
        category="supranational_bill",
        short_description=(
            "Short-term EUR debt issued directly by the European Union."
        ),
        economic_description=(
            "The treasury owns a direct short-term debt claim against "
            "the European Union."
        ),
        return_source=(
            "Discount yield earned as the bill converges toward "
            "redemption at maturity."
        ),
        currency="EUR",
        issuer_manager_protocol="European Union",
        possible_access_route=(
            "Secondary-market bond access through a suitable "
            "corporate broker or dealer."
        ),
        slovenian_doo_access_status="unknown",
        access_evidence_sufficient=False,
        discovery_priority="high",
        mandate_relevance="high",
        preliminary_yield_pct=2.533,
        yield_as_of="2026-08-05",
        maturity_date="2027-02-05",
        source_summary="European Commission EU-Bill auction results.",
        notes=(
            "Institutional market is established, but the exact Slovenian "
            "corporate secondary-market execution route remains unresolved."
        ),
    )


def _eu_bill_aug_2027() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="eu_bill_aug_2027",
        strategy_id="eu_supranational_bills",
        implementation_id="EU000A4EYPS6",
        display_name="EU-Bill Aug 2027",
        full_name="European Union Bill EU000A4EYPS6",
        category="supranational_bill",
        short_description=(
            "Short-term EUR debt issued directly by the European Union."
        ),
        economic_description=(
            "The treasury owns a direct short-term debt claim against "
            "the European Union."
        ),
        return_source=(
            "Discount yield earned as the bill converges toward "
            "redemption at maturity."
        ),
        currency="EUR",
        issuer_manager_protocol="European Union",
        possible_access_route=(
            "Secondary-market bond access through a suitable "
            "corporate broker or dealer."
        ),
        slovenian_doo_access_status="unknown",
        access_evidence_sufficient=False,
        discovery_priority="high",
        mandate_relevance="high",
        maximum_plausible_allocation_eur=5_000_000.0,
        preliminary_yield_pct=2.704,
        yield_as_of="2026-08-05",
        maturity_date="2027-08-06",
        liquidity_summary=(
            "Approximately €1.9 billion issued at the discovery auction."
        ),
        source_summary="European Commission EU-Bill auction results.",
        notes=(
            "Institutional market is established, but the exact Slovenian "
            "corporate secondary-market execution route remains unresolved."
        ),
    )


def _esm_bill_nov_2026() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="esm_bill_nov_2026",
        strategy_id="esm_short_term_debt",
        implementation_id="EU000A4DMLY0",
        display_name="ESM Bill Nov 2026",
        full_name="European Stability Mechanism Bill EU000A4DMLY0",
        category="supranational_bill",
        short_description=(
            "Short-term EUR debt issued by the European Stability Mechanism."
        ),
        economic_description=(
            "The treasury owns a direct debt claim against the "
            "European Stability Mechanism."
        ),
        return_source=(
            "Discount yield earned as the bill converges toward "
            "redemption at maturity."
        ),
        currency="EUR",
        issuer_manager_protocol="European Stability Mechanism",
        possible_access_route=(
            "Institutional or corporate secondary-market bond route."
        ),
        slovenian_doo_access_status="unknown",
        access_evidence_sufficient=False,
        discovery_priority="medium",
        mandate_relevance="high",
        preliminary_yield_pct=2.421,
        yield_as_of="2026-08-04",
        maturity_date="2026-11-05",
        liquidity_summary=(
            "Approximately €1.598 billion issued at discovery."
        ),
        source_summary="European Stability Mechanism auction results.",
    )


def _blackrock_ics_tokenized_eur() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="blackrock_ics_tokenized_eur",
        strategy_id="blackrock_ics_euro_liquidity",
        implementation_id="tokenized_eur_share_class_research_candidate",
        display_name="BlackRock Tokenized ICS EUR",
        full_name="BlackRock Tokenized EUR ICS Money-Market Fund Access",
        category="tokenized_money_market_fund",
        short_description=(
            "Tokenized access implementation for an underlying regulated "
            "EUR institutional money-market fund."
        ),
        economic_description=(
            "The treasury would hold a tokenized representation of an "
            "interest in an underlying regulated money-market fund."
        ),
        return_source=(
            "Return is primarily generated by the underlying "
            "money-market portfolio rather than by tokenization itself."
        ),
        currency="EUR",
        issuer_manager_protocol="BlackRock",
        possible_access_route=(
            "Eligible institutional tokenized-fund subscription and "
            "approved digital-asset custody route."
        ),
        slovenian_doo_access_status="unknown",
        access_evidence_sufficient=False,
        discovery_priority="medium",
        mandate_relevance="high",
        source_summary=(
            "BlackRock 2026 European tokenized ICS announcement."
        ),
        notes=(
            "Tokenization is treated as an alternate implementation "
            "of the underlying money-market strategy."
        ),
    )


def _aave_v3_base_eurc() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="aave_base_eurc",
        strategy_id="aave_eur_lending",
        implementation_id="aave_v3_base_eurc",
        display_name="Aave V3 Base EURC",
        full_name="Aave V3 Base EURC Supply Market",
        category="defi_lending",
        short_description=(
            "EURC supplied into Aave V3's overcollateralized lending "
            "market on Base."
        ),
        economic_description=(
            "The treasury owns an onchain lending position representing "
            "supplied EURC plus accrued variable interest."
        ),
        return_source="Variable interest paid by borrowers.",
        currency="EUR",
        issuer_manager_protocol="Aave",
        possible_access_route=(
            "Bank EUR to EURC to Aave on Base and back to bank EUR."
        ),
        slovenian_doo_access_status="unknown",
        access_evidence_sufficient=False,
        discovery_priority="medium",
        mandate_relevance="medium",
        maximum_plausible_allocation_eur=5_000_000.0,
        preliminary_yield_pct=1.741,
        yield_as_of="2026-09-01",
        liquidity_summary=(
            "Existing analysis found approximately 74.20% immediate "
            "exit coverage for a €5 million position."
        ),
        source_summary="Existing V1 Aave evidence package.",
    )


def _morpho_philidor_eurc_prime() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="morpho_philidor_eurc_prime",
        strategy_id="morpho_eurc_lending",
        implementation_id="philidor_eurc_prime_ethereum",
        display_name="Morpho Philidor EURC Prime",
        full_name="Morpho Philidor EURC Prime Vault on Ethereum",
        category="defi_lending",
        short_description=(
            "Curated EURC lending vault allocating capital into "
            "Morpho lending markets."
        ),
        economic_description=(
            "The treasury would own vault shares representing EURC "
            "allocated across approved collateralized lending markets."
        ),
        return_source=(
            "Borrower interest generated by underlying Morpho lending "
            "markets after applicable vault fees."
        ),
        currency="EUR",
        issuer_manager_protocol="Morpho / Philidor",
        possible_access_route=(
            "Bank EUR to EURC to Ethereum vault and back to bank EUR."
        ),
        slovenian_doo_access_status="unknown",
        access_evidence_sufficient=False,
        discovery_priority="low",
        mandate_relevance="medium",
        maximum_plausible_allocation_eur=107_000.0,
        preliminary_yield_pct=0.0,
        yield_as_of="2026-09-01",
        liquidity_summary=(
            "Approximately 107,000 EURC discovered in the vault, making "
            "treasury-scale deployment questionable."
        ),
        source_summary="Morpho application discovery research.",
    )


def _morpho_moonwell_eurc() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="morpho_moonwell_eurc",
        strategy_id="morpho_eurc_lending",
        implementation_id="moonwell_flagship_eurc_base",
        display_name="Morpho Moonwell Flagship EURC",
        full_name="Morpho Moonwell Flagship EURC Vault on Base",
        category="defi_lending",
        short_description=(
            "Curated EURC lending vault allocating capital into "
            "Morpho markets on Base."
        ),
        economic_description=(
            "The treasury would own vault shares representing EURC "
            "allocated across collateralized lending markets."
        ),
        return_source=(
            "Borrower interest generated in underlying lending markets "
            "after applicable fees."
        ),
        currency="EUR",
        issuer_manager_protocol="Morpho / Moonwell",
        possible_access_route=(
            "Bank EUR to EURC to Base vault and back to bank EUR."
        ),
        slovenian_doo_access_status="unknown",
        access_evidence_sufficient=False,
        discovery_priority="low",
        mandate_relevance="medium",
        maximum_plausible_allocation_eur=1_038.0,
        preliminary_yield_pct=2.8,
        yield_as_of="2026-09-01",
        liquidity_summary=(
            "Approximately 1,038 EURC discovered, far below the "
            "minimum useful treasury allocation."
        ),
        source_summary="Morpho application discovery research.",
    )


def _pendle_eur_term_yield() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="pendle_eur_term_yield_unresolved",
        strategy_id="pendle_eur_term_yield",
        implementation_id="specific_market_not_yet_identified",
        display_name="Pendle EUR Term Yield",
        full_name="Pendle EUR-Linked Principal Token Research Candidate",
        category="defi_term_yield",
        short_description=(
            "Potential EUR-linked fixed or term-yield opportunity using "
            "a specific Pendle principal-token market."
        ),
        economic_description=(
            "The treasury would own a principal-token claim tied to a "
            "specific yield-bearing underlying asset and maturity."
        ),
        return_source=(
            "Potential return from purchasing the principal claim below "
            "its expected redemption value and holding toward maturity."
        ),
        currency="EUR",
        issuer_manager_protocol="Pendle",
        possible_access_route=None,
        slovenian_doo_access_status="unknown",
        access_evidence_sufficient=False,
        discovery_priority="medium",
        mandate_relevance="medium",
        source_summary="Pendle market discovery research.",
        notes=(
            "No treasury-scale specific EUR-linked PT market was "
            "established during 13B. This record preserves the evidence "
            "gap rather than inventing an investable opportunity."
        ),
    )


def _icslo() -> DiscoveryOpportunity:
    return DiscoveryOpportunity(
        opportunity_id="icslo",
        strategy_id="slovenian_public_equities",
        implementation_id="HRICAMFSBIB2",
        display_name="ICSLO",
        full_name="InterCapital SBITOP TR UCITS ETF",
        category="equity_etf",
        short_description=(
            "ETF providing exposure to major Slovenian listed equities."
        ),
        economic_description=(
            "The treasury owns equity ETF shares whose value moves with "
            "Slovenian public companies."
        ),
        return_source="Equity price appreciation and dividends.",
        currency="EUR",
        issuer_manager_protocol="InterCapital",
        possible_access_route="Ljubljana Stock Exchange brokerage.",
        slovenian_doo_access_status="verified",
        access_evidence_sufficient=True,
        discovery_priority="low",
        mandate_relevance="low",
        known_hard_mandate_conflict=True,
        known_hard_mandate_conflict_reason=(
            "Equity market risk is incompatible with the current "
            "very-high capital-preservation treasury mandate."
        ),
        source_summary="Ljubljana Stock Exchange product information.",
    )