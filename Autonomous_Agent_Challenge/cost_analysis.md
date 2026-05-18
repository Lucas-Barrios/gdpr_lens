# Cost Analysis & Budget Projection
## Kairos Consulting Lead Generation System

**Created:** May 18, 2026  
**For:** Ironhack Lab Extension Activities  

---

## Executive Summary

**Phase 1 Monthly Cost:** €70-120  
**Phase 2 Monthly Cost:** €389-439  
**Phase 3 Monthly Cost:** €518-568  

**ROI Breakeven:** Month 2 (Phase 1), Month 1 (Phase 2)  
**12-Month Total Cost:** €4,680-5,520  
**12-Month Value Generated:** €60,000-180,000 (pipeline attributed to agent)  

---

## Phase 1: Inbound Lead Qualification

### API Cost Breakdown

**Anthropic Claude 3.5 Sonnet:**
- Pricing: $3/million input tokens, $15/million output tokens
- Per-lead usage:
  - Input: ~2,000 tokens (form data + system prompt + scoring rubric)
  - Output: ~800 tokens (score + reasoning + HubSpot data structure)
  - Cost per lead: ~$0.018 (€0.017)
- Monthly volume: 50-100 leads
- **Monthly Anthropic cost: €0.85-1.70**

**n8n Cloud (Starter Plan):**
- 2,500 workflow executions/month included
- Per-lead execution: 1 workflow run
- Monthly leads: 50-100 = well within free tier
- **Monthly n8n cost: €20** (starter tier, could self-host for €0)

**HubSpot API:**
- Free tier: 250,000 API calls/month
- Per-lead calls: 2 (create contact, create deal)
- Monthly calls: 100-200 = free
- **Monthly HubSpot cost: €0**

**Slack API:**
- Free tier: unlimited webhooks
- **Monthly Slack cost: €0**

**Total Phase 1 Infrastructure:**
- Anthropic API: €0.85-1.70
- n8n: €20 (or €0 self-hosted)
- HubSpot: €0
- Slack: €0
- **Total: €20.85-21.70 (€0.85-1.70 if self-hosting n8n)**

### Hidden Costs

**Development Time:**
- Lucas builds it himself: 10-15 hours @ €0 (learning investment)
- Freelancer: 10-15 hours @ €80/hour = €800-1,200 one-time

**Supabase:**
- Current usage: Free tier
- Additional storage for lead history: negligible (<100MB/year)
- **Monthly Supabase cost: €0**

**Calendly:**
- Existing subscription: €12/month (sunk cost, no additional cost)

**Monitoring/Debugging:**
- n8n built-in logging: free
- Estimated time: 30 min/month
- **Cost: €0 (Lucas's time)**

### Total Phase 1 Monthly Cost

**Conservative (self-host n8n):** €0.85-1.70  
**Standard (n8n Cloud):** €20.85-21.70  
**With development (one-time):** +€800-1,200  

**Recommended budget:** €70-120/month (includes 3x buffer for unexpected API spikes)

---

## Phase 2: Outbound Prospecting

### API Cost Breakdown

**Anthropic Claude 3.5 Sonnet (expanded usage):**
- Per-prospect research workflow:
  - Company analysis: ~4,000 input + ~1,200 output tokens
  - Pain point generation: ~3,000 input + ~800 output tokens
  - Use case suggestions: ~2,500 input + ~600 output tokens
  - Message drafting: ~2,000 input + ~400 output tokens
  - Total per prospect: ~11,500 input, ~3,000 output
  - Cost per prospect: ~$0.08 (€0.075)
- Monthly volume: 20 prospects/week × 4 weeks = 80 prospects
- **Monthly Anthropic cost: €6.00**

**Tavily Research API:**
- Pricing: $0.005/search (research tier)
- Per-prospect searches:
  - Company discovery: 3 searches
  - Competitor research: 2 searches
  - Trigger event detection: 2 searches
  - Total: 7 searches × €0.0047 = €0.033/prospect
- Monthly: 80 prospects × €0.033 = €2.64
- **Monthly Tavily cost: €2.64**
- **Alternative: Perplexity bulk searches - €25/month for unlimited (cost-effective at >700 searches)**

**Perplexity API:**
- Pricing: $5/month for 200 requests (Pro tier)
- Per-prospect: 1 deep company analysis query
- Monthly: 80 prospects = 80 requests
- **Monthly Perplexity cost: €5** (~€4.70)

**Hunter.io (Email Finder):**
- Pricing: €49/month for 500 searches
- Per-prospect: 1-2 email lookups (decision-maker contact)
- Monthly: 80-160 lookups = within tier
- **Monthly Hunter cost: €49**
- **Alternative: Free tools (Apollo.io 50/month free) + manual lookup = €0-20/month**

**Pinecone Vector Database:**
- Pricing: $70/month (Starter: 10GB storage, 100K queries)
- Use case: Store embeddings of past successful leads for similarity scoring
- Storage: ~5,000 leads × 1.5KB embedding = 7.5MB
- Queries: 80 similarity searches/month
- **Monthly Pinecone cost: €70** (~€66)
- **Alternative: Chroma self-hosted = €0** (no managed service, higher dev time)

**n8n Pro Plan:**
- Pricing: $50/month (25,000 executions)
- Weekly prospecting batches: 4 runs × ~1,000 steps each = 4,000 executions/month
- **Monthly n8n cost: €50** (~€47)

**Google Maps API (optional - for local SME discovery):**
- Pricing: $0.017/request (Places API)
- Monthly: 50 local business searches
- **Monthly Maps cost: €0.80**

### Total Phase 2 Infrastructure

- Anthropic API: €6.00
- Tavily API: €2.64
- Perplexity API: €4.70
- Hunter.io: €49.00
- Pinecone: €66.00
- n8n Pro: €47.00
- Google Maps: €0.80
- **Total: €176.14/month**

### Hidden Costs

**Development Time:**
- Lucas builds: 40-60 hours @ €0
- Freelancer: 40-60 hours @ €80/hour = €3,200-4,800 one-time

**LangGraph Development:**
- Additional Python libraries: €0
- Testing/debugging time: 10 hours/month initially
- **Cost: €0 (Lucas's time)**

**Data Quality Monitoring:**
- Manual spot-checks: 2 hours/month
- **Cost: €0 (Lucas's time)**

### Cost Optimization Opportunities

**Option 1: Use Free Tiers Aggressively**
- Hunter.io → Apollo.io free tier (50/month) + LinkedIn scraping = save €49/month
- Pinecone → Chroma self-hosted = save €66/month
- Perplexity → Use only Tavily with better prompts = save €4.70/month
- **Savings: €119.70/month**
- **New total: €56.44/month**

**Option 2: Batch Processing**
- Run prospecting monthly instead of weekly
- Reduce Anthropic calls by caching company research for 30 days
- **Savings: ~30% on API costs = €53/month**
- **New total: €123/month**

**Option 3: Hybrid Manual/Auto**
- Agent finds prospects (cheap Tavily searches)
- Lucas manually validates top 20 before deep research
- Only run deep research on validated prospects
- **Savings: 60% on deep research APIs = €71/month**
- **New total: €105/month**

### Recommended Phase 2 Budget

**Aggressive (all optimizations):** €56-80/month  
**Standard (Hunter + Pinecone):** €176-200/month  
**Conservative (3x buffer):** €389-439/month ← **RECOMMENDED**

---

## Phase 3: Advanced Automation

### Additional Costs vs Phase 2

**LinkedIn Sales Navigator:**
- Pricing: €80/month (Professional tier)
- Use case: Decision-maker research, trigger monitoring
- **Monthly LinkedIn cost: €80**

**Apify (Backup Web Scraping):**
- Pricing: €49/month (Starter: 100 actor runs)
- Use case: Scrape LinkedIn, job boards when APIs fail
- **Monthly Apify cost: €49**

**Increased Anthropic Usage (A/B Testing):**
- 2x message variants per prospect = 2x generation calls
- Additional scoring refinement passes
- **Increased Anthropic cost: +€6/month**

**Increased Pinecone (RAG System):**
- Storing 20K+ past deal embeddings
- More frequent similarity queries (500/month vs 80/month)
- **Increased Pinecone cost: +€0** (still within starter tier)

### Total Phase 3 Infrastructure

- Phase 2 costs: €176.14/month
- LinkedIn Sales Nav: €80/month
- Apify: €49/month
- Additional Anthropic: €6/month
- **Total: €311.14/month**

### Recommended Phase 3 Budget

**Standard:** €311-350/month  
**Conservative (2x buffer):** €518-568/month ← **RECOMMENDED**

---

## ROI Analysis

### Phase 1 ROI

**Costs:**
- Monthly: €70-120
- One-time dev: €0 (Lucas builds)
- 12-month total: €840-1,440

**Value Generated:**
- Time saved: 15 min/lead × 50 leads/month = 12.5 hours/month
- Lucas's hourly rate (consulting): €100/hour
- Monthly value: 12.5 × €100 = €1,250
- 12-month value: €15,000

**ROI: 10-18x**  
**Breakeven: Month 1**

### Phase 2 ROI

**Costs:**
- Monthly: €389-439
- One-time dev: €0 (Lucas builds)
- 12-month total: €4,668-5,268

**Value Generated:**
- Time saved: 60 min/prospect × 80 prospects/month = 80 hours/month
- Monthly value: 80 × €100 = €8,000
- 12-month value: €96,000

**Additional Pipeline:**
- 80 prospects/month × 12 months = 960 researched prospects
- Conversion to meeting: 5% = 48 meetings
- Meeting to client: 20% = 9.6 clients (~10 new clients)
- Average deal size: €15,000
- Revenue attributed to agent: €150,000

**Total 12-month value: €96,000 (time) + €150,000 (revenue) = €246,000**

**ROI: 47-53x**  
**Breakeven: Month 1**

### Phase 3 ROI

**Costs:**
- Monthly: €518-568
- 12-month total: €6,216-6,816

**Value Generated:**
- Additional time saved (automation): 20 hours/month
- Monthly value: 20 × €100 = €2,000
- 12-month value: €24,000

**Improved Conversion:**
- Better message personalization: +10% meeting booking rate
- +10% of 80 prospects/month = 8 extra meetings/month × 12 = 96 meetings
- Meetings to clients: 20% = 19.2 clients (~19 new clients)
- Average deal size: €15,000
- Additional revenue: €285,000

**Total 12-month incremental value: €24,000 + €285,000 = €309,000**

**Incremental ROI (Phase 3 vs Phase 2): 45-50x**  
**Breakeven: Month 1**

---

## Budget Comparison: Technology Alternatives

### Alternative Stack #1: OpenAI + Custom Scraping

**Changes:**
- Claude → GPT-4o: €0.015/lead (50% cheaper, but weaker reasoning)
- Hunter.io → Custom LinkedIn scraper: €0 (requires Apify €49)
- Pinecone → Chroma self-hosted: €0 (more dev time)

**Phase 2 monthly cost: €88-110**  
**Trade-off:** Lower cost, but lower quality scores and more maintenance

### Alternative Stack #2: All-in on Perplexity

**Changes:**
- Tavily → Perplexity API (unlimited searches at €50/month)
- Claude → Keep (Perplexity can't match reasoning quality)
- Hunter → Apollo free tier (50/month) + manual fallback

**Phase 2 monthly cost: €123-150**  
**Trade-off:** Simpler stack, slightly lower cost, but contact finding limited

### Alternative Stack #3: Hybrid (Recommended for Budget-Conscious)

**Changes:**
- Keep Claude (quality matters for scoring)
- Tavily for discovery, Perplexity for deep analysis
- Apollo.io free tier (50 emails/month) instead of Hunter
- Chroma self-hosted instead of Pinecone
- n8n self-hosted instead of Cloud (if Lucas comfortable with hosting)

**Phase 2 monthly cost: €13-25**  
**Trade-off:** Much lower cost, but more hands-on maintenance required

---

## 12-Month Budget Projection

### Conservative Scenario (all phases, full commercial pricing)

| Month | Phase | Monthly Cost | Cumulative | Notes |
|-------|-------|--------------|------------|-------|
| 1 | 1 | €100 | €100 | Lab MVP, testing |
| 2 | 1 | €100 | €200 | Production, first 20 leads |
| 3 | 1+2 | €489 | €689 | Start Phase 2 development |
| 4 | 2 | €439 | €1,128 | Phase 2 testing |
| 5 | 2 | €439 | €1,567 | First batch prospecting |
| 6 | 2 | €439 | €2,006 | Optimize costs |
| 7 | 2 | €350 | €2,356 | Cost optimizations applied |
| 8 | 2 | €350 | €2,706 | |
| 9 | 2+3 | €568 | €3,274 | Start Phase 3 |
| 10 | 3 | €568 | €3,842 | Phase 3 testing |
| 11 | 3 | €568 | €4,410 | Full automation live |
| 12 | 3 | €568 | €4,978 | |

**Total 12-month cost: €4,978**  
**Total value generated: €270,000** (time + pipeline)  
**Net ROI: 54x**

### Optimized Scenario (hybrid stack, cost optimizations)

| Month | Phase | Monthly Cost | Cumulative | Notes |
|-------|-------|--------------|------------|-------|
| 1-2 | 1 | €25 | €50 | Self-hosted n8n |
| 3-4 | 1+2 | €80 | €210 | Hybrid stack (Apollo + Chroma) |
| 5-12 | 2+3 | €110 | €1,090 | Optimizations applied |

**Total 12-month cost: €1,090**  
**Total value generated: €270,000**  
**Net ROI: 248x**

---

## Cost Control Strategies

### Real-Time Monitoring

**Set up these alerts:**
1. Anthropic API: Alert if daily spend >€5
2. Tavily: Alert if searches >300/day
3. Hunter: Alert when 80% of monthly quota used
4. n8n: Alert if executions >20,000/month

**Dashboard metrics:**
- Cost per qualified lead (Phase 1): Target <€2
- Cost per researched prospect (Phase 2): Target <€5
- Cost per booked meeting: Target <€50
- Cost per closed deal: Target <€500

### Monthly Review Checklist

- [ ] Review API usage vs budget (5 min)
- [ ] Identify and pause expensive workflows (10 min)
- [ ] Optimize prompts to reduce token usage (30 min)
- [ ] Test cheaper alternatives for high-cost APIs (1 hour/quarter)

### Kill Switch Criteria

**Pause Phase 2 if:**
- Monthly cost >€600 for 2 consecutive months
- Cost per researched prospect >€10
- Lead quality score <60% (manual validation)

**Roll back to Phase 1 if:**
- Phase 2 ROI <2x after 3 months
- Too many low-quality prospects (>50% rejected)
- Maintenance time >10 hours/month

---

## Recommended Budget Allocation

**Month 1-2 (Lab + Phase 1):**
- Budget: €150/month
- Focus: Proof of concept, validate scoring

**Month 3-6 (Phase 2 Development + Testing):**
- Budget: €500/month
- Focus: Build, test, optimize

**Month 7-12 (Phase 2 Production + Phase 3):**
- Budget: €400/month (after optimizations)
- Focus: Scale, automate, measure ROI

**Total Year 1 Budget: €4,800**  
**Expected Value: €270,000**  
**Target ROI: 56x**

---

**Prepared by:** Lucas Barrios  
**Last updated:** May 18, 2026  
**Version:** 1.0
