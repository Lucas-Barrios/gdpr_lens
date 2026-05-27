# Law Stacking Analysis

Prepared for: Data Protection Officer  
Repository: `autonomous_competitive_intelligence_agent`  
Date: 2026-05-27

## 1. AI Act

This system uses multiple LLMs to process and generate outputs that affect identifiable people: OpenAI analyzes company and web context, Anthropic Claude scores opportunities and generates engagement strategy, and the reply-analysis flow infers sentiment, intent, and next actions from an individual's email reply. The project is not itself a general-purpose AI model provider, but it deploys general-purpose AI models inside a sales workflow that profiles individuals and generates outreach targeted at them. Depending on the final deployment, jurisdiction, and user-facing behavior, this may trigger AI Act transparency obligations for AI systems that interact with natural persons, generate synthetic text, or expose people to AI-driven inference.

The most immediate design issue is transparency. Individuals receiving AI-drafted outreach may have a right to know that the message was generated or materially shaped by AI, and individuals whose replies are analyzed may need to be told that AI is being used to infer sentiment, intent, or recommended follow-up. The system currently has no disclosure in generated outreach, no email footer explaining AI involvement, no privacy notice hook, and no recipient-facing explanation of AI profiling. This is a separate gap from GDPR lawful basis: even if Kairos could establish a GDPR basis for processing, the AI Act may still require clear, recognizable disclosure at or before first interaction.

## 2. ePrivacy

The source stores and updates individual-level email engagement fields including `opened_at`, `first_click_at`, `replied_at`, `bounced_at`, and `unsubscribed_at`; the project uses Resend for email delivery and message IDs. Where Resend open and click tracking is enabled, opens are typically detected through tracking pixels and clicks through rewritten or tracked links, which means the system is measuring electronic communication behavior at the recipient-device level. Under ePrivacy rules, this is not solved by GDPR legitimate interests alone: accessing or storing information on a recipient's device, or monitoring interaction with an email, generally requires prior informed consent unless a narrow technical necessity exemption applies.

For Kairos, the German implementation is especially important because Kairos is Berlin-based. Germany's rule is now the TDDDG, formerly TTDSG; section 25 requires consent for storing information in or accessing information from terminal equipment, except for narrow transmission or strictly necessary service exceptions. Tracking pixels in professional emails are therefore high risk in Germany and should be treated as requiring consent before activation, even in a B2B context. The current system has no consent mechanism for email tracking, no per-recipient tracking opt-in state, and no logic to disable open/click tracking when consent is absent; this is a separate legal gap from GDPR.

## 3. Data Act And Other Supply Chain Exposure

The EU Data Act is not the primary legal regime for this project because the system is not mainly about connected-product data access or IoT-generated product data. The more relevant "other law" risk is supply-chain compliance: Hunter.io's own collection, retention, and commercialization of professional contact data is a dependency for Kairos's downstream processing. If Hunter.io's source database, transparency process, objection handling, or lawful basis is later found non-compliant, Kairos inherits practical and legal risk because Kairos chose that source and then combined the data with CRM records, AI-generated outreach, engagement tracking, and reply profiling. Kairos therefore needs vendor due diligence that covers Hunter.io as both data source and processor, not merely API availability or a processor DPA.

The planned or potential Phase 2 use of LinkedIn scraping through Apify would add materially higher exposure. LinkedIn's terms of service generally prohibit scraping and automated extraction, and professional-profile data remains personal data even when visible online. EU case law and regulator practice around large-scale automated collection of publicly available personal data make it unsafe to assume that public visibility equals lawful reuse for sales profiling. Any LinkedIn scraping plan should be treated as a separate legal workstream requiring terms-of-service review, lawful-basis analysis, purpose-compatibility analysis, DPIA update, and explicit approval before implementation.

## Law Stack Summary

This system sits at the intersection of GDPR, ePrivacy, and the emerging AI Act compliance regime. GDPR governs personal data processing, profiling, lawful basis, data subject rights, processor contracts, retention, international transfers, and DPIA obligations. ePrivacy separately governs unsolicited commercial email and email tracking technologies such as pixels and tracked links, with German TDDDG consent rules creating a particularly strict track for Kairos. The AI Act adds transparency expectations for AI-generated communications and AI-driven interaction or inference about individuals.

These frameworks impose distinct requirements and cannot be collapsed into one "GDPR compliance" exercise. A valid GDPR legitimate-interest assessment would not by itself legalize open/click tracking, unsolicited commercial email, or undisclosed AI-generated outreach. Likewise, an AI disclosure would not fix missing lawful basis, missing suppression enforcement, or uncontrolled local PDF retention. Satisfying GDPR alone is insufficient for lawful operation.

## Source Notes

- EU AI Act, Regulation (EU) 2024/1689, including Article 50 transparency obligations: https://eur-lex.europa.eu/eli/reg/2024/1689/
- European Commission AI Act overview, noting transparency rules taking effect in August 2026: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
- German TDDDG section 25 on terminal-equipment privacy and consent: https://www.gesetze-im-internet.juris.de/ttdsg/__25.html
- EU Data Act overview: https://digital-strategy.ec.europa.eu/en/policies/data-act
