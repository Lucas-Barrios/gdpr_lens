# API Contracts & Data Models
## Kairos Consulting Lead Generation System

**Created:** May 18, 2026  
**Version:** 1.0  

---

## Overview

This document defines all API contracts, data models, and integration specifications for the lead generation system. It serves as the single source of truth for data structures flowing between components.

---

## 1. Website Form → Supabase → n8n Webhook

### Form Submission Payload

**HTTP Method:** POST  
**Content-Type:** application/json  
**Endpoint:** `https://n8n.kairos-consulting.com/webhook/lead-intake`  

```json
{
  "id": "uuid-v4",
  "created_at": "2026-05-18T14:32:00Z",
  "source": "website_contact_form",
  "data": {
    "full_name": "Maria Schmidt",
    "email": "maria@example.com",
    "phone": "+49 30 000 0000",
    "company_name": "Your Business GmbH",
    "industry": "Fitness & Wellness",
    "budget_range": "€10K-€25K",
    "timeline": "1-3 months",
    "needs": "What's your biggest operational challenge? What would you like AI to help with? What have you already tried?"
  },
  "metadata": {
    "ip_address": "192.168.1.1",
    "user_agent": "Mozilla/5.0...",
    "language": "de",
    "referrer": "https://google.com"
  }
}
```

### Field Specifications

| Field | Type | Required | Validation | Notes |
|-------|------|----------|------------|-------|
| `id` | UUID | Yes | Valid UUID v4 | Supabase auto-generated |
| `created_at` | ISO 8601 | Yes | Valid datetime | Supabase timestamp |
| `source` | String | Yes | Enum: `website_contact_form`, `calendly_booking`, `manual_entry` | |
| `data.full_name` | String | Yes | 2-100 chars | Split into first/last in n8n |
| `data.email` | String | Yes | Valid email regex | Required for HubSpot contact |
| `data.phone` | String | No | E.164 format preferred | Optional |
| `data.company_name` | String | Yes | 2-200 chars | |
| `data.industry` | String | Yes | From dropdown | Predefined list |
| `data.budget_range` | String | Yes | From dropdown | €5K-€10K, €10K-€25K, €25K-€50K, €50K+ |
| `data.timeline` | String | Yes | From dropdown | Immediately, 1-3 months, 3-6 months, 6+ months |
| `data.needs` | String | Yes | 50-2000 chars | Free text |

### Industry Dropdown Values

```json
[
  "Wellness & Fitness Studios",
  "Aesthetic Clinics",
  "Private Medical Clinics",
  "Hairdressers & Beauty Salons",
  "Real Estate Agencies",
  "Hospitality & Restaurants",
  "Professional Services",
  "Retail & E-commerce",
  "Education & Training",
  "Technology & Software",
  "Other"
]
```

---

## 2. n8n → Claude API (LangChain)

### Qualification Request

**Library:** `langchain` Python SDK  
**Model:** `claude-3-5-sonnet-20241022`  
**Max Tokens:** 1000  

```python
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 1000,
  "temperature": 0.3,
  "system": "You are a lead qualification expert for Kairos Consulting...",
  "messages": [
    {
      "role": "user",
      "content": """
        Analyze this lead submission and provide a qualification score.

        LEAD DATA:
        - Name: Maria Schmidt
        - Company: Your Business GmbH
        - Industry: Fitness & Wellness
        - Budget: €10K-€25K
        - Timeline: 1-3 months
        - Needs: We have 5 fitness studios in Berlin and spend too much time manually responding to customer inquiries about class schedules, memberships, and trainer availability. We'd like to explore AI chatbots.

        SCORING CRITERIA:
        1. Industry Fit (40%): Education sector = 100, SME services = 80, Other = 50
        2. Budget Alignment (25%): €25K+ = 100, €10K-€25K = 75, €5K-€10K = 50, <€5K = 25
        3. Timeline Urgency (20%): Immediately = 100, 1-3mo = 80, 3-6mo = 60, 6+mo = 40
        4. Needs Clarity (15%): Specific use case = 100, General interest = 50, Vague = 25

        OUTPUT FORMAT (JSON):
        {
          "overall_score": 0-100,
          "scores": {
            "industry_fit": 0-100,
            "budget_alignment": 0-100,
            "timeline_urgency": 0-100,
            "needs_clarity": 0-100
          },
          "reasoning": "2-3 sentence explanation",
          "recommended_stage": "Outreach Sent" | "Lead" | "Lead (Low Fit)",
          "key_insights": ["insight 1", "insight 2"],
          "suggested_next_action": "specific action for Lucas"
        }
      """
    }
  ]
}
```

### Qualification Response

```json
{
  "id": "msg_01ABC123",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "{\"overall_score\": 78, \"scores\": {\"industry_fit\": 80, \"budget_alignment\": 75, \"timeline_urgency\": 80, \"needs_clarity\": 100}, \"reasoning\": \"Strong fit - SME service business with clear AI use case (customer service automation). Budget and timeline align well with typical engagement. Specific pain point identified (manual inquiry handling).\", \"recommended_stage\": \"Outreach Sent\", \"key_insights\": [\"Multi-location fitness business with scalable automation opportunity\", \"Already thinking about chatbots, ready for AI readiness assessment\"], \"suggested_next_action\": \"Send personalized email about customer service automation case studies in fitness industry\"}"
    }
  ],
  "model": "claude-3-5-sonnet-20241022",
  "usage": {
    "input_tokens": 1847,
    "output_tokens": 342
  }
}
```

---

## 3. n8n → HubSpot API

### Create Contact

**Endpoint:** `POST /crm/v3/objects/contacts`  
**Authentication:** Bearer token  

```json
{
  "properties": {
    "email": "maria@example.com",
    "firstname": "Maria",
    "lastname": "Schmidt",
    "phone": "+49 30 000 0000",
    "company": "Your Business GmbH",
    "industry": "Fitness & Wellness",
    "hs_lead_status": "NEW",
    "kairos_budget_range": "€10K-€25K",
    "kairos_timeline": "1-3 months",
    "kairos_needs_summary": "Customer service automation for 5 fitness studios",
    "kairos_lead_source": "Website Contact Form",
    "kairos_qualification_score": "78",
    "kairos_industry_fit_score": "80",
    "kairos_budget_fit_score": "75",
    "kairos_timeline_urgency": "80",
    "kairos_needs_clarity": "100"
  }
}
```

### Create Deal

**Endpoint:** `POST /crm/v3/objects/deals`  
**Authentication:** Bearer token  

```json
{
  "properties": {
    "dealname": "Your Business GmbH - AI Customer Service",
    "dealstage": "outreachsent",
    "pipeline": "kairos_sales_pipeline",
    "amount": "15000",
    "closedate": "2026-08-18",
    "kairos_qualification_score": "78",
    "kairos_key_insights": "Multi-location fitness business with scalable automation opportunity; Already thinking about chatbots, ready for AI readiness assessment",
    "kairos_suggested_use_case": "AI chatbot for class schedules, memberships, trainer availability",
    "kairos_lead_source": "Website Contact Form"
  },
  "associations": [
    {
      "to": {
        "id": "12345"
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 3
        }
      ]
    }
  ]
}
```

### HubSpot Custom Properties

These must be created in HubSpot before deployment:

**Contact Properties:**
- `kairos_budget_range` (Dropdown)
- `kairos_timeline` (Dropdown)
- `kairos_needs_summary` (Multi-line text)
- `kairos_lead_source` (Dropdown)
- `kairos_qualification_score` (Number, 0-100)
- `kairos_industry_fit_score` (Number, 0-100)
- `kairos_budget_fit_score` (Number, 0-100)
- `kairos_timeline_urgency` (Number, 0-100)
- `kairos_needs_clarity` (Number, 0-100)

**Deal Properties:**
- `kairos_qualification_score` (Number, 0-100)
- `kairos_key_insights` (Multi-line text)
- `kairos_suggested_use_case` (Multi-line text)
- `kairos_lead_source` (Dropdown)

---

## 4. n8n → Slack Webhook

### Notification Payload

**Endpoint:** Slack webhook URL  
**Method:** POST  

```json
{
  "text": "New qualified lead: Maria Schmidt (Score: 78/100)",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🎯 New High-Priority Lead",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Name:*\nMaria Schmidt"
        },
        {
          "type": "mrkdwn",
          "text": "*Company:*\nYour Business GmbH"
        },
        {
          "type": "mrkdwn",
          "text": "*Industry:*\nFitness & Wellness"
        },
        {
          "type": "mrkdwn",
          "text": "*Score:*\n78/100 ⭐"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Key Insights:*\n• Multi-location fitness business with scalable automation opportunity\n• Already thinking about chatbots, ready for AI readiness assessment"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Suggested Next Action:*\nSend personalized email about customer service automation case studies in fitness industry"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "View in HubSpot",
            "emoji": true
          },
          "url": "https://app.hubspot.com/contacts/12345/deal/67890",
          "style": "primary"
        }
      ]
    }
  ]
}
```

---

## 5. Phase 2: Prospect Research Data Model

### Supabase `prospects` Table Schema

```sql
CREATE TABLE prospects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Company Info
  company_name TEXT NOT NULL,
  website TEXT,
  industry TEXT,
  location TEXT,
  employee_range TEXT,
  revenue_estimate TEXT,
  business_model TEXT,
  main_products_services TEXT,
  
  -- Scoring
  overall_score INTEGER CHECK (overall_score >= 0 AND overall_score <= 100),
  fit_score INTEGER,
  ai_opportunity_score INTEGER,
  urgency_score INTEGER,
  budget_likelihood_score INTEGER,
  contactability_score INTEGER,
  
  -- Analysis
  why_relevant TEXT,
  pain_points JSONB,
  suggested_use_cases JSONB,
  trigger_events JSONB,
  
  -- Contacts
  decision_makers JSONB,
  
  -- Outreach
  outreach_angle TEXT,
  suggested_message TEXT,
  objections JSONB,
  buying_readiness TEXT,
  recommended_next_action TEXT,
  
  -- Meta
  data_sources JSONB,
  confidence_level TEXT,
  research_status TEXT DEFAULT 'pending',
  hubspot_deal_id TEXT,
  
  CONSTRAINT valid_scores CHECK (
    fit_score >= 0 AND fit_score <= 100 AND
    ai_opportunity_score >= 0 AND ai_opportunity_score <= 100 AND
    urgency_score >= 0 AND urgency_score <= 100 AND
    budget_likelihood_score >= 0 AND budget_likelihood_score <= 100 AND
    contactability_score >= 0 AND contactability_score <= 100
  )
);

-- Indexes
CREATE INDEX idx_prospects_overall_score ON prospects(overall_score DESC);
CREATE INDEX idx_prospects_research_status ON prospects(research_status);
CREATE INDEX idx_prospects_created_at ON prospects(created_at DESC);
```

### Prospect Research Output (JSON)

```json
{
  "company_name": "VitalSpa Wellness Centers",
  "website": "https://vitalspa-berlin.de",
  "industry": "Wellness & Spa",
  "location": "Berlin, Germany",
  "employee_range": "40-60",
  "revenue_estimate": "€3-5M",
  "business_model": "B2C wellness services, spa treatments, massage therapy, yoga classes",
  "main_products_services": "Spa treatments, massage therapy, yoga and fitness classes, wellness consultations, membership packages",
  
  "overall_score": 88,
  "fit_score": 95,
  "ai_opportunity_score": 90,
  "urgency_score": 75,
  "budget_likelihood_score": 80,
  "contactability_score": 85,
  
  "why_relevant": "This wellness center chain operates 3 locations in Berlin with high customer volume and multiple touchpoints (booking, class scheduling, membership management). Their website shows traditional contact forms and phone-based booking, suggesting significant automation opportunities. Recent expansion to third location indicates growth trajectory and process strain.",
  
  "pain_points": [
    {
      "pain_point": "Manual booking and scheduling",
      "evidence": "Website has separate booking forms for spa, massage, and classes - suggests fragmented process",
      "ai_opportunity": "Unified AI-powered booking system with automated confirmations and reminders"
    },
    {
      "pain_point": "Customer communication overload",
      "evidence": "FAQ page mentions 'Call us for availability and pricing' - indicates high inquiry volume",
      "ai_opportunity": "AI chatbot for pricing, availability, service descriptions, and membership questions"
    },
    {
      "pain_point": "Membership retention challenges",
      "evidence": "Multiple membership tiers visible, common pain point in wellness industry",
      "ai_opportunity": "Automated engagement sequences and personalized class recommendations"
    }
  ],
  
  "suggested_use_cases": [
    {
      "use_case": "AI-powered booking and client intake system",
      "fit_reason": "High ROI, addresses immediate pain point, quick implementation",
      "estimated_value": "€15,000-25,000"
    },
    {
      "use_case": "Customer service chatbot for 24/7 availability",
      "fit_reason": "Reduces front desk workload, improves customer experience",
      "estimated_value": "€10,000-15,000"
    },
    {
      "use_case": "AI Readiness Assessment",
      "fit_reason": "Low-risk entry point to identify additional automation opportunities",
      "estimated_value": "€3,000-5,000"
    }
  ],
  
  "trigger_events": [
    {
      "event": "Recent expansion",
      "details": "Opened third location in Prenzlauer Berg 4 months ago according to Google Maps",
      "urgency_indicator": "High - expansion creates operational complexity, good timing for automation"
    },
    {
      "event": "Hiring activity",
      "details": "Front desk coordinator position posted 2 weeks ago on Indeed, mentions 'managing high volume of customer inquiries'",
      "urgency_indicator": "Medium - hiring challenges suggest automation could reduce staffing needs"
    }
  ],
  
  "decision_makers": [
    {
      "name": "Christina Bauer",
      "role": "Founder & CEO",
      "linkedin_url": "https://linkedin.com/in/christina-bauer-vitalspa",
      "email": "c.bauer@vitalspa-berlin.de",
      "confidence": "High",
      "relevance": "Owner-operator, final decision-maker for major investments, personally involved in operations"
    },
    {
      "name": "Michael Klein",
      "role": "Operations Manager",
      "linkedin_url": "https://linkedin.com/in/michael-klein-wellness",
      "email": "m.klein@vitalspa-berlin.de",
      "confidence": "Medium",
      "relevance": "Day-to-day operations, manages front desk and booking systems, good initial contact"
    }
  ],
  
  "outreach_angle": "Mention their recent expansion to 3 locations and the operational complexity of managing bookings, class schedules, and customer inquiries across multiple sites. Position conversation around reducing manual coordination work and improving customer experience with unified booking and communication system. Lead with AI readiness assessment as low-risk entry point.",
  
  "suggested_message": {
    "channel": "LinkedIn",
    "subject": null,
    "body": "Hi Christina,\n\nI came across VitalSpa and saw your recent expansion to Prenzlauer Berg - congratulations!\n\nFor wellness centers managing multiple locations, AI can often streamline booking, class scheduling, and customer communications without requiring major system overhauls.\n\nI work with wellness and fitness businesses in Berlin on practical automation. Would it be relevant to exchange briefly about where AI could reduce coordination overhead across your three locations?\n\nBest,\nLucas"
  },
  
  "objections": [
    {
      "objection": "We already have a booking system",
      "response": "AI can integrate with your existing system to add intelligent automation - confirmations, reminders, availability queries - without replacing what works"
    },
    {
      "objection": "Our clients prefer personal touch",
      "response": "AI handles routine questions and bookings 24/7, freeing your team to focus on in-person service where personal touch matters most"
    },
    {
      "objection": "Budget is tight after expansion",
      "response": "Start with small pilot (€5-8K) to prove ROI before larger investment. Many wellness centers see payback in 3-6 months through reduced admin time"
    }
  ],
  
  "buying_readiness": "Warm - Strong fit, visible growth trajectory, clear automation opportunities. Recent expansion suggests budget availability but also stretched resources. Likely receptive to automation that reduces operational burden.",
  
  "recommended_next_action": "Send personalized LinkedIn message to Christina Bauer (CEO) emphasizing multi-location operational efficiency. If no response after 5 business days, follow up by email with brief wellness industry automation case study.",
  
  "data_sources": [
    "Company website (vitalspa-berlin.de)",
    "Google Maps business listings (3 locations)",
    "LinkedIn company page",
    "Indeed job posting for Front Desk Coordinator"
  ],
  
  "confidence_level": "High",
  "limitations": "Revenue estimate based on industry averages for similar-sized wellness centers. Email addresses constructed from common patterns (not verified). No inside information on current tech stack or budget cycles."
}
```

---

## 6. Tavily API Integration

### Search Request

**Endpoint:** `https://api.tavily.com/search`  
**Method:** POST  

```json
{
  "query": "logistics companies Berlin B2B 50-150 employees",
  "search_depth": "advanced",
  "max_results": 10,
  "include_domains": [],
  "exclude_domains": ["linkedin.com", "facebook.com"],
  "include_answer": true,
  "include_raw_content": false
}
```

### Search Response

```json
{
  "results": [
    {
      "title": "Müller Logistics GmbH - Regional Freight & Warehouse",
      "url": "https://mueller-logistics.de",
      "content": "Müller Logistics provides regional B2B freight shipping, warehouse coordination, and last-mile delivery services across Berlin and Brandenburg...",
      "score": 0.89,
      "published_date": "2025-03-15"
    }
  ],
  "answer": "Based on the search, here are logistics companies in Berlin with 50-150 employees focusing on B2B services...",
  "query": "logistics companies Berlin B2B 50-150 employees",
  "response_time": 2.3
}
```

---

## 7. Error Handling & Response Codes

### Standard Error Response

All APIs should return errors in this format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "field": "data.email",
    "timestamp": "2026-05-18T14:32:00Z",
    "request_id": "req_abc123"
  }
}
```

### Error Codes

| Code | HTTP Status | Meaning | Retry? |
|------|-------------|---------|--------|
| `VALIDATION_ERROR` | 400 | Invalid input data | No |
| `AUTHENTICATION_ERROR` | 401 | Invalid API key | No |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests | Yes, after delay |
| `API_ERROR` | 500 | Internal API failure | Yes, exponential backoff |
| `TIMEOUT` | 504 | Request timeout | Yes, 1 retry |
| `RESOURCE_NOT_FOUND` | 404 | Entity doesn't exist | No |

### Retry Logic

```python
def api_call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
        except TimeoutError:
            if attempt < max_retries - 1:
                continue
            raise
        except APIError as e:
            if e.status_code >= 500 and attempt < max_retries - 1:
                time.sleep(2)
                continue
            raise
    raise MaxRetriesExceeded()
```

---

## 8. Data Validation Rules

### Email Validation

```python
import re

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

### Phone Validation (E.164)

```python
def validate_phone(phone: str) -> bool:
    # E.164 format: +[country code][number]
    pattern = r'^\+[1-9]\d{1,14}$'
    return bool(re.match(pattern, phone))
```

### Score Validation

```python
def validate_score(score: int) -> bool:
    return 0 <= score <= 100
```

### URL Validation

```python
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False
```

---

## 9. Webhook Security

### Request Signature Verification (n8n)

n8n webhooks can be secured with HMAC signatures:

```python
import hmac
import hashlib

def verify_webhook_signature(payload: str, signature: str, secret: str) -> bool:
    expected_signature = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected_signature)
```

### IP Whitelisting

Restrict n8n webhook to Supabase IP ranges:
- Edge Functions: `[List of Supabase IPs]`
- n8n Cloud: `[List of n8n Cloud IPs]`

---

## 10. Rate Limiting

### API Rate Limits

| Service | Limit | Window | Handling |
|---------|-------|--------|----------|
| Anthropic | 50 requests/min | Rolling 60s | Queue + backoff |
| HubSpot | 100 requests/10s | Rolling 10s | Queue |
| Tavily | 100 requests/min | Rolling 60s | Batch queries |
| Hunter.io | 500 requests/month | Monthly | Track usage |
| Slack | 1 message/second | Rolling 1s | Batch notifications |

### Rate Limiter Implementation

```python
from collections import deque
from time import time, sleep

class RateLimiter:
    def __init__(self, max_calls: int, window_seconds: int):
        self.max_calls = max_calls
        self.window = window_seconds
        self.calls = deque()
    
    def wait_if_needed(self):
        now = time()
        # Remove old calls outside window
        while self.calls and self.calls[0] < now - self.window:
            self.calls.popleft()
        
        if len(self.calls) >= self.max_calls:
            # Wait until oldest call expires
            sleep_time = self.calls[0] + self.window - now
            if sleep_time > 0:
                sleep(sleep_time)
            self.calls.popleft()
        
        self.calls.append(now)
```

---

**Document Version:** 1.0  
**Last Updated:** May 18, 2026  
**Maintained By:** Lucas Barrios
