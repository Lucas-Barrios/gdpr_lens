# Kairos Lead Generation System - Prototype
## Phase 1: Inbound Lead Qualification

**Created:** May 18, 2026  
**For:** Ironhack Lab - Autonomous Agent Challenge  
**Author:** Lucas Barrios  

---

## Overview

This prototype implements an AI-powered lead qualification system that automatically scores and routes inbound leads from the Kairos website contact form.

**What it does:**
1. Receives form submissions via webhook
2. Calls Claude 3.5 Sonnet to analyze and score the lead
3. Routes to appropriate HubSpot pipeline stage (70+ = high priority, 40-69 = medium, <40 = low)
4. Sends Slack notification with key insights
5. Stores lead data in Supabase

**Time to complete:** 30-60 minutes for basic setup and testing

---

## Architecture

```
Website Form → n8n Webhook → Python Agent (Claude API) → {
    - HubSpot (create contact + deal)
    - Slack (notification)
    - Supabase (lead history)
}
```

---

## Prerequisites

**Required:**
- Python 3.9+ installed
- Anthropic API key ([get one here](https://console.anthropic.com))
- Basic command line knowledge

**For Full Integration (optional for prototype):**
- n8n account (free tier works)
- HubSpot account with API access
- Slack workspace with webhook
- Supabase project

---

## Quick Start (Local Testing)

### Step 1: Clone and Setup

```bash
# Create project directory
mkdir kairos-lead-gen-prototype
cd kairos-lead-gen-prototype

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install anthropic python-dotenv requests
```

### Step 2: Configure Environment

```bash
# Create .env file
cat > .env << EOF
ANTHROPIC_API_KEY=your_api_key_here
EOF

# For Windows, create .env file manually with:
# ANTHROPIC_API_KEY=your_api_key_here
```

### Step 3: Copy the Files

Save these files to your project directory:
- `lead_qualification_agent.py` (main agent code)
- `test_qualification.py` (test suite)

### Step 4: Run Tests

```bash
# Run the test suite
python test_qualification.py
```

Expected output:
```
==========================================================================
LEAD QUALIFICATION AGENT - TEST SUITE
==========================================================================

Test 1/6: High Priority - Education Sector
Company: TU Berlin - Department of Computer Science
...
✅ PASS
  Overall Score: 92/100 (expected 85-100)
  Recommended Stage: Outreach Sent
  ...

TEST SUMMARY
Total Tests: 6
Passed: 6 ✅
Failed: 0 ❌
Success Rate: 100.0%
```

### Step 5: Test with Custom Lead

```python
from lead_qualification_agent import process_lead_submission

# Your custom lead
my_lead = {
    "full_name": "Maria Schmidt",
    "email": "maria@fitlife-berlin.de",
    "company_name": "FitLife Studios GmbH",
    "industry": "Wellness & Fitness Studios",
    "budget_range": "€10K-€25K",
    "timeline": "1-3 months",
    "needs": "We have 5 fitness studios and need to automate customer inquiries about class schedules and memberships..."
}

# Process it
result = process_lead_submission(my_lead)

# See the results
print(f"Score: {result['qualification']['overall_score']}/100")
print(f"Stage: {result['qualification']['recommended_stage']}")
print(f"Insights: {result['qualification']['key_insights']}")
```

---

## Understanding the Scores

The agent evaluates leads across 4 dimensions:

### 1. Industry Fit (40% weight)
- **Wellness & Fitness Studios = 100**: Gyms, yoga studios, wellness centers
- **Aesthetic Clinics = 95**: Cosmetic procedures, dermatology
- **Private Medical Clinics = 95**: General practice, specialists
- **Beauty Salons = 90**: Hair, nails, spa services
- **Real Estate = 85**: Residential and commercial agencies
- **Other Services = 70**: Hospitality, professional services
- **Retail/E-commerce = 60**: Product-based businesses
- **Manufacturing/Tech = 50**: Lower fit for Kairos services

### 2. Budget Alignment (25% weight)
- **€50K+ = 100**: Large implementation projects
- **€25K-€50K = 90**: Standard engagements
- **€10K-€25K = 75**: Entry-level projects
- **€5K-€10K = 50**: Small pilots
- **<€5K = 25**: Too small for typical engagement

### 3. Timeline Urgency (20% weight)
- **Immediately = 100**: Ready to start now
- **1-3 months = 80**: Clear timeline
- **3-6 months = 60**: Planning phase
- **6+ months = 40**: Long-term interest

### 4. Needs Clarity (15% weight)
- **Specific use case = 100**: "Automate customer support for 5 locations"
- **General challenge = 75**: "Too much manual work in operations"
- **Vague interest = 50**: "Exploring AI options"
- **No clear use case = 25**: "Just learning about AI"

### Routing Logic

**70-100 = High Priority (Outreach Sent stage)**
- Strong fit across all dimensions
- Ready for immediate personalized outreach
- Likely to convert to discovery call

**40-69 = Medium Priority (Lead stage)**
- Some fit but not immediate
- Needs nurturing content
- May convert in 1-3 months

**0-39 = Low Priority (Lead stage + "Low Fit" tag)**
- Poor fit or very early stage
- Add to long-term nurture sequence
- Unlikely to convert in near term

---

## Example Results

### High-Priority Lead
```json
{
  "overall_score": 92,
  "recommended_stage": "Outreach Sent",
  "key_insights": [
    "Multi-location fitness business with clear automation opportunity across 5 studios",
    "Immediate timeline suggests budget allocated and decision urgency",
    "Specific pain point (customer service) with measurable impact on staff time"
  ],
  "suggested_next_action": "Send personalized email about customer service chatbot case studies in fitness industry, emphasize time savings for front desk staff",
  "suggested_use_case": "AI chatbot for class schedules, membership inquiries, and trainer availability - integrates with existing booking system"
}
```

### Medium-Priority Lead
```json
{
  "overall_score": 68,
  "recommended_stage": "Lead",
  "key_insights": [
    "Real estate agency with clear lead qualification need but longer timeline (3-6 months)",
    "Still in research phase, not ready for immediate engagement",
    "Budget range suggests serious interest but needs education on AI value proposition"
  ],
  "suggested_next_action": "Add to nurture sequence with real estate AI automation case studies and ROI calculator",
  "suggested_use_case": "AI-powered lead qualification and property matching system"
}
```

---

## Integration with n8n (Optional)

### n8n Workflow Structure

```
1. Webhook Trigger
   ↓
2. Python Script Node (run lead_qualification_agent.py)
   ↓
3. Split into 3 parallel branches:
   ├── HubSpot: Create Contact
   ├── HubSpot: Create Deal
   └── Slack: Send Notification
   ↓
4. Supabase: Log to database
```

### Setting up n8n

1. **Create n8n account** at https://n8n.io (free tier)

2. **Import workflow:**
   - Create new workflow
   - Add Webhook node
   - Add Code node with Python qualification logic
   - Add HubSpot nodes (contact + deal)
   - Add Slack webhook node
   - Connect nodes

3. **Configure credentials:**
   - Anthropic API key
   - HubSpot API key
   - Slack webhook URL
   - Supabase connection string

4. **Test workflow:**
   ```bash
   curl -X POST https://your-n8n-instance.app.n8n.cloud/webhook/lead-intake \
     -H "Content-Type: application/json" \
     -d @test_lead.json
   ```

---

## Deployment Options

### Option 1: n8n Cloud + Python (Recommended for Prototype)
**Pros:**
- Easiest to set up
- No server management
- Built-in monitoring

**Cons:**
- €20/month for n8n Cloud
- Vendor lock-in

**Setup time:** 30 minutes

---

### Option 2: Self-Hosted n8n on VPS
**Pros:**
- Full control
- Lower cost (€4.5/month for Hetzner CX11)
- Can scale easily

**Cons:**
- Requires Docker knowledge
- Need to manage SSL certificates
- More maintenance

**Setup time:** 2-3 hours

---

### Option 3: Serverless (Vercel Edge Functions)
**Pros:**
- Lowest cost (almost free for low volume)
- Auto-scaling
- Built-in SSL

**Cons:**
- More complex setup
- Cold starts
- Vendor-specific

**Setup time:** 1-2 hours

---

## Cost Estimates

### Phase 1 Prototype (50 leads/month)

**API Costs:**
- Anthropic Claude: ~€1.50/month (€0.03/lead)
- HubSpot: €0 (free tier)
- Slack: €0 (free tier)

**Infrastructure:**
- **Option A (n8n Cloud):** €20/month
- **Option B (Self-hosted):** €4.50/month
- **Option C (Serverless):** €0-5/month

**Total: €6-22/month**

### Phase 1 Production (100 leads/month)

**API Costs:**
- Anthropic: ~€3/month
- Other APIs: €0

**Infrastructure:**
- n8n Cloud Pro: €50/month
- Supabase: €0 (free tier)

**Total: €53/month**

---

## Monitoring

### Key Metrics to Track

**Operational:**
- Average processing time: <2 minutes
- API success rate: >99%
- Error rate: <1%

**Business:**
- Average score by industry
- Distribution: High/Med/Low priority
- Time saved vs manual process

### Simple Monitoring Script

```python
# monitor.py
import json
from datetime import datetime, timedelta

def analyze_leads(results_file="test_results.json"):
    with open(results_file) as f:
        results = json.load(f)
    
    scores = [r['score'] for r in results if 'score' in r]
    
    print(f"Total leads analyzed: {len(scores)}")
    print(f"Average score: {sum(scores)/len(scores):.1f}")
    print(f"High priority (70+): {len([s for s in scores if s >= 70])}")
    print(f"Medium priority (40-69): {len([s for s in scores if 40 <= s < 70])}")
    print(f"Low priority (<40): {len([s for s in scores if s < 40])}")

if __name__ == "__main__":
    analyze_leads()
```

---

## Troubleshooting

### Issue: "ANTHROPIC_API_KEY not set"

```bash
# Check if .env file exists
cat .env

# Make sure you're in the right directory and venv is activated
source venv/bin/activate

# Set API key manually
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Issue: "Invalid API key"

- Verify key is correct at https://console.anthropic.com
- Check for extra spaces in .env file
- Regenerate API key if needed

### Issue: "JSON decode error"

- This means Claude returned non-JSON text
- Usually happens with very unusual leads
- Check the actual response in error message
- May need to adjust the prompt

### Issue: Low scoring accuracy

```python
# Adjust scoring weights in lead_qualification_agent.py

# Current weights (line ~20-30):
# Industry Fit: 40%
# Budget: 25%
# Timeline: 20%
# Needs Clarity: 15%

# Example adjustment for more budget-sensitive scoring:
# Industry Fit: 30%
# Budget: 35%
# Timeline: 20%
# Needs Clarity: 15%
```

---

## Next Steps

### Immediate (Today)
1. Run test suite and validate scores
2. Test with 3-5 real past leads
3. Adjust scoring weights if needed

### Short-term (This Week)
1. Set up n8n workflow
2. Connect to HubSpot (create custom properties first)
3. Test end-to-end with staging environment
4. Deploy to production

### Medium-term (Next 2 Weeks)
1. Monitor first 20 real leads
2. Calculate time saved
3. Measure scoring accuracy vs manual
4. Iterate on prompt if needed

### Long-term (Next Month)
1. Start Phase 2 planning (outbound prospecting)
2. Build cost tracking dashboard
3. Document learnings for team
4. Consider hiring developer if scaling

---

## File Structure

```
kairos-lead-gen-prototype/
├── .env                          # API keys (DO NOT COMMIT)
├── .gitignore                    # Ignore .env, venv, etc.
├── README.md                     # This file
├── lead_qualification_agent.py   # Main agent code
├── test_qualification.py         # Test suite
├── test_results.json             # Test results output
├── requirements.txt              # Python dependencies
└── venv/                         # Virtual environment (DO NOT COMMIT)
```

---

## Security Best Practices

**DO:**
- ✅ Store API keys in .env file
- ✅ Add .env to .gitignore
- ✅ Use environment variables in n8n
- ✅ Enable HTTPS on webhook endpoint
- ✅ Rotate API keys quarterly

**DON'T:**
- ❌ Commit API keys to Git
- ❌ Share API keys in Slack/email
- ❌ Use same API key across environments
- ❌ Expose webhook URL publicly without auth
- ❌ Log sensitive customer data in plain text

---

## Support

**Documentation:**
- Full project plan: `project_plan.md`
- API contracts: `api_contracts_data_models.md`
- Cost analysis: `cost_analysis.md`
- Deployment guide: `deployment_runbook.md`

**Questions?**
- Review lab_summary.md for reflection on challenges
- Check deployment_runbook.md for operations guidance
- Refer to API contracts for integration details

**Found a bug?**
- Document it in test_results.json
- Add to issues list in project_plan.md
- Consider it learning for next iteration

---

## Lab Submission Checklist

For Ironhack Lab submission:

- [x] Project plan document (project_plan.md)
- [x] Technical design (architecture diagrams)
- [x] Cost analysis (cost_analysis.md)
- [x] API contracts and data models (api_contracts_data_models.md)
- [x] Deployment plan (deployment_runbook.md)
- [x] Working prototype (lead_qualification_agent.py)
- [x] Test suite (test_qualification.py)
- [x] lab_summary.md (reflection paragraph)
- [x] README with setup instructions

**Estimated completion time:** 60-90 minutes (planning) + 30-60 minutes (prototype testing)

---

**Good luck with your lab!** 🚀

**Created by:** Lucas Barrios  
**Date:** May 18, 2026  
**Version:** 1.0
