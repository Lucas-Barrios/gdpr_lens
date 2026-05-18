"""
Quick validation test for the Kairos Lead Qualification Agent.
Tests a single high-priority lead (wellness studio) to confirm the agent is working.
"""

import os
import json
from dotenv import load_dotenv
from lead_qualification_agent import process_lead_submission

load_dotenv()

if not os.getenv("ANTHROPIC_API_KEY"):
    print("ERROR: ANTHROPIC_API_KEY is not set.")
    print("Set it with:  export ANTHROPIC_API_KEY=sk-ant-...")
    exit(1)

lead = {
    "full_name": "Maria Schmidt",
    "email": "maria@fitlife-berlin.de",
    "phone": "+49 30 555 0000",
    "company_name": "FitLife Studios GmbH",
    "industry": "Wellness & Fitness Studios",
    "budget_range": "€10K-€25K",
    "timeline": "Immediately",
    "needs": (
        "We have 5 fitness studios in Berlin and spend too much time manually responding "
        "to customer inquiries about class schedules, memberships, and trainer availability. "
        "Need AI chatbot to automate routine questions and free up staff."
    ),
}

print("Running quick validation test...")
print(f"Lead: {lead['full_name']} — {lead['company_name']} ({lead['industry']})")
print()

result = process_lead_submission(lead)
q = result["qualification"]

print()
print("=" * 60)
print("RESULT")
print("=" * 60)
print(f"Overall Score : {q['overall_score']}/100")
print(f"Stage         : {q['recommended_stage']}")
print(f"Industry Fit  : {q['scores']['industry_fit']}/100")
print(f"Budget        : {q['scores']['budget_alignment']}/100")
print(f"Timeline      : {q['scores']['timeline_urgency']}/100")
print(f"Needs Clarity : {q['scores']['needs_clarity']}/100")
print()
print(f"Reasoning: {q['reasoning']}")
print()
print("Key Insights:")
for insight in q.get("key_insights", []):
    print(f"  - {insight}")
print()
print(f"Suggested Action: {q.get('suggested_next_action', '')}")
print(f"Suggested Use Case: {q.get('suggested_use_case', '')}")
print()

# Simple pass/fail: expect score >= 85 and stage = "Outreach Sent"
expected_min = 80
stage_ok = q["recommended_stage"] == "Outreach Sent"
score_ok = q["overall_score"] >= expected_min

if score_ok and stage_ok:
    print(f"PASS — Score {q['overall_score']} >= {expected_min} and stage is 'Outreach Sent'")
else:
    issues = []
    if not score_ok:
        issues.append(f"score {q['overall_score']} < {expected_min}")
    if not stage_ok:
        issues.append(f"stage '{q['recommended_stage']}' != 'Outreach Sent'")
    print(f"FAIL — {', '.join(issues)}")
