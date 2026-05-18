# Lab Summary: Autonomous Agent Challenge

## What Was Built

A fully production-deployed AI lead qualification system for Kairos Consulting. The system is live and processing real inbound leads from `kairosconsulting.co`.

**Complete stack implemented:**
- **Claude Sonnet 4.6** scoring agent with deterministic weighted recalculation (40/25/20/15)
- **FastAPI** wrapper deployed to **Vercel** at `api.kairosconsulting.co` (free, permanent, no ngrok)
- **n8n** 5-node workflow (Webhook → /qualify → Slack → HubSpot Contact → HubSpot Deal) — published and live
- **HubSpot CRM** — contacts upserted by email, deals created in correct pipeline stage, 14 custom AI scoring properties created
- **Slack** block-kit notifications on every new lead
- **Next.js contact form** on the live website wired directly to the n8n webhook

**Key technical decisions made during the lab:**
- Replaced the `anthropic` SDK with direct `requests` calls to fix a Vercel serverless compatibility issue (`httpx` connection failures)
- Moved overall score calculation from LLM to Python to eliminate arithmetic drift
- Used HubSpot PATCH with `?idProperty=email` for upsert behavior (avoids 409 duplicates)
- Vercel chosen over Railway/Render — free tier, already the existing infrastructure provider
- n8n workflow must be **Published** (not just saved/toggled) for the production webhook URL to register

---

## Reflection

The hardest part of planning this system was defining realistic scope boundaries between phases. I initially wanted to build the complete lead generation and qualification system (inbound + outbound prospecting + automated outreach) as the MVP, but quickly realized this was a 6-week production project, not a 60-minute lab. The discipline required to isolate Phase 1 (inbound qualification only) as the actual MVP — while documenting Phases 2-3 as future roadmap — was critical but difficult.

The biggest unexpected challenge was not the AI logic itself but the **integration plumbing**: HubSpot's legacy Service Key auth model, Vercel Python runtime incompatibilities with httpx, n8n's distinction between test and production webhook URLs, and the `properties` wrapper requirement in HubSpot's v3 API. Each of these required debugging that wasn't part of the original plan.

The biggest open question going into Phase 2 is whether LangGraph is actually necessary for the prospect research workflow, or if a simpler sequential chain would suffice. LangGraph adds complexity (state management, graph visualization) but provides better control over multi-step research. The decision hinges on how often the agent needs to backtrack or retry failed steps — if retries are rare, LangChain might be enough.

---

## Phase 1 — Completed ✅

| Milestone | Status |
|---|---|
| Claude scoring agent (6/6 tests passing) | ✅ |
| FastAPI wrapper + Swagger UI | ✅ |
| Vercel deployment at api.kairosconsulting.co | ✅ |
| n8n 5-node workflow published | ✅ |
| Slack notifications | ✅ |
| HubSpot contact + deal creation | ✅ |
| 14 HubSpot custom properties (Kairos AI Scoring group) | ✅ |
| Live website form connected to n8n webhook | ✅ |

## Phase 2 — Planned

Outbound prospecting with LangGraph + Tavily: identify target companies, research decision-makers, score fit, draft personalized outreach.

---

**Lab completed by:** Lucas Barrios  
**Date:** May 18, 2026  
**Program:** Ironhack AI Manager / AI Consulting Specialization
