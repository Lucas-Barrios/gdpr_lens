# Kairos Lead Generation System - Prototype
## Phase 1: Inbound Lead Qualification

**Created:** May 18, 2026  
**For:** Ironhack Lab - Autonomous Agent Challenge  
**Author:** Lucas Barrios  

---

## Overview

An AI-powered lead qualification system that automatically scores and routes inbound leads from the Kairos website contact form. Built with Claude Sonnet 4.6 and exposed as an HTTP API so n8n can orchestrate the full workflow.

**What it does:**
1. Receives a lead (via API or n8n webhook) with company, industry, budget, timeline, and needs
2. Calls Claude Sonnet 4.6 to score the lead across 4 dimensions (industry fit, budget, timeline, needs clarity)
3. Recalculates the overall score deterministically using defined weights (40/25/20/15)
4. Routes to the appropriate HubSpot pipeline stage (70+ = high priority, 40-69 = medium, <40 = low)
5. Returns a ready-to-use HubSpot contact/deal payload and a Slack block-kit notification

**Test results:** 6/6 test cases passing (100%) across all target industries.

---

## Architecture

```
Website Form
     │
     ▼
n8n Webhook Trigger
     │
     ▼
POST /qualify  ◄─── FastAPI (api.py)
     │                    │
     │              Claude Sonnet 4.6
     │              (lead_qualification_agent.py)
     │
     ├──► HubSpot API  (create contact + deal)
     ├──► Slack Webhook (block-kit notification)
     └──► Supabase     (lead history log)
```

---

## File Structure

```
Autonomous_Agent_Challenge/
├── .env                          # API keys — DO NOT COMMIT (gitignored)
├── .env.example                  # Safe template — copy to .env and fill in
├── .gitignore                    # Ignores .env, __pycache__
├── api.py                        # FastAPI wrapper — exposes /qualify and /health
├── lead_qualification_agent.py   # Core agent: scoring logic + HubSpot/Slack formatting
├── quick_test.py                 # Single-lead smoke test (run before full suite)
├── test_qualification.py         # Full 6-case test suite
├── test_results.json             # Latest test run results
└── requirements.txt              # Python dependencies
```

---

## Prerequisites

**Required:**
- Python 3.9+
- Anthropic API key ([console.anthropic.com](https://console.anthropic.com))

**For full n8n integration:**
- n8n instance (cloud or self-hosted)
- HubSpot account with API access
- Slack webhook URL
- Supabase project (optional — for lead history logging)

---

## Quick Start

### 1. Clone and install dependencies

```bash
git clone https://github.com/Lucas-Barrios/Autonomous-Agent-Challenge.git
cd Autonomous-Agent-Challenge/Autonomous_Agent_Challenge
pip install -r requirements.txt
```

### 2. Configure your API key

```bash
cp .env.example .env
# Open .env and replace the placeholder with your real key:
# ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

### 3. Run the smoke test (single lead)

```bash
python3 quick_test.py
```

Expected: score ≥ 80, stage = `Outreach Sent` for a wellness studio lead.

### 4. Run the full test suite

```bash
python3 test_qualification.py
```

Expected output:
```
TEST SUMMARY
Total Tests: 6
Passed: 6 ✅
Failed: 0 ❌
Success Rate: 100.0%
```

### 5. Start the API server

```bash
python3 -m uvicorn api:app --port 8000
```

Then open **http://127.0.0.1:8000/docs** in your browser — interactive Swagger UI to test the endpoint live.

---

## API Reference

### `GET /health`

Liveness check for n8n or monitoring tools.

```bash
curl http://localhost:8000/health
# → {"status": "ok"}
```

### `POST /qualify`

Qualify a lead and receive scores, HubSpot payload, and Slack notification payload.

**Request body:**

```json
{
  "full_name": "Dr. Thomas Weber",
  "email": "weber@aesthetics-berlin.de",
  "phone": "+49 30 666 0000",
  "company_name": "Berlin Aesthetics Clinic",
  "industry": "Aesthetic Clinics",
  "budget_range": "€25K-€50K",
  "timeline": "1-3 months",
  "needs": "Patient intake and appointment scheduling automation. 200+ new patient inquiries per month handled manually."
}
```

**Response (abbreviated):**

```json
{
  "qualification": {
    "overall_score": 92,
    "recommended_stage": "Outreach Sent",
    "scores": {
      "industry_fit": 95,
      "budget_alignment": 90,
      "timeline_urgency": 80,
      "needs_clarity": 100
    },
    "reasoning": "Near-ideal profile — high-volume pain point, strong budget, short timeline.",
    "key_insights": ["200+ monthly inquiries = quantified ROI case", "..."],
    "suggested_next_action": "Send personalized outreach within 24 hours...",
    "suggested_use_case": "AI patient intake chatbot + automated scheduling"
  },
  "hubspot": {
    "contact": { "email": "...", "kairos_qualification_score": "92", "..." },
    "deal":    { "dealstage": "outreachsent", "pipeline": "kairos_sales_pipeline", "..." }
  },
  "slack": {
    "text": "New qualified lead: Dr. Thomas Weber (Score: 92/100)",
    "blocks": [ "..." ]
  }
}
```

---

## Scoring Logic

Overall score = weighted sum of 4 sub-scores. The LLM estimates sub-scores; the final rollup is calculated in Python to keep it deterministic.

### Industry Fit — 40%

| Industry | Score |
|---|---|
| Wellness & Fitness Studios | 100 |
| Aesthetic Clinics | 95 |
| Private Medical Clinics | 95 |
| Hairdressers & Beauty Salons | 90 |
| Real Estate Agencies | 85 |
| Other service businesses | 70 |
| Retail / E-commerce | 60 |
| Manufacturing / Pure tech | 50 |

### Budget Alignment — 25%

| Budget | Score |
|---|---|
| €50K+ | 100 |
| €25K–€50K | 90 |
| €10K–€25K | 75 |
| €5K–€10K | 50 |
| <€5K or not sure | 25 |

### Timeline Urgency — 20%

| Timeline | Score |
|---|---|
| Immediately | 100 |
| 1–3 months | 80 |
| 3–6 months | 60 |
| 6+ months | 40 |
| Not sure | 30 |

### Needs Clarity — 15%

| Clarity | Score |
|---|---|
| Specific use case + clear pain point | 100 |
| General operational challenge | 75 |
| Vague interest / "exploring AI" | 50 |
| No clear use case | 25 |

### Routing

| Score | HubSpot Stage | Action |
|---|---|---|
| 70–100 | `Outreach Sent` | Personalized outreach within 24h |
| 40–69 | `Lead` | Nurture sequence |
| 0–39 | `Lead` + tag `Low Fit - Nurture` | Educational content, re-qualify in 6 months |

---

## n8n Integration

### Workflow (5 nodes — fully implemented)

```
1. Webhook Trigger           ← POST from website contact form
        │
2. HTTP Request → /qualify   ← POST https://<ngrok-or-prod-url>/qualify
        │                       body: { full_name, email, company_name, ... }
        │
3. HTTP Request → Slack      ← POST {{ $json.slack }} to Slack Incoming Webhook
        │
4. HTTP Request → HubSpot Contact  ← POST /crm/v3/objects/contacts
        │                              body: { "properties": {{ $json.hubspot.contact }} }
        │
5. HTTP Request → HubSpot Deal     ← POST /crm/v3/objects/deals
                                       body: { "properties": {{ $json.hubspot.deal }} }
```

**Status: All 5 nodes tested and confirmed working end-to-end.**

### Node-by-node configuration

#### Node 1 — Webhook Trigger
- **Authentication:** None
- **HTTP Method:** POST
- **Response Mode:** When Last Node Finishes

#### Node 2 — HTTP Request `/qualify`
- **Method:** POST
- **URL:** `https://<your-ngrok-url>/qualify`
- **Body Content Type:** JSON
- **Body:**
```json
{
  "full_name": "{{ $json.body.full_name }}",
  "email": "{{ $json.body.email }}",
  "company_name": "{{ $json.body.company_name }}",
  "industry": "{{ $json.body.industry }}",
  "budget_range": "{{ $json.body.budget_range }}",
  "timeline": "{{ $json.body.timeline }}",
  "needs": "{{ $json.body.needs }}",
  "phone": "{{ $json.body.phone }}"
}
```

#### Node 3 — Slack Notification
- **Method:** POST
- **URL:** Your Slack Incoming Webhook URL
- **Body Content Type:** JSON
- **Body:** `{{ JSON.stringify($json.slack) }}`

#### Node 4 — HubSpot Contact
- **Method:** POST
- **URL:** `https://api.hubapi.com/crm/v3/objects/contacts`
- **Headers:** `Authorization: Bearer pat-eu1-YOUR_TOKEN`
- **Body Content Type:** JSON
- **Body:**
```json
{
  "properties": {{ JSON.stringify($json.hubspot.contact) }}
}
```

#### Node 5 — HubSpot Deal
- **Method:** POST
- **URL:** `https://api.hubapi.com/crm/v3/objects/deals`
- **Headers:** `Authorization: Bearer pat-eu1-YOUR_TOKEN`
- **Body Content Type:** JSON
- **Body:**
```json
{
  "properties": {{ JSON.stringify($json.hubspot.deal) }}
}
```

### HubSpot Setup

**Create a Service Key (HubSpot's current auth method):**
1. Go to `app-eu1.hubspot.com` → Settings → Integrations → Private Apps
2. If redirected to "Legacy Apps", choose **Create Service Key**
3. Required scopes: `crm.objects.contacts.write`, `crm.objects.deals.write`, `crm.objects.contacts.read`, `crm.objects.deals.read`
4. Copy the generated token (`pat-eu1-...`) into your n8n HubSpot nodes as `Bearer <token>`

**HubSpot Pipeline Stage IDs (Kairos Sales Pipeline):**

| Stage | HubSpot ID |
|---|---|
| Lead | `5198127291` |
| Outreach Sent | `5198127292` |

### Exposing the API to n8n

**Local testing — use ngrok:**
```bash
python3 -m uvicorn api:app --port 8000
ngrok http 8000
# Copy the https://xxxx.ngrok-free.app URL into Node 2 in n8n
```

**If port 8000 is already in use:**
```bash
kill $(lsof -ti:8000)
python3 -m uvicorn api:app --port 8000
```

**Production — deploy to Railway or Render:**
```bash
# Railway (one command after linking repo):
railway up
```

---

## Test Cases

| Lead | Industry | Budget | Timeline | Score | Stage |
|---|---|---|---|---|---|
| FitLife Studios GmbH | Wellness & Fitness | €10K–€25K | Immediately | 94 | Outreach Sent ✅ |
| Berlin Aesthetics Clinic | Aesthetic Clinics | €25K–€50K | 1–3 months | 92 | Outreach Sent ✅ |
| Praxis Dr. Müller | Private Medical | €10K–€25K | 1–3 months | 88 | Outreach Sent ✅ |
| Salon Luxe Berlin | Beauty Salons | €5K–€10K | 1–3 months | 80 | Outreach Sent ✅ |
| Becker Immobilien GmbH | Real Estate | €10K–€25K | 3–6 months | 76 | Outreach Sent ✅ |
| Modehaus Hoffmann | Retail | €5K–€10K | 6+ months | 52 | Lead ✅ |

Full results: `Autonomous_Agent_Challenge/test_results.json`

---

## Troubleshooting

**`ANTHROPIC_API_KEY not set`**
```bash
cat .env   # confirm key is present and starts with sk-ant-
```

**`model not found` (404)**
The agent uses `claude-sonnet-4-6`. If you see a 404, your API key may not have access to this model — check [console.anthropic.com](https://console.anthropic.com).

**`JSON decode error`**
Claude returned non-JSON output. Rare with the current prompt. Check the raw error message for the actual response text.

**Port 8000 already in use**
```bash
kill $(lsof -ti:8000) && python3 -m uvicorn api:app --port 8000
```

**HubSpot 401 Unauthorized**
Ensure the Authorization header in n8n HubSpot nodes is `Bearer pat-eu1-YOUR_TOKEN` (not just the token alone). HubSpot EU instance base URL: `https://api.hubapi.com` (same for EU and US portals).

**HubSpot contact created with no data**
The v3 API requires a `properties` wrapper. The request body must be:
```json
{ "properties": { "email": "...", "firstname": "...", ... } }
```
Not a flat object.

---

## Cost Estimates

| Volume | Anthropic API | n8n Cloud | Total/month |
|---|---|---|---|
| 50 leads/month | ~€1.50 | €20 (starter) | ~€22 |
| 100 leads/month | ~€3 | €20 (starter) | ~€23 |
| 500 leads/month | ~€15 | €50 (pro) | ~€65 |

Per-lead cost: ~€0.03 (≈1,300 tokens input + 400 tokens output at Sonnet pricing).

---

## Next Steps

- [x] Build n8n workflow (webhook → /qualify → Slack → HubSpot contact → HubSpot deal)
- [x] Connect HubSpot Service Key authentication
- [x] Validate end-to-end: contact and deal created in HubSpot with correct stage
- [ ] Deploy API to Railway / Render for permanent URL (removes ngrok dependency)
- [ ] Create HubSpot custom properties (`kairos_qualification_score`, `kairos_budget_fit_score`, etc.)
- [ ] Connect live website form to n8n webhook
- [ ] Monitor first 20 real leads, validate scores vs manual judgment
- [ ] Phase 2: outbound prospecting with LangGraph + Tavily

---

## Supporting Documents

| File | Description |
|---|---|
| `project_plan.md` | Full 3-phase roadmap with timelines and budget |
| `api_contracts_data_models.md` | Request/response schemas for all integrations |
| `cost_analysis.md` | Detailed API cost breakdown |
| `deployment_runbook.md` | Step-by-step production deployment guide |
| `lab_summary.md` | Lab reflection and open questions |

---

**Created by:** Lucas Barrios  
**Date:** May 18, 2026  
**Version:** 2.0
