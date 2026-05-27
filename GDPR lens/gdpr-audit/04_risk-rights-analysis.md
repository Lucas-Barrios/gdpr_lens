# Risk And Rights Analysis

Prepared for: Data Protection Officer  
Repository: `autonomous_competitive_intelligence_agent`  
Date: 2026-05-27

## 1. Special Category Data

AI-inferred company pain points, contact reply content, and sentiment analysis could reveal or imply Article 9 special category data depending on the target organization and the content of the reply. A contact at a medical clinic, church, political organization, trade union, NGO, or advocacy group could have their role, employer, reply text, or inferred intent analyzed in a way that reveals health status, religious affiliation, trade union membership, political views, or related sensitive context. The system has no mechanism to detect, classify, suppress, or route possible special category data for separate handling. This is a design-level risk requiring mitigation before live processing, including exclusion rules, sensitive-domain blocking, AI prompt constraints, and human review for sensitive sectors.

## 2. Automated Decision-Making And Profiling

The system scores AI opportunities, ranks or prioritizes contacts, drafts outreach, determines follow-up cadence, and analyzes reply sentiment/intent without a documented human-review gate before outreach is sent. The reply sentiment and intent analysis informs next-action decisions about identifiable individuals, including whether to follow up, archive, complete, or send for human review. This chain constitutes profiling with potentially significant effects because it influences which individuals are targeted, how persistently they are contacted, and how their replies are interpreted. Article 22 requires safeguards such as meaningful information or explanation, the right to obtain human review, and the right to contest the decision; none of these are currently implemented in the live workflow.

## 3. DPIA Trigger

Applying the nine EDPB DPIA criteria: evaluation/scoring of people is YES because contacts are scored indirectly through opportunity and contact prioritization; automated decision-making with significant effects is YES because the system influences outreach targeting and follow-up cadence; systematic monitoring is YES because email engagement is tracked at individual level; special category data at scale is POSSIBLE for sensitive-sector targets; and large-scale processing DEPENDS, but must be watched as the client list grows. Matching or combining datasets is YES because Hunter.io contact data is combined with web research and AI-inferred attributes; vulnerable people is LOW in a B2B context but still needs screening; innovative technology is YES because the system uses a multi-LLM pipeline with sentiment profiling; and cross-border transfer preventing rights exercise is YES because all processors are US-based. At least five criteria clearly apply: evaluation/scoring, automated decision-making, systematic monitoring, matching/combining datasets, innovative technology, and cross-border transfer risk. A DPIA is required before this system processes real contact data at scale; this is a hard requirement, not a recommendation.

## 4. Data Subject Rights Friction

A contact whose email was collected through Hunter.io and profiled by the system has rights to access, erasure, objection to profiling, and restriction of processing. The `opt_out_domains` table exists, but the live workflow does not check it before research, Hunter.io collection, CRM creation, report generation, or outreach, meaning an opted-out contact or domain could still be researched and contacted. This is an active compliance gap, not a future risk. Local PDF, HTML, and Markdown reports containing contact data also have no documented deletion mechanism, so suppression enforcement and report deletion must both be resolved before deployment.

