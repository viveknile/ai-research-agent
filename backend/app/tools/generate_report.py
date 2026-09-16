from app.agents.state import ResearchState
from app.schemas.research import (
    FinalReportFinding,
    ReportCitation,
    ResearchReport,
)


async def generate_report(state: ResearchState) -> dict:
    draft = state.get("report_draft", {})

    sources = state.get("sources", [])
    evidence = state.get("evidence", [])

    evidence_lookup = {
        item["id"]: item
        for item in evidence
    }

    # ==================================================
    # Create citation records
    # ==================================================

    citations: list[ReportCitation] = []
    citation_lookup: dict[str, str] = {}

    for index, source in enumerate(sources):
        citation_id = f"source-{index + 1}"

        citation = ReportCitation(
            citation_id=citation_id,
            source_id=source["id"],
            title=source["title"],
            url=source["url"],
            domain=source["domain"],
        )

        citations.append(citation)

        citation_lookup[source["id"]] = citation_id

    # ==================================================
    # Convert draft findings into final findings
    # ==================================================

    final_findings: list[FinalReportFinding] = []

    for finding in draft.get("findings", []):
        citation_ids: list[str] = []

        evidence_ids = finding.get(
            "evidence_ids",
            [],
        )

        for evidence_id in evidence_ids:
            evidence_item = evidence_lookup.get(
                evidence_id
            )

            if not evidence_item:
                continue

            source_id = evidence_item["source_id"]

            citation_id = citation_lookup.get(
                source_id
            )

            if (
                citation_id
                and citation_id not in citation_ids
            ):
                citation_ids.append(citation_id)

        final_findings.append(
            FinalReportFinding(
                statement=finding["statement"],
                confidence=finding["confidence"],
                citation_ids=citation_ids,
            )
        )

    # ==================================================
    # Development fallback
    # ==================================================
    #
    # The mock model does not know the UUIDs generated
    # dynamically during evidence extraction.
    #
    # Therefore attach the first real source to findings
    # that do not have a citation.
    #
    # This fallback is only for mock development.
    # ==================================================

    if citations:
        for finding in final_findings:
            if not finding.citation_ids:
                finding.citation_ids = [
                    citations[0].citation_id
                ]

    # ==================================================
    # Build final report
    # ==================================================

    report = ResearchReport(
        title=draft.get(
            "title",
            "ResearchPilot Report",
        ),
        executive_summary=draft.get(
            "executive_summary",
            "No executive summary was generated.",
        ),
        findings=final_findings,
        citations=citations,
    )

    return {
        "final_report": report.model_dump(),
    }