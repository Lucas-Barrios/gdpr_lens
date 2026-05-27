# Compliance Memo

To: Kairos Legal Counsel  
Subject: Conditions for Processing Contact Data and Outreach

Bottom line: PROCEED WITH CONDITIONS. The system cannot process real contact data or send outreach until three hard blockers are resolved. The combined use of Hunter.io-sourced contact data, multi-LLM profiling, email engagement tracking, sentiment/intent analysis, and a non-functional opt-out check creates compliance exposure that outweighs the operational risk of delaying launch.

## Required Actions

1. Activate the opt-out check. The `opt_out_domains` table exists, but the live research workflow does not call it before research, Hunter.io enrichment, CRM creation, report generation, or outreach. This must be fixed in code before any real company is researched. This is a one-day engineering fix, not a legal project, and there is no defensible reason for it to remain open. Owner: developer. Timeline: immediate.

2. Establish DPAs with all active processors before any live data flows. Anthropic, OpenAI, Supabase, Hunter.io, Resend, Tavily, Slack, and n8n all process personal data or personal-data-bearing workflow payloads. Supabase and OpenAI publish standard DPAs; accept them formally and retain evidence. Hunter.io and Tavily require specific review because Hunter.io is both data source and processor, and Tavily's processor terms must be verified. No personal data should flow to any processor without a signed or formally accepted DPA. Owner: legal counsel and developer. Timeline: before any live run.

3. Conduct a DPIA before deploying at any scale. At least five EDPB criteria apply: systematic monitoring, automated profiling, dataset combination, innovative technology, and cross-border transfers. The DPIA is legally required, not optional. It must also address ePrivacy: email tracking pixels and tracked links require consent under German TTDSG, which GDPR legitimate interests does not satisfy. Owner: legal counsel. Timeline: before pilot deployment.

## Residual Risks

Reply sentiment/intent analysis via Anthropic has no clearly defensible lawful basis under current GDPR interpretation. Legal counsel must decide whether this feature can be retained, narrowed to human-assisted review, or disabled.

Local PDF, HTML, and Markdown reports containing contact data have no deletion mechanism. Kairos needs an enforceable local-file retention and deletion policy before production use.

Hunter.io supply-chain compliance remains outside Kairos's direct control. If Hunter.io's collection practices are challenged, downstream exposure follows.

## Disclaimer

This is a first-pass consultant assessment, not a legal opinion, not a DPIA, and not a certification. Kairos must engage qualified legal counsel before relying on this assessment for compliance decisions.
