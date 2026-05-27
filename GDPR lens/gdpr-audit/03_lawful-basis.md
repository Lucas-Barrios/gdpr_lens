# Lawful Basis Assessment

Prepared for: Data Protection Officer  
Repository: `autonomous_competitive_intelligence_agent`  
Date: 2026-05-27

This document is a preliminary GDPR lawful-basis assessment for the system described in `00_data-processing-brief.md`, `01_personal-data-inventory.md`, and `02_role-map.md`. It is not a final legal conclusion. The entries marked for legal review require controller-level approval before production use.

## Lawful Basis Matrix

| Purpose | Proposed Lawful Basis | One-Line Justification | Flag for Legal Review? |
|---|---|---|---|
| Prospect research on companies using public web content | Legitimate interests, Article 6(1)(f), where the output remains company-level | Kairos has a commercial interest in identifying potential consulting prospects, and company-level research is generally less intrusive if no individual-level data is included. | Yes, if public snippets identify individual employees or are later combined with contact data. |
| Contact data collection via Hunter.io | TBD; possible legitimate interests only if a full LIA passes | Collecting names, work emails, roles, and confidence scores from a third-party broker is more intrusive than ordinary company research, and individuals did not provide the data to Kairos. | Yes. This is a core legal-risk area. |
| Storage of contact data in Supabase CRM | Legitimate interests only if collection is lawful, minimized, transparent, and suppressions are enforced | CRM storage may support B2B sales operations, but it depends on the upstream Hunter.io collection and must be limited by retention, objection, and opt-out controls. | Yes. Current workflow does not enforce `opt_out_domains`. |
| CRM record creation for companies, projects, opportunities, activities, and tasks | Legitimate interests, Article 6(1)(f), for internal sales administration | Internal CRM operations can support a legitimate commercial purpose, but personal data fields must be minimized and not retained indefinitely. | Yes, where records include named contacts, tasks assigned to contact follow-up, or outreach status. |
| AI-generated outreach drafting linked to named individuals | TBD; possible legitimate interests only after a narrowed LIA and DPIA-style risk review | Personalized drafting linked to a named person goes beyond company research and uses AI to shape how an individual will be approached. | Yes. High risk, especially when combined with brokered contact data. |
| Sending cold outreach emails to B2B contacts who did not opt in | GDPR: possible legitimate interests for narrowly targeted B2B outreach; ePrivacy: separate consent or soft opt-in analysis required | Legitimate interests is common in B2B sales, but GDPR lawful basis does not override ePrivacy rules for unsolicited commercial email. | Yes. Must be reviewed under both GDPR and national ePrivacy implementation. |
| Email engagement tracking: sent, opened, clicked, replied, bounced timestamps | TBD; possible legitimate interests for minimal delivery/admin records, but open/click tracking needs separate ePrivacy review | Delivery and reply status may be operationally useful, but individual open/click tracking is behavioral monitoring and may require consent depending on implementation and local law. | Yes. Tracking pixels and link tracking are separate from merely sending an email. |
| Processing reply text from inbound emails | Legitimate interests for handling correspondence, if limited to human-readable CRM context | If a person replies, Kairos has a business need to process the content to respond, but reuse for profiling or automated sequence decisions changes the risk. | Yes, if reply text is sent to AI or used for automated next-action logic. |
| Reply sentiment and intent analysis via Anthropic | TBD; legal review required | This is profiling: the individual did not consent to AI analysis of their reply to infer psychological state, commercial intent, or recommended treatment. | Yes. Highest-risk processing activity in the system. |
| AI next-action recommendation for follow-up, archive, completed, or human review | TBD; possible legitimate interests only with human review, transparency, and opt-out controls | Recommendations directly affect how an identifiable person is treated in sales follow-up and are based on inferred attributes. | Yes. Requires review with profiling and automated-decision controls. |
| Follow-up cadence and email sequence scheduling | TBD; possible legitimate interests only if outreach itself is lawful and ePrivacy-compliant | Sequencing increases persistence and intrusiveness; the lawful basis depends on whether the original contact and email were lawful. | Yes. Current opt-out enforcement is insufficient. |
| Internal sales reporting using generated intelligence reports | Legitimate interests where reports are minimized and primarily company-level | Internal reporting supports sales operations, but named contacts and AI-inferred engagement strategy inside reports turn them into personal-data records. | Yes, where reports include contact names, work emails, roles, or personalized outreach content. |
| Slack/email notifications containing report links or contact data | Legitimate interests for operational alerts, only with strict minimization | Notifications may support workflow operations, but Slack/email should not become an uncontrolled duplicate store of personal data. | Yes. Minimize payloads and avoid contact details where possible. |
| PDF report generation containing contacts and outreach strategy | Legitimate interests only if report creation is necessary and deletion is controlled | PDF generation may support internal review, but embedding named contacts creates portable personal-data files outside normal database controls. | Yes. |
| Storing contacts in local PDF/HTML/Markdown reports with no deletion mechanism | No defensible standalone basis as currently controlled; remediation required | Even if report generation has a sales purpose, uncontrolled local retention is not necessary or proportionate and conflicts with storage limitation. | Yes. Critical retention and access-control issue. |
| Supabase Storage signed URLs for reports | Legitimate interests only if access is restricted, time-limited, and logged | Seven-day signed URLs reduce exposure, but the underlying report may contain contact data and should not be broadly shared. | Yes, where reports include personal data. |
| Maintaining opt-out or suppression records | Legitimate interests and legal obligation depending on applicable marketing law | Suppression records are needed to respect objections and prevent future unlawful outreach. | No for the concept; yes for implementation because the current workflow does not enforce `opt_out_domains`. |

## Three-Part LIA For Cold B2B Outreach

### 1. Legitimate interest

Kairos has a commercial interest in identifying companies that may need AI consulting services and contacting relevant business decision-makers. In a B2B context, direct marketing and business development may be capable of falling under legitimate interests if the outreach is targeted, proportionate, transparent, and subject to objection rights.

### 2. Necessity

Some processing may be necessary to identify a relevant business contact rather than sending generic messages to unrelated recipients. However, the full current stack is not obviously necessary:

- Automated Hunter.io collection is more intrusive than using a company's public contact form, generic business inbox, or manually verified public contact details.
- AI-personalized drafting linked to named people is more intrusive than generic company-level outreach.
- Open/click tracking and reply sentiment analysis are not necessary to send a single B2B introduction.
- Follow-up automation can be replaced with manual review, shorter retention, and suppression-first controls.

The necessity test is therefore weak for the combined processing chain. A less intrusive approach is available: company-level research, no brokered contact enrichment unless needed, manual contact verification, no open/click tracking by default, no AI reply profiling, clear opt-out in every message, and enforced suppression before collection or outreach.

### 3. Balancing

The balancing test is not straightforward. Contacts may have published work emails for professional contact, but that does not mean they reasonably expect:

- Their details to be collected from Hunter.io by an unrelated company.
- Their work email to be used in automated outreach sequences.
- Their interactions to be tracked at open/click level.
- Their replies to be analyzed by AI for sentiment, intent, and next-action recommendations.
- Their names and emails to be embedded in local PDF reports with no deletion mechanism.

The current system increases risk because `opt_out_domains` exists but is not checked before contact collection, CRM creation, or report generation. Until suppression is enforced and the tracking/profiling scope is reduced, legitimate interests may be arguable only for narrow, low-volume, transparent B2B contact. It is not a clean basis for the full current workflow.

Conclusion: flag for legal review before any cold outreach campaign. Document a full LIA, implement suppression checks before Hunter.io, include transparency and objection mechanisms, and separate GDPR lawful basis from ePrivacy permission to send the email.

## Reply Sentiment And Intent Analysis

Reply sentiment and intent analysis via Anthropic is profiling because it uses personal data to evaluate or predict aspects of an identifiable person, including attitude, commercial intent, and likely next response. The individual has not consented to AI analysis of their reply for those inferences.

Proposed lawful basis: TBD pending legal review. This should be treated as the highest-risk activity in the system.

Minimum remediation before use:

- Do not send reply text to Anthropic unless a lawful basis is confirmed.
- Add a human-review gate before any next action based on inferred sentiment or intent.
- Provide transparency that replies may be processed by AI if this processing continues.
- Store only the minimum tags needed, with a short retention period.
- Allow objection and deletion of inferred attributes.

## ePrivacy Note: Separate Legal Track

GDPR lawful basis is not enough to send commercial email. Unsolicited commercial email to individuals is also governed by ePrivacy rules and national implementations.

For B2B cold outreach, Kairos must determine whether the recipient's jurisdiction requires:

- Prior consent for unsolicited commercial email; or
- A valid soft opt-in rule, normally limited to existing customers where the contact details were obtained in the context of a sale or service, the marketing concerns similar products or services, and the person was given a clear opt-out at collection and in every later message.

For Hunter.io contacts who did not opt in and are not existing customers, the soft opt-in path is likely unavailable. This must be handled as a separate legal review track before sending outreach, independent of any GDPR legitimate-interests conclusion.

Open/click tracking also needs ePrivacy review because it may involve tracking technologies or terminal-equipment access separate from the content of the email itself.

## Source Notes

- GDPR Article 6(1)(f): legitimate interests requires necessity and balancing against the data subject's rights and freedoms. Official EUR-Lex text: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
- EDPB Guidelines 1/2024 analyze criteria for Article 6(1)(f) legitimate interests: https://www.edpb.europa.eu/our-work-tools/documents/public-consultations/2024/guidelines-12024-processing-personal-data-based_fr
- EDPB SME guidance describes profiling under Article 4(4) GDPR and automated-decision concerns: https://www.edpb.europa.eu/sme-data-protection-guide/respect-individuals-rights_en
- ePrivacy Directive Article 13 governs unsolicited communications and soft opt-in rules. Official EUR-Lex text: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32002L0058
- ICO guidance summarizes the legitimate-interests three-part test and notes that direct marketing must also comply with electronic-communications rules: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/legitimate-interests/what-is-the-legitimate-interests-basis/