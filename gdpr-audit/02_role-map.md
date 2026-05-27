# GDPR Role Map

Prepared for: Data Protection Officer  
Repository: `autonomous_competitive_intelligence_agent`  
Date: 2026-05-27

This role map is based on the project source and `gdpr-audit/00_data-processing-brief.md`. No signed DPAs or vendor contract records were found in the repository, so "DPA in place" means "evidenced for this deployment," not merely that a vendor publishes a template.

| Entity | Role | Processing Activity | DPA in Place? |
|---|---|---|---|
| Kairos Consulting | Controller | Defines research targets, selects companies/domains, owns the CRM records, determines outreach strategy, triggers or permits outreach, and decides how reports and engagement data are used. | Not applicable as controller. Kairos must maintain Article 30 records, lawful-basis analysis, transparency notices, opt-out handling, processor contracts, and transfer documentation. |
| Tavily | Processor | Executes web searches on Kairos's behalf and returns public web snippets used for prospect research and company analysis. Queries and snippets may include personal data if names, roles, or other identifiers appear in public web results. | Not evidenced in repo. Must be reviewed and an Article 28 DPA plus transfer terms must be established before sending personal data or personal-data-bearing prompts/searches. Tavily terms reviewed separately do not by themselves evidence an executed DPA for this deployment. |
| OpenAI | Processor | Receives company context and web content, including public snippets, and returns structured company analysis through `gpt-4o-mini`. Personal data may be included where public content or company context identifies individuals. | Not evidenced in repo. OpenAI publishes a DPA, but Kairos must actively sign, accept, or otherwise confirm it applies to the API account and this processing. Do not assume coverage from API use alone. |
| Anthropic Claude | Processor | Receives company/contact context and returns opportunity scores, engagement strategies, outreach drafts, reply sentiment, reply intent, and next-action suggestions. | Not evidenced in repo. Anthropic publishes/incorporates a commercial DPA with SCCs, but Kairos must confirm the relevant Claude/API commercial terms were accepted for this account and cover this processing. |
| Hunter.io | Dual role: data source and processor | Acts as a source of professional contact data and actively queries its database on Kairos's behalf. Returns names, work emails, roles, and confidence scores. | Not evidenced in repo. Hunter.io's dual role creates a separate compliance obligation: Kairos must have processor terms for the query/enrichment service and must also confirm Hunter.io's own controller lawful basis, transparency approach, and data-subject-rights process for holding and supplying the contact data. |
| Supabase (intelligence DB) | Processor | Stores or supports research runs, generated reports, report metadata, audit/support tables, opt-out table, and private report storage depending on workflow path. | Not evidenced in repo. Supabase publishes a DPA, but Kairos must actively sign/accept it for the relevant Supabase organization/project. The DPA must cover storage, backups, logs, support access, and sub-processors. |
| Supabase (shared CRM DB) | Processor | Stores CRM records including companies, contacts, intelligence reports, projects, AI opportunities, activities, tasks, email sequences, and email engagement events. | Not evidenced in repo. A Supabase DPA must be actively signed/accepted for this separate CRM project as well; do not assume the intelligence-project DPA covers a different Supabase organization or project. |
| Resend | Processor | Sends emails from the Kairos domain, processes recipient names/emails, message content, delivery metadata, and individual-level engagement tracking such as opens, clicks, replies, bounces, and unsubscribes. | Not evidenced in repo. Resend publishes a DPA, but Kairos must review and accept/execute it, including tracking, message-content, retention, sub-processor, and transfer terms. |
| Slack | Processor | Receives internal notifications that may include company details, report links, errors, and potentially contact names or other personal data if included in notification payloads. | Not evidenced in repo. Slack publishes DPA/SCC materials, but Kairos must review and accept/execute them for the workspace used by this system. Notification payloads should be minimized regardless of DPA status. |
| n8n | Processor | Orchestrates batch runs, passes target data and workflow outputs between services, and may process command outputs, errors, company details, report links, and personal data if included in workflow payloads. | Not evidenced in repo. If n8n Cloud is used, Kairos must establish n8n's DPA and transfer terms. If self-hosted, Kairos must document the hosting provider and any infrastructure processors instead. |

## Hunter.io Dual-Role Compliance Flag

Hunter.io is not just a passive API processor in this system. It is also the source of the professional contact database being queried. That creates two parallel compliance questions:

- Processor question: whether Hunter.io has an Article 28 DPA with Kairos for account usage, API queries, enrichment activity, and any customer lead data processed on Kairos's behalf.
- Source/controller question: whether Hunter.io has its own lawful basis, transparency notices, objection handling, and data-subject-rights workflow for the contact records it holds and supplies before Kairos queries them.

Kairos cannot satisfy this issue merely by signing a processor DPA. It must also document vendor due diligence on Hunter.io's own lawful basis for collecting, retaining, and commercializing professional contact data.

## International Transfers

All processors in the live processing chain should be treated as US-based for this audit. This creates a full-stack US transfer chain for personal data, including contact identifiers, outreach content, engagement events, reply text, and AI-inferred attributes.

For standard commercial data flows, Kairos should not assume an adequacy decision applies simply because a vendor publishes GDPR language or uses EU infrastructure. Each processor needs a documented Chapter V transfer mechanism, normally:

- Article 46 Standard Contractual Clauses, usually Module Two for controller-to-processor transfers.
- A transfer impact assessment for the specific vendor and data flow.
- Supplementary technical and organizational measures where needed.
- Onward-transfer controls for sub-processors.
- Evidence that the relevant DPA/SCCs were actively signed, accepted, or incorporated into the account agreement.

| Processor | Transfer Mechanism To Document |
|---|---|
| Tavily | Article 28 DPA plus SCCs and transfer impact assessment. If Tavily cannot provide processor/SCC terms for API use, avoid sending personal data or personal-data-bearing queries. |
| OpenAI | OpenAI DPA plus SCCs, actively accepted for the API account. Confirm it applies to `gpt-4o-mini` API processing and any sub-processors. |
| Anthropic Claude | Anthropic commercial DPA plus SCCs, actively accepted through the applicable Claude/API commercial terms. Confirm coverage for opportunity scoring, outreach drafting, and reply analysis. |
| Hunter.io | DPA plus SCCs for processor activity, plus documented due diligence for Hunter.io's controller/source role and lawful basis for the underlying contact database. |
| Supabase (intelligence DB) | Supabase DPA plus SCCs for the intelligence project, including storage, database, backups, logs, support access, and sub-processors. |
| Supabase (shared CRM DB) | Supabase DPA plus SCCs for the shared CRM project. Treat this as a separate transfer record because it stores contacts, email sequences, and engagement events. |
| Resend | Resend DPA plus SCCs and review of open/click tracking, message-content processing, retention, and sub-processors. If relying on any Data Privacy Framework certification, verify current certification and contractual scope first. |
| Slack | Slack DPA plus SCCs for workspace notifications. Minimize personal data in Slack payloads because Slack is not the system of record and notification data is harder to govern. |
| n8n | DPA plus SCCs if n8n Cloud is used. If self-hosted, document the hosting provider's DPA/SCCs and treat n8n as an internal orchestration component running on processor infrastructure. |

Supabase, OpenAI, and Anthropic publish DPAs or DPA/SCC terms, but these must be actively signed, accepted, or otherwise incorporated into the specific accounts used by Kairos. Hunter.io, Tavily, Resend, and Slack must each be separately reviewed for DPA coverage, SCCs, sub-processors, retention, and role clarity.

## Vendor DPA Review Notes

- OpenAI: DPA published for API/business services; must be confirmed for the exact Kairos account.
- Anthropic: commercial DPA with SCCs is described as incorporated into commercial terms; must be confirmed for the exact Claude/API account.
- Supabase: DPA is published; must be signed/accepted for both the intelligence and shared CRM projects.
- Hunter.io: DPA and GDPR materials identify both controller and processor roles; Kairos must review both roles, not only processor terms.
- Resend: DPA is published and covers email/message data and tracking; Kairos must review tracking and transfer terms.
- Slack: GDPR/DPA materials are published and include SCC language; Kairos must confirm acceptance for the workspace.
- Tavily: official terms and privacy materials must be reviewed further for processor terms, SCCs, customer-input handling, and any AI or third-party provider processing.
