# Kairos Lead Qualification System
## Phase 1: Inbound Lead Qualification — Complete

**Created:** May 18, 2026  
**For:** Ironhack Lab - Autonomous Agent Challenge  
**Author:** Lucas Barrios  

---

## Overview

An AI-powered lead qualification system that automatically scores and routes inbound leads from the Kairos website contact form. Built with Claude Sonnet 4.6, deployed as a serverless API on Vercel, and orchestrated with n8n.

**What it does — end to end:**
1. Visitor fills out the contact form on `kairosconsulting.co`
2. The Next.js server action fires a webhook to n8n
3. n8n calls `api.kairosconsulting.co/qualify` → Claude Sonnet 4.6 scores the lead across 4 dimensions
4. Score is recalculated deterministically in Python (weights: 40/25/20/15)
5. HubSpot contact is created or updated (PATCH by email) with all AI scores
6. HubSpot deal is created in the correct pipeline stage (`Outreach Sent` ≥ 70, `Lead` otherwise)
7. Slack block-kit notification sent to the team

**Test results:** 6/6 test cases passing (100%) across all target industries.

---

## Architecture

```
kairosconsulting.co (Next.js)
  Contact Form → contact.ts (server action)
        │
        │ fire-and-forget POST
        ▼
n8n Webhook  (lucas-b.n8n.irn.hk/webhook/lead-intake)
        │
        ▼
POST api.kairosconsulting.co/qualify   ← FastAPI on Vercel
        │         Claude Sonnet 4.6
        │         (direct Anthropic API via requests)
        │
        ├──► Slack Incoming Webhook   (block-kit alert)
        ├──► HubSpot PATCH /contacts  (upsert by email + AI scores)
        └──► HubSpot POST  /deals     (pipeline stage + use case)
```

---

## File Structure

```
Autonomous_Agent_Challenge/
├── .env                              # API keys — DO NOT COMMIT (gitignored)
├── .env.example                      # Safe template — copy to .env and fill in
├── .gitignore                        # Ignores .env, __pycache__, .vercel
├── vercel.json                       # Vercel deployment config (Python, 60s timeout)
├── api.py                            # FastAPI wrapper — exposes /qualify and /health
├── lead_qualification_agent.py       # Core agent: scoring logic + HubSpot/Slack formatting
├── create_hubspot_properties.py      # One-time script: creates 14 HubSpot custom properties
├── quick_test.py                     # Single-lead smoke test (run before full suite)
├── test_qualification.py             # Full 6-case test suite
├── test_results.json                 # Latest test run results
└── requirements.txt                  # Python dependencies
```

---

## Prerequisites

**Required:**
- Python 3.9+
- Anthropic API key ([console.anthropic.com](https://console.anthropic.com))
- Vercel account (free) — for deployment

**For full n8n integration:**
- n8n instance (cloud or self-hosted)
- HubSpot account with two Service Keys (see HubSpot Setup below)
- Slack Incoming Webhook URL

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
# Open .env and add your key:
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

### 5. Start the API server (local dev)

```bash
python3 -m uvicorn api:app --port 8000
```

Swagger UI: **http://127.0.0.1:8000/docs**

---

## Deployment (Vercel)

The API is deployed to Vercel and served at **`https://api.kairosconsulting.co`**.

```bash
# First deploy
vercel link --scope <your-scope> --yes --project kairos-lead-api
vercel env add ANTHROPIC_API_KEY production   # paste key when prompted
vercel --prod

# Subsequent deploys (after code changes)
vercel --prod
```

The `vercel.json` sets a 60-second function timeout to accommodate Claude API response times.

---

## API Reference

### `GET /health`

```bash
curl https://api.kairosconsulting.co/health
# → {"status": "ok"}
```

### `POST /qualify`

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
    "deal": { "dealstage": "5198127292", "pipeline": "kairos_sales_pipeline", "..." }
  },
  "slack": {
    "text": "New qualified lead: Dr. Thomas Weber (Score: 92/100)",
    "blocks": [ "..." ]
  }
}
```

---

## Scoring Logic

Overall score = weighted sum of 4 sub-scores. Claude estimates sub-scores; the final rollup is recalculated in Python to keep it deterministic.

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
| 70–100 | `Outreach Sent` (ID: 5198127292) | Personalized outreach within 24h |
| 40–69 | `Lead` (ID: 5198127291) | Nurture sequence |
| 0–39 | `Lead (Low Fit)` | Educational content, re-qualify in 6 months |

---

## n8n Integration

### Workflow (5 nodes — published and live)

```
1. Webhook Trigger           ← POST from kairosconsulting.co contact form
        │
2. HTTP Request → /qualify   ← POST https://api.kairosconsulting.co/qualify
        │
3. HTTP Request → Slack      ← POST Slack Incoming Webhook
        │
4. HTTP Request → HubSpot Contact  ← PATCH /crm/v3/objects/contacts/{email}?idProperty=email
        │
5. HTTP Request → HubSpot Deal     ← POST /crm/v3/objects/deals
```

### Node-by-node configuration

#### Node 1 — Webhook Trigger
- **Path:** `lead-intake`
- **HTTP Method:** POST
- **Response Mode:** When Last Node Finishes

#### Node 2 — HTTP Request `/qualify`
- **Method:** POST
- **URL:** `https://api.kairosconsulting.co/qualify`
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
- **URL:** Slack Incoming Webhook URL
- **Body:** `{{ JSON.stringify($('HTTP Request').item.json.slack) }}`

#### Node 4 — HubSpot Contact (upsert)
- **Method:** PATCH
- **URL:** `https://api.hubapi.com/crm/v3/objects/contacts/{{ $('HTTP Request').item.json.hubspot.contact.email }}?idProperty=email`
- **Headers:** `Authorization: Bearer pat-eu1-YOUR_TOKEN`
- **Body:**
```json
{
  "properties": {{ JSON.stringify($('HTTP Request').item.json.hubspot.contact) }}
}
```
- **Settings:** Enable "Continue on Error" to handle first-time creation gracefully

#### Node 5 — HubSpot Deal
- **Method:** POST
- **URL:** `https://api.hubapi.com/crm/v3/objects/deals`
- **Headers:** `Authorization: Bearer pat-eu1-YOUR_TOKEN`
- **Body:**
```json
{
  "properties": {{ JSON.stringify($('HTTP Request').item.json.hubspot.deal) }}
}
```

### HubSpot Setup

**Two Service Keys required:**

| Key Name | Scopes | Used for |
|---|---|---|
| `kairos-n8n` | `crm.objects.contacts.read/write`, `crm.objects.deals.read/write` | n8n contact + deal creation |
| `kairos-schema-admin` | above + `crm.schemas.contacts.write`, `crm.schemas.deals.write` | Creating custom properties (one-time) |

**Create Service Keys:**
1. `app-eu1.hubspot.com` → Settings → Integrations → Private Apps → Create Service Key
2. Use `kairos-n8n` token in n8n nodes
3. Use `kairos-schema-admin` token only when running `create_hubspot_properties.py`

**Create custom properties (one-time):**
```bash
export HUBSPOT_TOKEN=pat-eu1-your-schema-admin-token
python3 create_hubspot_properties.py
```

This creates 14 properties (9 on contacts, 5 on deals) in the "Kairos AI Scoring" group.

**HubSpot Pipeline Stage IDs (Kairos Sales Pipeline):**

| Stage | HubSpot ID |
|---|---|
| Lead | `5198127291` |
| Outreach Sent | `5198127292` |

---

## Website Form Integration

The contact form on `kairosconsulting.co` is a custom Next.js form (`src/actions/contact.ts`). On submission it:
1. Validates fields with Zod
2. Stores the lead in Supabase
3. Fires a non-blocking POST to the n8n webhook with mapped field values
4. Sends notification email to admin (Resend)
5. Sends confirmation email to the lead

**Field mapping** (form values → n8n/qualify API):

| Form value | Mapped to |
|---|---|
| `wellness` | `Wellness & Fitness Studios` |
| `aesthetic_clinic` | `Aesthetic Clinics` |
| `5k_15k` | `€5K-€10K` |
| `15k_plus` | `€10K-€25K` |
| `immediate` | `Immediately` |
| `1_3_months` | `1-3 months` |

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

**Vercel function times out**
The `vercel.json` sets `maxDuration: 60` via the builds config. If you see timeout errors, confirm the config was deployed correctly.

**`JSON decode error`**
Claude returned non-JSON output. Rare. Check the raw error message for the actual response text.

**Port 8000 already in use (local dev)**
```bash
kill $(lsof -ti:8000) && python3 -m uvicorn api:app --port 8000
```

**HubSpot 401 Unauthorized**
Ensure the Authorization header is `Bearer pat-eu1-YOUR_TOKEN`. HubSpot EU base URL: `https://api.hubapi.com`.

**HubSpot contact created with no data**
The v3 API requires a `properties` wrapper:
```json
{ "properties": { "email": "...", "firstname": "...", ... } }
```

**HubSpot contact 409 Conflict (duplicate)**
Node 4 uses PATCH with `?idProperty=email` to upsert. Also enable "Continue on Error" on the node as a fallback.

**n8n webhook 404 (not registered)**
The workflow must be **Published** (not just saved). Click the Publish button in the top-right of the n8n editor.

---

## Cost Estimates

| Volume | Anthropic API | Vercel | n8n | Total/month |
|---|---|---|---|---|
| 50 leads/month | ~€1.50 | Free | Self-hosted | ~€1.50 |
| 100 leads/month | ~€3 | Free | Self-hosted | ~€3 |
| 500 leads/month | ~€15 | Free | Self-hosted | ~€15 |

Per-lead cost: ~€0.03 (≈1,300 tokens input + 400 tokens output at Sonnet pricing).  
Vercel hosting: free (Hobby plan, serverless functions).

---

## Phase 1 — Completed Milestones

- [x] Core Claude Sonnet 4.6 scoring agent with deterministic score recalculation
- [x] FastAPI wrapper with `/qualify` and `/health` endpoints
- [x] 6/6 test cases passing across all target industries
- [x] Deployed to Vercel at `api.kairosconsulting.co` (free, permanent URL)
- [x] n8n 5-node workflow built and published
- [x] Slack block-kit notifications
- [x] HubSpot contact upsert + deal creation with correct pipeline stage
- [x] 14 HubSpot custom properties created (Kairos AI Scoring group)
- [x] Live website form connected to n8n webhook

## Phase 2 — Next Steps

- [ ] Monitor first 20 real leads, validate scores vs manual judgment
- [ ] Associate HubSpot deals with contacts via Associations API
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
**Version:** 3.0
