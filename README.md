# GDPR Audit — B2B Sales Intelligence Research System

This audit covers the current development phase of the Kairos B2B sales intelligence research system: a Python-based workflow that researches target companies, enriches them with Hunter.io contact data, analyzes company and outreach context through OpenAI and Anthropic, stores CRM/report records in Supabase, generates local HTML/Markdown/PDF reports, and supports outbound email tracking through Resend. The review focuses on the system as implemented in source code and documented architecture before full production deployment with real contact data. Bottom line: **PROCEED WITH CONDITIONS**. The system should not process real contact data or send outreach until the hard blockers below are resolved.

## File Map

| File | Purpose |
|---|---|
| `gdpr-audit/00_data-processing-brief.md` | Plain-language system overview for a DPO, covering personal data categories, sources, purposes, processors, storage, decision-making, and the opt-out gap. |
| `gdpr-audit/01_personal-data-inventory.md` | Inventory table mapping data categories to sources, purposes, retention posture, and EU-US transfer exposure. |
| `gdpr-audit/02_role-map.md` | Controller/processor role map, DPA status, Hunter.io dual-role analysis, and international transfer requirements. |
| `gdpr-audit/03_lawful-basis.md` | Purpose-by-purpose lawful-basis assessment, cold outreach LIA, reply profiling analysis, and ePrivacy note. |
| `gdpr-audit/04_risk-rights-analysis.md` | Special category risk, Article 22 profiling risk, DPIA trigger analysis, and data subject rights friction. |
| `gdpr-audit/05_law-stacking.md` | AI Act, ePrivacy/German TDDDG, supply-chain, LinkedIn scraping, and broader law-stack analysis. |
| `gdpr-audit/06_compliance-memo.md` | Client-facing legal counsel memo with bottom line, required actions, residual risks, and disclaimer. |

## Critical Open Items

1. **Activate the opt-out check.** The `opt_out_domains` table exists but is not called in the live research workflow before research, Hunter.io enrichment, CRM creation, report generation, or outreach. Owner: developer. Timeline: immediate.

2. **Establish DPAs with all active processors.** Anthropic, OpenAI, Supabase, Hunter.io, Resend, Tavily, Slack, and n8n must have signed or formally accepted DPAs before any live personal data flows. Owner: legal counsel and developer. Timeline: before any live run.

3. **Conduct a DPIA before pilot deployment.** At least five EDPB DPIA criteria apply, and the DPIA must address the German TDDDG/ePrivacy consent gap for email tracking pixels and tracked links. Owner: legal counsel. Timeline: before pilot deployment.

## Disclaimer

This audit pack is a first-pass consultant assessment based on the reviewed repository and related project documentation. It is not a legal opinion, not a completed DPIA, not a certification, and not evidence of GDPR, ePrivacy, AI Act, or international transfer compliance. Kairos must engage qualified legal counsel before relying on this assessment for compliance decisions or processing live personal data.
