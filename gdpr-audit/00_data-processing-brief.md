# Data Processing Brief: Autonomous Competitive Intelligence Agent

Prepared for: Data Protection Officer  
Repository: `autonomous_competitive_intelligence_agent`  
Date: 2026-05-27

## System Overview

The project is an automated competitive-intelligence and sales-prospecting system for Kairos Consulting. It takes a target company, city, and optional domain/industry, researches the company online, identifies employee contacts, scores possible AI consulting opportunities, generates a report, creates or updates CRM records, and can trigger outreach-related workflows.

The live research flow is implemented primarily through `scripts/run_research.py`, `agents/research_orchestrator.py`, and `src/workflows/intelligence_workflow.py`. The workflow searches the web, sends public company information to AI services for analysis, queries Hunter.io for contacts, scores opportunities, generates HTML/Markdown/PDF reports, uploads reports to Supabase Storage, and syncs company/contact/opportunity data into Supabase CRM tables.

Company-level information is not personal data unless it identifies, singles out, or can reasonably be linked to an individual. The system also processes multiple categories of individual-level data, which are personal data under GDPR.

## 1. Personal Data Processed

### A. Individual contact data from Hunter.io

The system calls Hunter.io domain search to retrieve business-contact data for people associated with a target company domain. This includes:

- First name and last name.
- Work email address.
- Role, job title, or position.
- Hunter.io confidence score.
- Associated company/domain context.

The confidence score is personal data because it is a third-party assessment attached to an identifiable person and affects whether that person is selected as a contact.

### B. Email engagement data

The system stores and/or processes sales-outreach engagement events connected to identifiable email recipients. This includes:

- Sent timestamps.
- Opened timestamps.
- Clicked timestamps.
- Replied timestamps.
- Bounced timestamps.
- Reply text from inbound email responses.
- Sequence status and related outreach metadata.

These events are personal data because they describe the behavior, communications, and status of identifiable recipients.

### C. AI-inferred data

The system uses AI analysis to infer or generate data about contacts and outreach outcomes. This includes:

- Reply sentiment.
- Reply intent.
- Suggested next action.
- Engagement strategy.
- Outreach prioritization and follow-up recommendations.

These outputs are personal data when linked to an identifiable person because they are inferred evaluations or predictions about that person's response, intent, and future handling.

## 2. Sources Of Personal Data And Related Inputs

The system receives or derives data from the following sources:

- Hunter.io domain search: automated third-party collection of individual contact data. The individuals did not submit this data directly to this system.
- Tavily web search snippets: public web search results and snippets about target companies, markets, and relevant business context.
- OpenAI analysis of public web content: the system sends public web-search content and company context to OpenAI for structured company analysis.
- Anthropic-generated engagement strategies: the system sends company/profile/opportunity context to Anthropic Claude to generate opportunity scores, recommendations, and engagement strategy.
- Inbound email replies: replies from recipients are processed for tracking, reply text, sentiment, intent, and next-action suggestions.

## 3. Purposes Of Processing

The system processes data for the following separate purposes:

- Prospect research: researching target companies and their market context.
- Contact discovery: identifying individual employees or business contacts at target companies.
- Sales outreach generation: drafting or supporting personalized outreach based on company research and inferred opportunities.
- Engagement tracking: recording whether outreach emails were sent, opened, clicked, replied to, or bounced.
- CRM record creation: creating and updating company, contact, opportunity, project, activity, task, sequence, and email-event records.
- Internal sales reporting: producing intelligence reports and opportunity summaries for Kairos Consulting.
- Slack/email notifications: notifying internal users about reports, workflow status, failures, or outreach-related activity.
- PDF report generation: converting generated intelligence reports into PDF format for sharing and storage.

## 4. Who Processes The Data

The following services and components process data in the system. For this brief, each is treated as a processor or processing component for the relevant operation.

- Tavily: processes search queries and returns public web-search snippets used for company and market research.
- OpenAI, using `gpt-4o-mini`: processes public web content, company context, and research snippets to produce structured company analysis.
- Anthropic Claude: processes company profiles, market context, AI opportunity data, outreach context, and email-reply content to generate opportunity scoring, engagement strategies, sentiment, intent, and next-action suggestions.
- Hunter.io: processes target company domains and returns individual contact data, including names, work emails, roles, and confidence scores.
- Supabase intelligence project: stores or supports private intelligence data, report metadata, generated reports, audit/support tables, and private report storage depending on the workflow path.
- Supabase Kairos CRM project: stores CRM data including companies, contacts, intelligence reports, projects, AI opportunities, activities, tasks, email sequences, and email events.
- Resend: processes outbound email content, recipient email addresses, and delivery metadata for sales outreach and notifications.
- Slack: processes internal notification content, which may include company names, workflow status, report links, errors, or personal data if included in notifications.
- n8n: orchestrates scheduled automation and can process target company inputs, workflow status, and error payloads.
- WeasyPrint locally: processes generated HTML reports into PDFs on the local runtime.
- Vercel, if applicable: project documentation describes a related deployed Kairos web application that can trigger the Python agent and proxy report access. If that path is active, Vercel processes request metadata, target inputs, report access traffic, and any personal data passed through those routes.

## 5. Storage Locations And Stored Data

The system stores data in the following locations:

- Local `reports/` folder: contains generated HTML, Markdown, and PDF reports. These reports can embed contact data, including names, work emails, roles, AI opportunity context, engagement strategy, and other sales-relevant information.
- Supabase Storage: stores generated reports in the private `intelligence-reports` bucket. The code creates signed URLs for access, with a default expiry of 7 days through `REPORT_URL_EXPIRY=604800`.
- Supabase CRM database: stores operational CRM records in tables including `companies`, `contacts`, `intelligence_reports`, `projects`, `ai_opportunities`, `activities`, `tasks`, `email_sequences`, and `email_events`.

The schema also defines support tables such as `opt_out_domains`, `research_runs`, `reports`, `audit_log`, `generated_reports`, and `system_settings`. Not all of these are clearly used by the main live workflow, but they are part of the project data model and should be considered during audit and retention review.

## 6. Decision-Making And Human Review

The system produces outputs that directly influence commercial decisions about which individuals and companies to target and how to approach them.

Specifically, the system:

- Scores AI consulting opportunities.
- Ranks or prioritizes contacts through Hunter.io confidence filtering and report-generation logic.
- Drafts or supports sales outreach emails.
- Generates engagement strategies.
- Determines or supports follow-up cadence through email sequence and engagement-tracking logic.
- Suggests next actions based on reply sentiment and inferred intent.

No enforced human-review step is present in the main live workflow before outreach can be triggered. Human review may occur operationally outside the code, but the repository does not enforce a mandatory approval gate before contact collection, CRM creation, outreach generation, or email-sequence activity.

## Critical GDPR Gap: Opt-Out Table Not Enforced

The database schema contains an `opt_out_domains` table. This indicates the system anticipates domain-level suppression or opt-out handling.

However, the main live workflow does not check `opt_out_domains` before:

- Running company research.
- Calling Hunter.io to collect individual contact data.
- Creating or updating company records.
- Creating or updating contact records.
- Generating reports containing contact data.
- Syncing records into the CRM.

This is the most serious gap identified in the current data-processing flow. The presence of the table does not provide meaningful protection unless the live workflow checks it before data collection and before CRM/report creation. As implemented, a domain could be opted out in the schema but still be researched, enriched, stored, and used for outreach by the main workflow.

For GDPR audit purposes, this should be treated as a priority remediation item: suppression checks should be enforced at the earliest practical point in the workflow, before third-party enrichment, AI processing, CRM writes, report generation, or outreach activity.
