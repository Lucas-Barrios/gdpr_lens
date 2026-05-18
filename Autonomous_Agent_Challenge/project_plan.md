# Autonomous Agent Project Plan
## AI-Powered Lead Generation & Qualification System for Kairos Consulting

**Author:** Lucas Barrios  
**Company:** Kairos Consulting  
**Date:** May 18, 2026  
**Lab:** Ironhack Autonomous Agent Challenge  

---

## 1. Executive Summary

### Problem Statement
Kairos Consulting currently has no automated lead qualification or outbound prospecting system. All inbound leads from the website contact form require manual review and qualification, creating bottlenecks and missed opportunities. There is no systematic way to identify and research potential clients before they contact us.

### Solution
A three-phase autonomous agent system that:
1. **Automatically qualifies inbound leads** from website forms and routes them to the appropriate HubSpot pipeline stage
2. **Proactively finds and researches outbound prospects** from the web with comprehensive lead intelligence
3. **Drafts personalized outreach messages** and provides decision-maker contact information

### Target Users
- Lucas Barrios (primary user - receives qualified leads and prospect research)
- Future sales team members as Kairos scales
- Marketing team (for lead scoring insights and conversion optimization)

### Target Customers (Kairos ICP)
**Primary Industries:**
- Wellness & Fitness Studios (gyms, yoga studios, wellness centers)
- Aesthetic Clinics (cosmetic, dermatology practices)
- Private Medical Clinics (general practice, specialists)
- Hairdressers & Beauty Salons (hair, nails, spa services)
- Real Estate Agencies (residential, commercial brokers)

**Services Offered:**
- AI Strategy & Readiness Assessment
- Workflow Automation
- CRM & Process Optimization
- AI Chatbots & Client Intake
- Marketing & Content Automation
- Fractional AI Consultant
- AI Training for Teams
- End-to-End Implementation

### Success Criteria
- **Phase 1:** 90%+ of inbound leads automatically qualified and routed to HubSpot within 2 minutes of form submission
- **Phase 2:** 20+ high-quality outbound prospects researched per week with 80%+ accuracy on company data
- **Phase 3:** 30%+ reduction in time from lead identification to first outreach

### Current Manual Process
1. Prospect fills contact form on kairosconsulting.co
2. Form data sent to backend (Supabase)
3. Lucas manually reviews submission in admin dashboard
4. Lucas manually creates HubSpot deal
5. Lucas manually researches company and writes personalized outreach
6. For outbound: Lucas manually searches web for prospects, researches each company individually

**Time cost:** 15-30 minutes per inbound lead, 45-90 minutes per outbound prospect

---

## 2. Technology Stack

### Core Agent Infrastructure

**LLM:** Claude 3.5 Sonnet via Anthropic API
- **Justification:** Superior reasoning for lead qualification scoring, better at structured output than GPT-4, familiar to development team, strong multilingual support (German/Spanish required)
- **Alternative considered:** GPT-4o (cheaper but weaker reasoning on complex qualification logic)
- **Cost estimate:** $0.50-1.50 per lead (Phase 1), $2-4 per researched prospect (Phase 2)

**Agent Framework:** LangChain (Phase 1) → LangGraph (Phase 2+)
- **Phase 1:** Simple LangChain agent sufficient for inbound qualification
- **Phase 2+:** LangGraph needed for multi-step research workflow (search → analyze → score → draft → verify)
- **Justification:** LangGraph provides state management and complex workflow orchestration needed for autonomous prospect research
- **Alternative considered:** Custom Python orchestration (more flexible but higher development cost)

**Orchestration:** n8n
- **Justification:** Already familiar from course, visual workflow builder, strong HubSpot/webhook integrations, self-hostable
- **Alternative considered:** Zapier (easier but expensive at scale, less control)

**Vector Database:** Pinecone (Phase 2+)
- **Purpose:** Store and retrieve similar past successful/unsuccessful leads for improved scoring
- **Justification:** Fast, managed service, good Python SDK
- **Alternative considered:** Chroma (free but requires hosting)

### Integrations & Tools

**Existing Infrastructure (No Changes Required):**
- Website contact form → Supabase backend
- HubSpot CRM (Pipeline: Lead → Outreach Sent → Discovery Call Booked → Proposal Sent)
- Calendly (Discovery Call booking)
- Admin dashboard (lead management)

**New Integrations (Phase 1):**
- HubSpot API (create/update deals, contacts)
- Slack API (notifications)
- Email SMTP (follow-up questions if needed)

**New Tools (Phase 2):**
- **Tavily API:** Web search and research ($0.005/search, high-quality results)
- **Perplexity API:** Deep company analysis and summary ($0.01/query)
- **Clearbit or Hunter.io:** Email finding and company enrichment ($0.10-0.50/lookup)
- **LinkedIn scraper:** Decision-maker identification (custom built or Apify actor $20-50/month)
- **Google Maps API:** Local business discovery for SME targeting

**Data Storage:**
- Supabase (already in use): Lead data, qualification history, prospect research results
- HubSpot: CRM records, deals, contacts
- Pinecone: Vector embeddings of past leads for similarity scoring

### Justification Summary

| Technology | Why This Choice | What It Replaces |
|------------|----------------|------------------|
| Claude 3.5 Sonnet | Best reasoning for scoring logic, multilingual | Manual qualification decisions |
| LangGraph | Complex multi-step research workflows | Manual web research process |
| n8n | Visual workflow, HubSpot integration | Manual data entry to HubSpot |
| Tavily | Better than raw Google for business research | Manual Google searches |
| Pinecone | Fast similarity search for lead scoring | No historical comparison capability |

---

## 3. MVP Scope Definition

### Phase 1: Inbound Lead Qualification (Lab MVP)

**Must-Have Features:**
1. ✅ Webhook trigger when website form submitted
2. ✅ Extract and validate form data (name, email, company, industry, budget, timeline, needs)
3. ✅ LLM-based qualification scoring (0-100 fit score)
4. ✅ Auto-create/update HubSpot deal with correct pipeline stage
5. ✅ Slack notification to Lucas with qualification summary
6. ✅ Support German and Spanish submissions

**Qualification Logic (Fit Score Components):**
- Industry match (40%): Wellness/Fitness = 100, Aesthetics = 95, Medical = 95, Beauty = 90, Real Estate = 85, Other service businesses = 70, Non-service = 50
- Budget alignment (25%): €5K-50K+ monthly = high, <€5K = low
- Timeline urgency (20%): "Immediately" or "1-3 months" = high, "6+ months" = low
- Needs clarity (15%): Specific AI use case mentioned = high, vague = medium

**Pipeline Routing:**
- Score 70-100: HubSpot stage = "Outreach Sent" (high priority)
- Score 40-69: HubSpot stage = "Lead" (medium priority)
- Score 0-39: HubSpot stage = "Lead" + tag "Low Fit - Nurture"

**Success Metrics (Phase 1):**
- 95%+ of form submissions processed within 2 minutes
- Qualification accuracy: 80%+ agreement with Lucas's manual assessment (validated on first 20 leads)
- Zero data loss (all form submissions reach HubSpot)

**Out of Scope (Phase 1):**
- ❌ Outbound prospecting
- ❌ Multi-dimensional scoring (only fit score)
- ❌ Automated email follow-up questions
- ❌ Decision-maker research
- ❌ Message drafting
- ❌ Integration with Calendly (manual booking still)

---

### Phase 2: Outbound Prospecting & Research (Post-Lab)

**New Features:**
1. ✅ Web-based prospect discovery (search for SMEs in target industries/locations)
2. ✅ Comprehensive lead research with all fields:
   - Company snapshot (name, website, industry, location, size, revenue, business model)
   - Lead quality scores (fit, AI opportunity, urgency, budget likelihood, contactability)
   - Relevance analysis (why this lead matters, pain point hypotheses)
   - AI use case suggestions
   - Trigger events (hiring, funding, expansion, etc.)
   - Decision-maker contacts (name, role, LinkedIn, email, confidence)
   - Personalized outreach angle
   - Suggested first message draft
   - Objection handling notes
   - Buying readiness assessment
   - Recommended next action
3. ✅ Auto-populate HubSpot with researched prospects
4. ✅ Weekly batch prospecting runs (configurable)

**Research Workflow (LangGraph State Machine):**
```
Start → Search Web → Extract Companies → Research Each Company → 
Score & Analyze → Find Decision Makers → Draft Message → 
Validate Quality → Store in HubSpot → Notify Lucas
```

**Comprehensive Lead Summary Structure:**
```markdown
# Lead Summary: [Company Name]

## Priority
- Overall score: 82/100
- Lead priority: High
- Buying readiness: Warm
- Main reason to contact: Strong operational complexity, recent hiring

## Company Snapshot
- Website: example.com
- Industry: Logistics
- Location: Berlin, Germany
- Employee range: 80-120
- Revenue estimate: €5-10M
- Business model: B2B freight and warehouse services
- Main services: Regional freight, warehouse coordination, B2B delivery

## Why This Lead Fits
[AI-generated explanation of fit with Kairos ICP]

## Likely Pain Points
- Manual customer support
- Slow proposal creation
- Fragmented CRM data

## Suggested AI Opportunities
- Primary offer: AI Readiness Assessment
- Secondary offer: CRM and customer inquiry automation
- Possible pilot: Internal operations assistant

## Trigger Events
- Recent hiring: Operations Manager (process optimization role)
- Expansion: None detected
- Digitalization signals: Website mentions "digital transformation"

## Best Contacts
| Name | Role | Relevance | Contact Source | Confidence |
|------|------|-----------|----------------|------------|
| Anna Schneider | COO | Process automation owner | LinkedIn | High |

## Outreach Angle
[Personalized hook based on company research]

## Suggested First Message
[AI-drafted LinkedIn/email message]

## Objections to Expect
- "AI is too expensive" → Start with small assessment
- "We don't have clean data" → Begin with process mapping

## Recommended Next Action
Send LinkedIn message to COO using operations automation angle

## Sources and Confidence
- Sources: Company website, LinkedIn, job posting
- Confidence: Medium-high
- Limitations: Revenue is estimated
```

**Success Metrics (Phase 2):**
- 20+ qualified prospects researched per week
- 80%+ accuracy on company data (validated by spot-checking)
- 60%+ of researched leads move to outreach stage
- 30% reduction in research time per prospect

**Out of Scope (Phase 2):**
- ❌ Automated sending of outreach messages (manual approval required)
- ❌ Full CRM enrichment of existing contacts
- ❌ Real-time trigger monitoring (weekly batch only)

---

### Phase 3: Advanced Automation & Optimization (Future)

**New Features:**
1. ✅ Five-dimensional lead scoring:
   - Fit score (ICP alignment)
   - AI opportunity score (potential project value)
   - Urgency score (timing/triggers)
   - Budget likelihood score (ability to pay)
   - Contactability score (ease of reaching decision-makers)
2. ✅ Real-time trigger event monitoring (daily checks for hiring, funding, news)
3. ✅ A/B testing of message templates with performance tracking
4. ✅ Automated follow-up sequences (with approval gates)
5. ✅ Integration with Calendly for auto-booking suggestions
6. ✅ Lead enrichment from CRM history and past interactions
7. ✅ RAG system using past successful deals to improve scoring

**Success Metrics (Phase 3):**
- 50%+ reduction in time from lead identification to first outreach
- 25%+ improvement in outreach response rates
- 90%+ scoring accuracy vs manual assessment

---

## 4. Risk Assessment & Mitigation

### Technical Risks

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **High API costs from excessive LLM calls** | Medium | High | - Implement aggressive caching for similar leads<br>- Use cheaper models for simple tasks (GPT-3.5 for extraction)<br>- Set up cost monitoring alerts at €100/month threshold<br>- Batch process outbound research (weekly, not daily) |
| **LLM hallucination on company research** | High | Medium | - Cross-validate data from multiple sources<br>- Show confidence scores to user<br>- Require manual approval before sending messages<br>- Build validation layer to check URLs, emails exist |
| **HubSpot API rate limits** | Low | Medium | - Implement request queuing and retry logic<br>- Batch create deals (max 10/minute)<br>- Use HubSpot webhook for updates instead of polling |
| **Web scraping blocks/failures** | Medium | Medium | - Use multiple data sources (Tavily, Perplexity, direct scraping)<br>- Implement exponential backoff and retries<br>- Respect robots.txt and rate limits<br>- Consider rotating proxy service if needed |
| **Integration failures with existing systems** | Low | High | - Build comprehensive error handling and logging<br>- Set up dead letter queue for failed webhooks<br>- Test with duplicate Supabase/HubSpot sandbox first<br>- Maintain manual fallback process |

### Business Risks

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **Poor lead scoring accuracy** | Medium | High | - Start with human-in-the-loop (manual approval required)<br>- Track scoring accuracy metrics weekly<br>- Retrain/adjust scoring logic based on feedback<br>- Keep manual override option in dashboard |
| **Low adoption by Lucas/team** | Low | Medium | - Design simple dashboard for reviewing agent decisions<br>- Send daily summary reports, not individual notifications<br>- Build manual override for every automated action<br>- Gather feedback after first 20 leads processed |
| **Scope creep into full sales automation** | High | Medium | - Strict phase boundaries with approval gates<br>- Phase 1 deliverable locked before starting Phase 2<br>- Document "out of scope" explicitly for each phase<br>- Set budget caps per phase |
| **Cost overruns from underestimated API usage** | Medium | High | - Start with €200/month budget, monitor weekly<br>- Set hard API limit at €300/month (kill switch)<br>- Optimize prompts to reduce token usage<br>- Consider self-hosting some components if costs exceed budget |

### Data & Compliance Risks

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **GDPR violations from web scraping personal data** | Medium | High | - Only collect publicly available business contact info<br>- Implement data retention policies (delete after 90 days if no engagement)<br>- Add opt-out mechanism in outreach messages<br>- Consult legal before launching Phase 2 prospecting<br>- Document data sources and collection methods |
| **Poor quality prospect data** | Medium | Medium | - Set minimum confidence thresholds (70%+ required)<br>- Show data sources and confidence scores to user<br>- Manual verification step before outreach<br>- Build feedback loop to improve data quality |
| **Inaccurate company information** | Medium | Low | - Use multiple data sources for validation<br>- Show "last updated" timestamps<br>- Allow manual corrections in dashboard<br>- Prioritize recent/fresh data sources |
| **Email deliverability issues from automation** | Low | Medium | - Use Lucas's actual email (not generic/automated sender)<br>- Warm up sending gradually (5→10→20 per week)<br>- Personalize every message (no bulk templates)<br>- Monitor bounce rates and spam complaints |

### Operational Risks

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **Agent requires constant babysitting** | Medium | Medium | - Set up daily automated health checks<br>- Build self-healing for common errors<br>- Clear escalation path when agent fails<br>- Weekly review of agent performance metrics |
| **Breakdown in communication with prospects** | Low | High | - All messages require manual approval before sending<br>- Build "pause" mechanism for agent decisions<br>- Maintain manual outreach process as backup<br>- Monitor response rates and sentiment |
| **Dependency on external APIs (single point of failure)** | Medium | Medium | - Build fallback data sources (Tavily fails → use Perplexity)<br>- Cache research results for 30 days<br>- Document manual research process<br>- Consider backing up to local storage |

---

## 5. Implementation Plan

### Phase 1: Inbound Lead Qualification (Lab MVP)
**Timeline:** 3-5 days  
**Effort:** 10-15 hours  
**Status:** Lab deliverable (minimal prototype)

#### Step 1.1: Environment Setup (Day 1)
- [ ] Set up n8n instance (self-hosted or n8n Cloud)
- [ ] Configure Anthropic API key
- [ ] Set up HubSpot API credentials and test connection
- [ ] Create Slack webhook for notifications
- [ ] Set up development Supabase database (copy of production schema)

#### Step 1.2: Webhook & Data Flow (Day 1-2)
- [ ] Create n8n webhook endpoint for form submissions
- [ ] Update website form to send POST request to n8n webhook
- [ ] Build data extraction and validation node
- [ ] Test webhook with sample form data

#### Step 1.3: Qualification Agent (Day 2-3)
- [ ] Design qualification prompt with scoring rubric
- [ ] Build LangChain agent with Claude 3.5 Sonnet
- [ ] Implement fit score calculation logic
- [ ] Add German/Spanish language detection
- [ ] Test with 10 sample leads (mix of high/medium/low quality)

#### Step 1.4: HubSpot Integration (Day 3)
- [ ] Build deal creation node in n8n
- [ ] Map form fields to HubSpot contact/deal properties
- [ ] Implement pipeline stage routing logic (score → stage)
- [ ] Add error handling for duplicate contacts
- [ ] Test end-to-end flow with sandbox HubSpot

#### Step 1.5: Notifications & Monitoring (Day 4)
- [ ] Create Slack message template with qualification summary
- [ ] Build notification node in n8n
- [ ] Set up error alerts (webhook failures, API errors)
- [ ] Create simple dashboard for reviewing agent decisions

#### Step 1.6: Testing & Documentation (Day 5)
- [ ] Test with 5 real form submissions (Lucas submits test leads)
- [ ] Validate qualification accuracy vs manual assessment
- [ ] Document workflow in n8n with comments
- [ ] Write runbook for troubleshooting common issues
- [ ] Create README for future team members

**Deliverables:**
- Working n8n workflow (exportable JSON)
- Qualification prompt and scoring logic documentation
- 5 test case results with accuracy validation
- Runbook and setup instructions

**Success Criteria:**
- ✅ 5/5 test leads processed successfully
- ✅ <2 minute processing time per lead
- ✅ 80%+ scoring accuracy vs Lucas's manual assessment
- ✅ Zero data loss (all submissions in HubSpot)

---

### Phase 2: Outbound Prospecting & Research (Post-Lab)
**Timeline:** 2-3 weeks  
**Effort:** 40-60 hours  
**Status:** Real implementation after lab submission

#### Step 2.1: Research Tool Setup (Week 1)
- [ ] Sign up for Tavily API (research tier)
- [ ] Set up Perplexity API for company analysis
- [ ] Configure Hunter.io or Clearbit for email finding
- [ ] Test each API with sample company queries
- [ ] Build cost monitoring for all APIs

#### Step 2.2: Prospect Discovery (Week 1)
- [ ] Design search queries for target industries (education, SMEs in Berlin)
- [ ] Build web scraper for local business directories
- [ ] Integrate Google Maps API for SME discovery
- [ ] Create deduplication logic (avoid researching same company twice)
- [ ] Test discovery with 20 sample companies

#### Step 2.3: LangGraph Research Workflow (Week 1-2)
- [ ] Design state machine for research workflow
- [ ] Build company data extraction node (website, industry, size, etc.)
- [ ] Implement pain point hypothesis generation
- [ ] Create AI use case suggestion logic
- [ ] Build trigger event detection (job posts, funding news)
- [ ] Add decision-maker identification
- [ ] Test workflow with 10 companies

#### Step 2.4: Lead Scoring & Analysis (Week 2)
- [ ] Implement fit score calculation (ICP alignment)
- [ ] Build AI opportunity score (potential project value estimation)
- [ ] Create urgency score (trigger-based timing)
- [ ] Add budget likelihood score (company size/revenue based)
- [ ] Implement contactability score (LinkedIn presence, email findability)
- [ ] Test scoring with 20 companies, validate accuracy

#### Step 2.5: Message Drafting & Personalization (Week 2)
- [ ] Design outreach message templates (LinkedIn, email)
- [ ] Build personalization logic (company-specific hooks)
- [ ] Create objection handling library
- [ ] Generate buying readiness assessment
- [ ] Test message quality with Lucas's feedback

#### Step 2.6: Integration & Automation (Week 3)
- [ ] Build Supabase tables for storing prospect research
- [ ] Create HubSpot deal creation for researched prospects
- [ ] Set up weekly batch prospecting scheduler (n8n cron)
- [ ] Build approval dashboard for reviewing prospects before outreach
- [ ] Implement email notifications with prospect summaries

#### Step 2.7: Testing & Refinement (Week 3)
- [ ] Run first batch: research 20 prospects
- [ ] Validate data accuracy (spot-check 5 companies manually)
- [ ] Gather Lucas's feedback on lead quality
- [ ] Adjust scoring weights based on real results
- [ ] Optimize prompts to reduce API costs
- [ ] Document research workflow and data sources

**Deliverables:**
- LangGraph workflow for prospect research
- Comprehensive lead summary template
- 20+ researched prospects in HubSpot
- Cost analysis report (actual API spending)
- Updated documentation

**Success Criteria:**
- ✅ 20+ prospects researched per week
- ✅ 80%+ data accuracy on spot-checks
- ✅ €200-300/month API costs (within budget)
- ✅ 60%+ of prospects approved for outreach by Lucas

---

### Phase 3: Advanced Automation (Future)
**Timeline:** 4-6 weeks  
**Effort:** 80-120 hours  
**Status:** Future roadmap

#### High-Level Milestones:
1. **Multi-dimensional scoring system** (Week 1-2)
   - Five-score dashboard (fit, opportunity, urgency, budget, contactability)
   - Weighted composite score for prioritization
   - Score visualization in HubSpot custom properties

2. **Real-time trigger monitoring** (Week 2-3)
   - Daily checks for hiring activity (LinkedIn, job boards)
   - Funding news alerts (Crunchbase, TechCrunch)
   - Company expansion signals (new locations, product launches)
   - Automated notifications for high-urgency triggers

3. **Message optimization & A/B testing** (Week 3-4)
   - Track response rates by message template
   - A/B test different personalization strategies
   - Build message performance dashboard
   - Auto-optimize templates based on data

4. **Automated follow-up sequences** (Week 4-5)
   - Build 3-touch follow-up workflow (Day 3, Day 7, Day 14)
   - Integrate with HubSpot sequences
   - Manual approval gates for each send
   - Response detection and auto-pause

5. **RAG system for lead intelligence** (Week 5-6)
   - Vectorize past successful deals (Pinecone)
   - Build similarity search for new leads
   - "Leads similar to this one closed at €X" insights
   - Improve scoring based on historical patterns

**Success Criteria:**
- ✅ 50%+ time reduction from lead ID to outreach
- ✅ 25%+ improvement in response rates
- ✅ 90%+ scoring accuracy
- ✅ Fully autonomous weekly prospecting (minimal manual review)

---

## 6. Success Metrics & KPIs

### Phase 1 Metrics (Inbound Qualification)

**Operational Metrics:**
- Processing time: <2 minutes per lead (target: <1 minute)
- Uptime: 99%+ (allow for occasional webhook failures)
- Data completeness: 100% (all form fields captured in HubSpot)

**Quality Metrics:**
- Scoring accuracy: 80%+ agreement with Lucas's manual assessment
- False positives (high score, but low quality): <10%
- False negatives (low score, but high quality): <5%

**Business Impact:**
- Time saved: 15 minutes per lead × 20 leads/month = 5 hours/month
- Faster response time: Outreach within 4 hours vs 24-48 hours manually
- Higher conversion: 20%+ improvement (faster response = better conversion)

**How to Measure:**
- Weekly review: Lucas reviews 5 random leads, compares agent score vs his judgment
- Monthly analysis: Track conversion rates by score tier (70-100, 40-69, 0-39)
- Dashboard: Real-time processing time and error rate monitoring

---

### Phase 2 Metrics (Outbound Prospecting)

**Operational Metrics:**
- Prospects researched per week: 20+ (target: 30+)
- Research time per prospect: <10 minutes (vs 45-90 minutes manually)
- API cost per prospect: <€4 (target: <€3)

**Quality Metrics:**
- Data accuracy: 80%+ (validated by manual spot-checks)
- Lead quality (approved for outreach): 60%+ (target: 75%+)
- Contact findability: 70%+ prospects have decision-maker identified

**Business Impact:**
- Time saved: 60 minutes per prospect × 20 prospects/week = 20 hours/week
- Pipeline growth: 80+ new qualified prospects/month in HubSpot
- Outreach volume: 3x increase (more prospects = more outreach)

**How to Measure:**
- Weekly spot-check: Manually validate 5 researched prospects
- Monthly review: Track % of prospects that convert to meetings
- Cost tracking: Monitor API spending per prospect, optimize if >€4

---

### Phase 3 Metrics (Advanced Automation)

**Operational Metrics:**
- Real-time trigger detection: <24 hours from event to notification
- Message send volume: 50+ personalized messages/week
- Follow-up sequence completion: 80%+ (20% stop due to responses)

**Quality Metrics:**
- Outreach response rate: 15%+ (industry avg is 8-12%)
- Meeting booking rate: 5%+ of outreach converts to meetings
- Message personalization quality: 90%+ perceived as human-written

**Business Impact:**
- Pipeline velocity: 50%+ faster from lead ID to first meeting
- Sales efficiency: 30%+ more meetings booked per hour of sales time
- Revenue impact: 2x qualified pipeline in HubSpot

**How to Measure:**
- A/B test tracking: Compare response rates across message variants
- HubSpot analytics: Track deals created, meetings booked, revenue attributed
- Quarterly review: Full ROI analysis (cost vs revenue from agent-sourced deals)

---

## 7. Resource Requirements

### Team & Roles

**Phase 1 (Lab MVP):**
- Lucas Barrios: Product owner, testing, validation (5 hours)
- No additional team needed

**Phase 2 (Real Implementation):**
- Lucas Barrios: Product owner, prompt engineering, testing (15 hours)
- Developer (can be Lucas): LangGraph implementation, API integrations (40-60 hours)
- Optional: Freelance developer if Lucas focuses on consulting (€2,000-3,000)

**Phase 3 (Advanced):**
- Same as Phase 2 + ongoing maintenance (10 hours/month)

---

### Tools & Services Budget

**Phase 1:**
| Service | Cost | Notes |
|---------|------|-------|
| Anthropic API | €50-100/month | ~50-100 leads/month |
| n8n Cloud (Starter) | €20/month | Or self-host for free |
| Slack | Free | Existing workspace |
| **Total Phase 1** | **€70-120/month** | |

**Phase 2:**
| Service | Cost | Notes |
|---------|------|-------|
| Anthropic API | €150-200/month | 20 prospects/week × €3/prospect |
| Tavily API | €50/month | Research tier |
| Perplexity API | €20/month | Company analysis |
| Hunter.io | €49/month | Email finding (500 searches) |
| Pinecone | €70/month | Starter tier (vector DB) |
| n8n Cloud (Pro) | €50/month | More workflows needed |
| **Total Phase 2** | **€389-439/month** | |

**Phase 3:**
| Service | Cost | Notes |
|---------|------|-------|
| All Phase 2 costs | €389-439/month | |
| LinkedIn Sales Nav | €80/month | Decision-maker research |
| Apify (scraping) | €49/month | Backup data source |
| **Total Phase 3** | **€518-568/month** | |

**One-Time Costs:**
- Development time (if outsourced): €2,000-5,000 for Phase 2
- None if Lucas builds it himself

---

### Infrastructure

**Phase 1:**
- n8n instance (cloud or self-hosted on existing server)
- Existing Supabase database (no additional cost)
- Existing HubSpot account (no additional cost)

**Phase 2+:**
- Pinecone vector database (cloud hosted)
- Increased Supabase storage (still within free tier likely)
- Optional: Dedicated server for n8n if self-hosting (€10-20/month)

---

## 8. Next Steps & Action Items

### Immediate (Lab Submission - Next 2 Days)
1. ✅ Review and approve this project plan
2. ✅ Set up n8n instance and test webhook
3. ✅ Build minimal Phase 1 prototype (inbound qualification only)
4. ✅ Test with 3-5 sample form submissions
5. ✅ Document workflow and create lab_summary.md
6. ✅ Submit lab to Ironhack with GitHub repo

### Short-Term (Week 1-2 Post-Lab)
1. ⏳ Finalize Phase 1 production deployment
2. ⏳ Monitor first 20 real leads, validate scoring accuracy
3. ⏳ Gather feedback from Lucas on qualification quality
4. ⏳ Adjust scoring weights based on real data
5. ⏳ Decision point: Proceed to Phase 2 or optimize Phase 1?

### Medium-Term (Month 1-2)
1. ⏳ Begin Phase 2 implementation (outbound prospecting)
2. ⏳ Set up API accounts (Tavily, Perplexity, Hunter)
3. ⏳ Build LangGraph research workflow
4. ⏳ Test with first batch of 20 prospects
5. ⏳ Measure ROI: time saved, lead quality, API costs

### Long-Term (Month 3-6)
1. ⏳ Phase 3 planning and design
2. ⏳ Consider hiring developer if Lucas is consulting full-time
3. ⏳ Scale to 50+ prospects/week if Phase 2 successful
4. ⏳ Build training dataset from successful deals for RAG system
5. ⏳ Explore additional markets (Spain, Latin America)

---

## 9. Risk Mitigation Summary

**Top 3 Risks to Watch:**

1. **API Cost Overruns**
   - Monitor weekly, set hard caps at €300/month
   - Optimize prompts, use caching aggressively
   - Kill switch if costs exceed budget

2. **Poor Lead Scoring Accuracy**
   - Human-in-the-loop for first 50 leads
   - Weekly validation against Lucas's judgment
   - Continuous prompt refinement based on feedback

3. **GDPR Compliance on Web Scraping**
   - Legal review before Phase 2 launch
   - Only collect public business data
   - Clear data retention and opt-out policies

---

## 10. Conclusion & Vision

This autonomous agent system transforms Kairos Consulting's sales process from reactive and manual to proactive and automated. 

**Phase 1** solves the immediate pain of manual inbound lead qualification, saving 5+ hours/month and enabling faster response times.

**Phase 2** unlocks outbound growth by systematically researching 80+ qualified prospects/month, creating a predictable pipeline.

**Phase 3** optimizes the entire process with real-time triggers, A/B tested messaging, and historical intelligence.

**The ultimate vision:** Lucas focuses on high-value consulting and closing deals, while the agent handles lead discovery, qualification, research, and initial outreach. The agent becomes Kairos's "AI SDR" - working 24/7 to fill the pipeline with qualified, well-researched prospects.

**ROI Projection (6 months post-Phase 3):**
- Time saved: 100+ hours/month (€5,000+ value at €50/hour consulting rate)
- Pipeline growth: 200+ qualified prospects added to HubSpot
- Revenue impact: 10+ new clients from agent-sourced leads = €50,000-150,000 ARR
- Total cost: €3,000 (6 months × €500/month) + development time
- **ROI: 15-50x** (conservative estimate)

This lab is not just an academic exercise - it's the blueprint for building Kairos's automated sales engine.

---

**Prepared by:** Lucas Barrios  
**For:** Ironhack AI Manager/AI Consulting Program  
**Date:** May 18, 2026  
**Version:** 1.0
