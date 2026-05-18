"""
Kairos Lead Qualification Agent
Phase 1 MVP - Inbound Lead Scoring

This script implements the lead qualification logic using Claude 3.5 Sonnet.
It analyzes form submissions and generates qualification scores + routing recommendations.
"""

import os
import json
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()  # loads ANTHROPIC_API_KEY from .env if present

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

QUALIFICATION_SYSTEM_PROMPT = """You are a lead qualification expert for Kairos Consulting, an AI consulting firm based in Berlin.

COMPANY CONTEXT:
- Target customers: Service-based SMEs in wellness, fitness, aesthetics, beauty, medical, and real estate
- Services: AI readiness assessments, workflow automation, CRM optimization, chatbots, marketing automation, fractional AI consulting, team training, end-to-end implementation
- Typical deal size: €5K-€50K
- Focus: Practical AI for client-facing service businesses with high-touch operations

IDEAL CUSTOMER PROFILE:
- Service businesses (50-500 employees) with heavy client interactions
- Industries: Wellness/Fitness studios, Aesthetic clinics, Private medical clinics, Beauty salons, Real estate agencies
- Budget: €10K+ 
- Timeline: Ready to start within 3 months
- Clear use case: Client intake, booking automation, CRM optimization, marketing automation, or customer service

SCORING CRITERIA:
1. Industry Fit (40%):
   - Wellness & Fitness Studios (gyms, yoga, wellness centers): 100
   - Aesthetic Clinics (cosmetic, dermatology): 95
   - Private Medical Clinics (general practice, specialists): 95
   - Hairdressers & Beauty Salons (hair, nails, spa): 90
   - Real Estate Agencies (residential, commercial): 85
   - Other service businesses (hospitality, professional services): 70
   - Retail, e-commerce: 60
   - Manufacturing, pure tech companies: 50

2. Budget Alignment (25%):
   - €50K+: 100
   - €25K-€50K: 90
   - €10K-€25K: 75
   - €5K-€10K: 50
   - <€5K or "Not sure": 25

3. Timeline Urgency (20%):
   - Immediately: 100
   - 1-3 months: 80
   - 3-6 months: 60
   - 6+ months: 40
   - "Not sure": 30

4. Needs Clarity (15%):
   - Specific AI use case with clear pain point: 100
   - General operational challenge, exploring AI: 75
   - Vague interest or "learning about AI": 50
   - No clear use case: 25

ROUTING RULES:
- Score 70-100: "Outreach Sent" (High Priority) - Ready for immediate personalized outreach
- Score 40-69: "Lead" (Medium Priority) - Qualified but needs nurturing
- Score 0-39: "Lead" + tag "Low Fit - Nurture" - Educational content, long-term nurture

OUTPUT FORMAT:
Return valid JSON only, no markdown formatting or explanation outside the JSON.
"""

QUALIFICATION_USER_PROMPT_TEMPLATE = """Analyze this lead submission and provide a qualification score.

LEAD DATA:
- Name: {full_name}
- Company: {company_name}
- Industry: {industry}
- Budget Range: {budget_range}
- Timeline: {timeline}
- Needs Description: {needs}

Please analyze this lead and provide your assessment in the following JSON format:

{{
  "overall_score": <0-100>,
  "scores": {{
    "industry_fit": <0-100>,
    "budget_alignment": <0-100>,
    "timeline_urgency": <0-100>,
    "needs_clarity": <0-100>
  }},
  "reasoning": "<2-3 sentence explanation of the score>",
  "recommended_stage": "<Outreach Sent|Lead|Lead (Low Fit)>",
  "key_insights": ["<insight 1>", "<insight 2>"],
  "suggested_next_action": "<specific action for Lucas>",
  "suggested_use_case": "<AI use case that fits their needs>"
}}

Ensure the output is valid JSON without any markdown code blocks or additional text."""


def calculate_qualification_score(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call Claude API to analyze lead and generate qualification score.
    
    Args:
        lead_data: Dictionary containing form submission data
        
    Returns:
        Dictionary with qualification scores and recommendations
    """
    
    # Format the prompt with lead data
    user_prompt = QUALIFICATION_USER_PROMPT_TEMPLATE.format(
        full_name=lead_data.get("full_name", ""),
        company_name=lead_data.get("company_name", ""),
        industry=lead_data.get("industry", ""),
        budget_range=lead_data.get("budget_range", ""),
        timeline=lead_data.get("timeline", ""),
        needs=lead_data.get("needs", "")
    )
    
    # Call Claude API directly via requests (more reliable in serverless environments)
    try:
        resp = requests.post(
            ANTHROPIC_API_URL,
            headers={
                "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 1000,
                "system": QUALIFICATION_SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": user_prompt}]
            },
            timeout=50
        )
        resp.raise_for_status()
        data = resp.json()

        # Extract response text
        response_text = data["content"][0]["text"]

        # Remove markdown code blocks if present
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        qualification_result = json.loads(response_text)

        # Recalculate overall_score from sub-scores using the defined weights.
        # The LLM estimates sub-scores well but its rollup arithmetic drifts;
        # doing it here keeps the number deterministic and consistent.
        s = qualification_result["scores"]
        qualification_result["overall_score"] = round(
            s["industry_fit"]     * 0.40 +
            s["budget_alignment"] * 0.25 +
            s["timeline_urgency"] * 0.20 +
            s["needs_clarity"]    * 0.15
        )

        # Re-derive routing stage from the recalculated score.
        score = qualification_result["overall_score"]
        if score >= 70:
            qualification_result["recommended_stage"] = "Outreach Sent"
        elif score >= 40:
            qualification_result["recommended_stage"] = "Lead"
        else:
            qualification_result["recommended_stage"] = "Lead (Low Fit)"

        # Add API usage metadata
        qualification_result["api_usage"] = {
            "input_tokens": data["usage"]["input_tokens"],
            "output_tokens": data["usage"]["output_tokens"],
            "model": data["model"]
        }

        return qualification_result

    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse Claude response as JSON: {e}\nResponse: {response_text}")
    except Exception as e:
        raise RuntimeError(f"Error calling Claude API: {e}")


def map_stage_to_hubspot_stage(recommended_stage: str) -> str:
    """
    Map qualification stage to HubSpot pipeline stage ID.
    
    Args:
        recommended_stage: Stage from qualification ("Outreach Sent", "Lead", etc.)
        
    Returns:
        HubSpot stage identifier
    """
    stage_mapping = {
        "Outreach Sent": "5198127292",
        "Lead": "5198127291",
        "Lead (Low Fit)": "5198127291"
    }
    return stage_mapping.get(recommended_stage, "lead")


def format_for_hubspot(lead_data: Dict[str, Any], qualification: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format qualification results for HubSpot API.
    
    Args:
        lead_data: Original form submission data
        qualification: Qualification results from Claude
        
    Returns:
        Dictionary formatted for HubSpot contact/deal creation
    """
    
    # Split name into first/last
    name_parts = lead_data.get("full_name", "").split(" ", 1)
    first_name = name_parts[0] if len(name_parts) > 0 else ""
    last_name = name_parts[1] if len(name_parts) > 1 else ""
    
    return {
        "contact": {
            "email": lead_data.get("email"),
            "firstname": first_name,
            "lastname": last_name,
            "phone": lead_data.get("phone"),
            "company": lead_data.get("company_name"),
            "industry": lead_data.get("industry"),
            "hs_lead_status": "NEW",
            "kairos_budget_range": lead_data.get("budget_range"),
            "kairos_timeline": lead_data.get("timeline"),
            "kairos_needs_summary": lead_data.get("needs"),
            "kairos_lead_source": "Website Contact Form",
            "kairos_qualification_score": str(qualification["overall_score"]),
            "kairos_industry_fit_score": str(qualification["scores"]["industry_fit"]),
            "kairos_budget_fit_score": str(qualification["scores"]["budget_alignment"]),
            "kairos_timeline_urgency": str(qualification["scores"]["timeline_urgency"]),
            "kairos_needs_clarity": str(qualification["scores"]["needs_clarity"])
        },
        "deal": {
            "dealname": f"{lead_data.get('company_name', 'Unknown')} - {qualification.get('suggested_use_case', 'AI Consulting')}",
            "dealstage": map_stage_to_hubspot_stage(qualification["recommended_stage"]),
            "pipeline": "kairos_sales_pipeline",
            "amount": "15000",  # Default estimate, adjust based on budget
            "kairos_qualification_score": str(qualification["overall_score"]),
            "kairos_key_insights": "; ".join(qualification.get("key_insights", [])),
            "kairos_suggested_use_case": qualification.get("suggested_use_case", ""),
            "kairos_lead_source": "Website Contact Form",
            "kairos_reasoning": qualification.get("reasoning", "")
        }
    }


def format_for_slack(lead_data: Dict[str, Any], qualification: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format notification for Slack webhook.
    
    Args:
        lead_data: Original form submission data
        qualification: Qualification results from Claude
        
    Returns:
        Dictionary formatted for Slack webhook
    """
    
    # Determine emoji based on score
    score = qualification["overall_score"]
    if score >= 70:
        emoji = "🎯"
        priority = "High-Priority"
    elif score >= 40:
        emoji = "📊"
        priority = "Medium-Priority"
    else:
        emoji = "📋"
        priority = "Low-Priority"
    
    return {
        "text": f"New qualified lead: {lead_data.get('full_name', 'Unknown')} (Score: {score}/100)",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} New {priority} Lead",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Name:*\n{lead_data.get('full_name', 'Unknown')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Company:*\n{lead_data.get('company_name', 'Unknown')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Industry:*\n{lead_data.get('industry', 'Unknown')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Score:*\n{score}/100 {'⭐' if score >= 70 else ''}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Key Insights:*\n" + "\n".join([f"• {insight}" for insight in qualification.get("key_insights", [])])
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Suggested Next Action:*\n{qualification.get('suggested_next_action', 'Review and reach out')}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Reasoning:*\n{qualification.get('reasoning', 'See full details in HubSpot')}"
                }
            }
        ]
    }


def process_lead_submission(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function to process a lead submission.
    
    Args:
        lead_data: Dictionary containing form submission data
        
    Returns:
        Complete processing result with qualification and formatted outputs
    """
    
    # Step 1: Qualify the lead
    print(f"📊 Qualifying lead: {lead_data.get('full_name')} from {lead_data.get('company_name')}")
    qualification = calculate_qualification_score(lead_data)
    
    print(f"✅ Qualification complete. Score: {qualification['overall_score']}/100")
    print(f"   Stage: {qualification['recommended_stage']}")
    
    # Step 2: Format for HubSpot
    hubspot_data = format_for_hubspot(lead_data, qualification)
    
    # Step 3: Format for Slack
    slack_notification = format_for_slack(lead_data, qualification)
    
    # Return complete result
    return {
        "lead_data": lead_data,
        "qualification": qualification,
        "hubspot": hubspot_data,
        "slack": slack_notification
    }


# Example usage (for testing)
if __name__ == "__main__":
    # Test with sample lead
    sample_lead = {
        "full_name": "Maria Schmidt",
        "email": "maria@fitlife-berlin.de",
        "phone": "+49 30 555 0000",
        "company_name": "FitLife Studios GmbH",
        "industry": "Wellness & Fitness Studios",
        "budget_range": "€10K-€25K",
        "timeline": "1-3 months",
        "needs": "We have 5 fitness studios in Berlin and spend too much time manually responding to customer inquiries about class schedules, memberships, and trainer availability. We'd like to explore AI chatbots to automate routine questions and free up our staff for more valuable interactions."
    }
    
    # Process the lead
    result = process_lead_submission(sample_lead)
    
    # Print results
    print("\n" + "="*80)
    print("QUALIFICATION RESULT")
    print("="*80)
    print(json.dumps(result, indent=2))
