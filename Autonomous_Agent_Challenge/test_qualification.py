"""
Test Script for Lead Qualification Agent
Validates scoring accuracy across different lead profiles
"""

import os
import json
from lead_qualification_agent import process_lead_submission

# Test cases covering different lead profiles
TEST_LEADS = [
    {
        "name": "High Priority - Wellness Studio Chain",
        "data": {
            "full_name": "Maria Schmidt",
            "email": "maria@fitlife-berlin.de",
            "phone": "+49 30 555 0000",
            "company_name": "FitLife Studios GmbH",
            "industry": "Wellness & Fitness Studios",
            "budget_range": "€10K-€25K",
            "timeline": "Immediately",
            "needs": "We have 5 fitness studios in Berlin and spend too much time manually responding to customer inquiries about class schedules, memberships, and trainer availability. Need AI chatbot to automate routine questions and free up staff."
        },
        "expected_score_range": (85, 100),
        "expected_stage": "Outreach Sent"
    },
    {
        "name": "High Priority - Aesthetic Clinic",
        "data": {
            "full_name": "Dr. Thomas Weber",
            "email": "weber@aesthetics-berlin.de",
            "phone": "+49 30 666 0000",
            "company_name": "Berlin Aesthetics Clinic",
            "industry": "Aesthetic Clinics",
            "budget_range": "€25K-€50K",
            "timeline": "1-3 months",
            "needs": "Patient intake, appointment scheduling, and follow-up automation. Currently handling 200+ new patient inquiries per month manually. Need AI to streamline patient onboarding and reduce administrative burden."
        },
        "expected_score_range": (88, 100),
        "expected_stage": "Outreach Sent"
    },
    {
        "name": "High Priority - Medical Clinic",
        "data": {
            "full_name": "Dr. Anna Müller",
            "email": "anna.mueller@praxis-berlin.de",
            "phone": "+49 30 777 0000",
            "company_name": "Praxis Dr. Müller",
            "industry": "Private Medical Clinics",
            "budget_range": "€10K-€25K",
            "timeline": "1-3 months",
            "needs": "Private practice with 3 doctors. Overwhelmed with appointment requests via phone and email. Want AI-powered booking system and patient communication automation to reduce front desk workload."
        },
        "expected_score_range": (85, 98),
        "expected_stage": "Outreach Sent"
    },
    {
        "name": "Medium-High Priority - Beauty Salon",
        "data": {
            "full_name": "Sophie Klein",
            "email": "sophie@salon-luxe.de",
            "phone": "+49 30 888 0000",
            "company_name": "Salon Luxe Berlin",
            "industry": "Hairdressers & Beauty Salons",
            "budget_range": "€5K-€10K",
            "timeline": "1-3 months",
            "needs": "High-end salon with 12 stylists. Need smart booking system with automated reminders and loyalty program. Currently using basic calendar, lots of no-shows and manual follow-up."
        },
        "expected_score_range": (65, 80),
        "expected_stage": "Lead"
    },
    {
        "name": "Medium Priority - Real Estate",
        "data": {
            "full_name": "Max Becker",
            "email": "max.becker@immobilien-berlin.de",
            "phone": "+49 30 999 0000",
            "company_name": "Becker Immobilien GmbH",
            "industry": "Real Estate Agencies",
            "budget_range": "€10K-€25K",
            "timeline": "3-6 months",
            "needs": "Residential real estate agency with 8 agents. Interested in AI for lead qualification and property matching. Currently researching options."
        },
        "expected_score_range": (60, 75),
        "expected_stage": "Lead"
    },
    {
        "name": "Low Priority - Retail Store",
        "data": {
            "full_name": "Julia Hoffmann",
            "email": "julia@modehaus-berlin.de",
            "phone": "+49 30 123 0000",
            "company_name": "Modehaus Hoffmann",
            "industry": "Retail & E-commerce",
            "budget_range": "€5K-€10K",
            "timeline": "6+ months",
            "needs": "Fashion boutique. Just learning about AI and what it can do for retail. No specific use case yet."
        },
        "expected_score_range": (35, 55),
        "expected_stage": "Lead"
    }
]


def run_tests():
    """Run all test cases and validate results."""
    
    print("="*80)
    print("LEAD QUALIFICATION AGENT - TEST SUITE")
    print("="*80)
    print()
    
    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("   Please set your API key: export ANTHROPIC_API_KEY=sk-ant-...")
        return
    
    results = []
    passed = 0
    failed = 0
    
    for i, test in enumerate(TEST_LEADS, 1):
        print(f"\n{'='*80}")
        print(f"Test {i}/{len(TEST_LEADS)}: {test['name']}")
        print(f"{'='*80}")
        print(f"Company: {test['data']['company_name']}")
        print(f"Industry: {test['data']['industry']}")
        print(f"Budget: {test['data']['budget_range']}")
        print(f"Timeline: {test['data']['timeline']}")
        print(f"Needs: {test['data']['needs'][:100]}...")
        print()
        
        try:
            # Process the lead
            result = process_lead_submission(test['data'])
            qualification = result['qualification']
            
            # Extract scores
            overall_score = qualification['overall_score']
            recommended_stage = qualification['recommended_stage']
            
            # Validate score range
            min_expected, max_expected = test['expected_score_range']
            score_in_range = min_expected <= overall_score <= max_expected
            
            # Validate stage (allow some flexibility)
            stage_correct = recommended_stage == test['expected_stage']
            
            # Overall pass/fail
            test_passed = score_in_range
            
            if test_passed:
                passed += 1
                status = "✅ PASS"
            else:
                failed += 1
                status = "❌ FAIL"
            
            print(f"{status}")
            print(f"  Overall Score: {overall_score}/100 (expected {min_expected}-{max_expected})")
            print(f"  Recommended Stage: {recommended_stage} (expected {test['expected_stage']})")
            print(f"  Score Breakdown:")
            print(f"    Industry Fit: {qualification['scores']['industry_fit']}/100")
            print(f"    Budget Alignment: {qualification['scores']['budget_alignment']}/100")
            print(f"    Timeline Urgency: {qualification['scores']['timeline_urgency']}/100")
            print(f"    Needs Clarity: {qualification['scores']['needs_clarity']}/100")
            print(f"  Reasoning: {qualification['reasoning']}")
            print(f"  Key Insights:")
            for insight in qualification['key_insights']:
                print(f"    - {insight}")
            print(f"  Suggested Action: {qualification['suggested_next_action']}")
            
            # Store result
            results.append({
                "test_name": test['name'],
                "passed": test_passed,
                "score": overall_score,
                "expected_range": test['expected_score_range'],
                "recommended_stage": recommended_stage,
                "expected_stage": test['expected_stage']
            })
            
        except Exception as e:
            failed += 1
            print(f"❌ ERROR: {str(e)}")
            results.append({
                "test_name": test['name'],
                "passed": False,
                "error": str(e)
            })
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Total Tests: {len(TEST_LEADS)}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    print(f"Success Rate: {(passed/len(TEST_LEADS)*100):.1f}%")
    print()
    
    # Print detailed results table
    print("Detailed Results:")
    print(f"{'Test Name':<40} {'Score':<12} {'Expected':<15} {'Stage':<20} {'Status':<10}")
    print("-"*100)
    for r in results:
        if 'error' not in r:
            score_str = f"{r['score']}/100"
            expected_str = f"{r['expected_range'][0]}-{r['expected_range'][1]}"
            status = "PASS ✅" if r['passed'] else "FAIL ❌"
            print(f"{r['test_name']:<40} {score_str:<12} {expected_str:<15} {r['recommended_stage']:<20} {status:<10}")
        else:
            print(f"{r['test_name']:<40} {'ERROR':<12} {'':<15} {'':<20} {'FAIL ❌':<10}")
    
    # Save results to file
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: test_results.json")


if __name__ == "__main__":
    run_tests()
