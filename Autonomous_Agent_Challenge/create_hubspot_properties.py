"""
Creates all Kairos custom properties in HubSpot (contacts + deals).
Run once. Safe to re-run — skips properties that already exist.

Usage:
    HUBSPOT_TOKEN=pat-eu1-xxx python3 create_hubspot_properties.py
"""

import os
import sys
import requests

TOKEN = os.getenv("HUBSPOT_TOKEN")
if not TOKEN:
    print("ERROR: Set HUBSPOT_TOKEN environment variable first.")
    print("  export HUBSPOT_TOKEN=pat-eu1-your-token-here")
    sys.exit(1)

BASE_URL = "https://api.hubapi.com/crm/v3/properties"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

GROUP_NAME = "kairos_ai_scoring"

CONTACT_PROPERTIES = [
    {"name": "kairos_qualification_score",  "label": "AI Qualification Score",  "type": "number",  "fieldType": "number"},
    {"name": "kairos_industry_fit_score",   "label": "Industry Fit Score",       "type": "number",  "fieldType": "number"},
    {"name": "kairos_budget_fit_score",     "label": "Budget Fit Score",         "type": "number",  "fieldType": "number"},
    {"name": "kairos_timeline_urgency",     "label": "Timeline Urgency Score",   "type": "number",  "fieldType": "number"},
    {"name": "kairos_needs_clarity",        "label": "Needs Clarity Score",      "type": "number",  "fieldType": "number"},
    {"name": "kairos_budget_range",         "label": "Budget Range",             "type": "string",  "fieldType": "text"},
    {"name": "kairos_timeline",             "label": "Timeline to Start",        "type": "string",  "fieldType": "text"},
    {"name": "kairos_needs_summary",        "label": "Needs Summary",            "type": "string",  "fieldType": "textarea"},
    {"name": "kairos_lead_source",          "label": "Kairos Lead Source",       "type": "string",  "fieldType": "text"},
]

DEAL_PROPERTIES = [
    {"name": "kairos_qualification_score",  "label": "AI Qualification Score",  "type": "number",  "fieldType": "number"},
    {"name": "kairos_key_insights",         "label": "Key Insights",             "type": "string",  "fieldType": "textarea"},
    {"name": "kairos_suggested_use_case",   "label": "Suggested Use Case",       "type": "string",  "fieldType": "text"},
    {"name": "kairos_lead_source",          "label": "Kairos Lead Source",       "type": "string",  "fieldType": "text"},
    {"name": "kairos_reasoning",            "label": "AI Reasoning",             "type": "string",  "fieldType": "textarea"},
]


def ensure_group(object_type: str):
    url = f"{BASE_URL}/{object_type}/groups"
    resp = requests.post(url, headers=HEADERS, json={
        "name": GROUP_NAME,
        "label": "Kairos AI Scoring",
        "displayOrder": 1
    })
    if resp.status_code == 409:
        print(f"  [skip] group '{GROUP_NAME}' already exists on {object_type}")
    elif resp.status_code in (200, 201):
        print(f"  [ok]   created group '{GROUP_NAME}' on {object_type}")
    else:
        print(f"  [warn] group creation returned {resp.status_code}: {resp.text}")


def create_property(object_type: str, prop: dict):
    url = f"{BASE_URL}/{object_type}"
    resp = requests.post(url, headers=HEADERS, json={
        "name": prop["name"],
        "label": prop["label"],
        "type": prop["type"],
        "fieldType": prop["fieldType"],
        "groupName": GROUP_NAME,
    })
    if resp.status_code == 409:
        print(f"  [skip] {prop['name']} already exists")
    elif resp.status_code in (200, 201):
        print(f"  [ok]   {prop['name']}")
    else:
        print(f"  [fail] {prop['name']}: {resp.status_code} {resp.text}")


def main():
    print("\n=== Contacts ===")
    ensure_group("contacts")
    for p in CONTACT_PROPERTIES:
        create_property("contacts", p)

    print("\n=== Deals ===")
    ensure_group("deals")
    for p in DEAL_PROPERTIES:
        create_property("deals", p)

    print("\nDone. Refresh HubSpot → Contact/Deal record to see the new fields.")


if __name__ == "__main__":
    main()
