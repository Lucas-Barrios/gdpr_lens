# Deployment Plan & Operations Runbook
## Kairos Consulting Lead Generation System

**Created:** May 18, 2026  
**Version:** 1.0  

---

## 1. Deployment Architecture

### Phase 1 Architecture

```
┌─────────────────┐
│ Kairos Website  │
│ (Vercel)        │
└────────┬────────┘
         │ POST /webhook/lead-intake
         ▼
┌─────────────────┐
│ n8n Cloud       │  ◄──── Primary orchestrator
│ or Self-Hosted  │
└────────┬────────┘
         │
         ├──────► Anthropic API (Claude 3.5 Sonnet)
         │
         ├──────► HubSpot API (CRM updates)
         │
         ├──────► Slack Webhook (notifications)
         │
         └──────► Supabase (lead history storage)
```

### Hosting Options

**Option A: Full Cloud (Recommended for MVP)**
- n8n: n8n Cloud ($20/month)
- Supabase: Free tier
- Benefits: Zero DevOps, automatic backups, SSL included
- Drawbacks: Monthly cost, vendor lock-in

**Option B: Self-Hosted (Cost-Optimized)**
- n8n: Docker on Hetzner VPS (€4.5/month for CX11)
- Supabase: Self-hosted on same VPS
- Benefits: Lower cost, full control
- Drawbacks: Requires DevOps knowledge, maintenance burden

**Option C: Hybrid (Recommended for Production)**
- n8n: n8n Cloud (managed workflows)
- Supabase: Self-hosted (data control)
- Benefits: Balance of convenience and cost
- Drawbacks: Split infrastructure

---

## 2. Environment Setup

### Development Environment

```bash
# Create project directory
mkdir kairos-lead-gen
cd kairos-lead-gen

# Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install langchain anthropic python-dotenv requests

# Create .env file
cat > .env << EOF
ANTHROPIC_API_KEY=sk-ant-...
HUBSPOT_API_KEY=pat-na1-...
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGciOiJ...
N8N_WEBHOOK_URL=https://your-instance.app.n8n.cloud/webhook/lead-intake
EOF

# Create directory structure
mkdir -p {workflows,scripts,tests,docs}
```

### Production Environment (n8n Cloud)

1. Sign up at https://n8n.io
2. Create new workflow
3. Add environment variables:
   - `ANTHROPIC_API_KEY`
   - `HUBSPOT_API_KEY`
   - `SLACK_WEBHOOK_URL`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`

---

## 3. Deployment Checklist

### Pre-Deployment

**Infrastructure:**
- [ ] n8n instance running and accessible
- [ ] Supabase project created
- [ ] HubSpot custom properties created (see API contracts doc)
- [ ] Slack webhook configured
- [ ] Anthropic API key obtained and tested

**Configuration:**
- [ ] All environment variables set
- [ ] Webhook endpoint secured (HTTPS, signature verification)
- [ ] Rate limits configured
- [ ] Error notifications enabled

**Testing:**
- [ ] Test form submission end-to-end
- [ ] Verify HubSpot contact/deal creation
- [ ] Confirm Slack notifications working
- [ ] Validate scoring logic with 5 test cases
- [ ] Load test webhook (50 concurrent requests)

### Deployment Steps

**Step 1: Deploy n8n Workflow**
1. Import workflow JSON
2. Activate workflow
3. Test webhook endpoint with curl
4. Monitor first 5 real submissions

**Step 2: Connect Website Form**
1. Update form action URL to n8n webhook
2. Deploy to Vercel staging
3. Test form submission
4. Deploy to production

**Step 3: Monitor & Validate**
1. Watch first 20 leads process
2. Compare agent scores vs manual assessment
3. Adjust scoring weights if needed
4. Enable Slack alerts for errors

### Post-Deployment

- [ ] Document workflow for team
- [ ] Set up monitoring dashboard
- [ ] Schedule weekly review meetings
- [ ] Create incident response plan

---

## 4. Monitoring & Logging

### Key Metrics to Track

**Operational Metrics:**
- Webhook response time (target: <2s)
- API success rate (target: >99%)
- End-to-end processing time (target: <2 min)
- Error rate (target: <1%)

**Business Metrics:**
- Leads processed per day
- Average qualification score
- Distribution by pipeline stage (high/med/low)
- Time saved vs manual process

### Monitoring Stack

**Option A: Built-in Tools (Free)**
- n8n execution logs
- Slack error notifications
- Weekly manual review

**Option B: Advanced Monitoring**
- Sentry for error tracking (€26/month)
- Datadog for metrics (€15/month)
- Grafana for dashboards (self-hosted, free)

### Log Retention

- n8n execution history: 30 days (n8n Cloud free tier)
- Supabase logs: 7 days (free tier)
- Error logs to Slack: permanent
- Monthly aggregated reports: permanent (Google Sheets)

---

## 5. Alerting Rules

### Critical Alerts (Immediate Response)

**Trigger:** Webhook down for >5 minutes  
**Action:** Page Lucas via SMS  
**SLA:** Respond within 15 minutes  

**Trigger:** Error rate >10% over 1 hour  
**Action:** Slack @lucas notification  
**SLA:** Investigate within 1 hour  

**Trigger:** No leads processed in 24 hours (during business days)  
**Action:** Email Lucas  
**SLA:** Check within 4 hours  

### Warning Alerts (Daily Review)

**Trigger:** API costs >€10/day  
**Action:** Daily Slack summary  
**SLA:** Review next morning  

**Trigger:** Average score <50 for >10 leads  
**Action:** Slack notification  
**SLA:** Review scoring logic within 24 hours  

**Trigger:** HubSpot rate limit hit  
**Action:** Slack notification  
**SLA:** Add queue/backoff logic within 48 hours  

### Alert Configuration (Slack Webhook)

```python
import requests
import os

def send_alert(severity: str, title: str, message: str, context: dict = None):
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    
    color_map = {
        'critical': '#FF0000',
        'warning': '#FFA500',
        'info': '#0000FF'
    }
    
    payload = {
        'attachments': [{
            'color': color_map.get(severity, '#808080'),
            'title': f'[{severity.upper()}] {title}',
            'text': message,
            'fields': [
                {'title': k, 'value': str(v), 'short': True}
                for k, v in (context or {}).items()
            ],
            'footer': 'Kairos Lead Gen System',
            'ts': int(time.time())
        }]
    }
    
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()
```

---

## 6. Backup & Recovery

### Data Backup Strategy

**Supabase Database:**
- Automatic daily backups (Supabase managed)
- Point-in-time recovery available
- Manual exports weekly to Google Drive
- Backup retention: 30 days

**n8n Workflows:**
- Export workflow JSON daily
- Store in GitHub private repo
- Version control all changes
- Backup retention: unlimited (Git history)

**HubSpot Data:**
- Native HubSpot backups
- Weekly export of custom properties
- No additional backup needed

### Backup Script

```bash
#!/bin/bash
# backup.sh - Run daily via cron

DATE=$(date +%Y-%m-%d)
BACKUP_DIR="$HOME/backups/kairos-lead-gen"

mkdir -p "$BACKUP_DIR"

# Export Supabase data
psql $SUPABASE_URL -c "COPY (SELECT * FROM prospects) TO STDOUT CSV HEADER" > "$BACKUP_DIR/prospects_$DATE.csv"

# Export n8n workflow (if self-hosted)
# curl -u admin:password http://n8n:5678/rest/workflows/1 > "$BACKUP_DIR/workflow_$DATE.json"

# Upload to Google Drive
rclone copy "$BACKUP_DIR" remote:kairos-backups/

# Clean old backups (keep last 30 days)
find "$BACKUP_DIR" -type f -mtime +30 -delete
```

### Recovery Procedures

**Scenario 1: n8n Workflow Corrupted**
1. Deactivate current workflow
2. Import latest backup from GitHub
3. Test with sample payload
4. Reactivate workflow
5. **RTO:** 15 minutes

**Scenario 2: Supabase Data Loss**
1. Contact Supabase support for point-in-time recovery
2. Restore from most recent daily backup
3. Verify data integrity
4. Resume operations
5. **RTO:** 2 hours, **RPO:** 24 hours

**Scenario 3: Complete Infrastructure Failure**
1. Spin up new n8n instance (n8n Cloud or VPS)
2. Import workflow from GitHub
3. Configure environment variables
4. Update webhook URL in website
5. Deploy and test
6. **RTO:** 4 hours

---

## 7. Rollback Procedures

### Rollback Triggers

- Error rate >20% sustained for >1 hour
- Data corruption detected in HubSpot
- Critical bug in scoring logic
- API cost spike (>€50/day)

### Rollback Steps

**Step 1: Pause Automation**
```bash
# Deactivate n8n workflow immediately
curl -X PATCH https://n8n-instance/api/v1/workflows/1/active \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"active": false}'
```

**Step 2: Revert to Manual Process**
1. Update website form to send to Lucas's email
2. Lucas manually processes leads in HubSpot
3. Document all manual entries for later bulk processing

**Step 3: Root Cause Analysis**
1. Review error logs
2. Identify breaking change
3. Fix in development environment
4. Test with 10 sample leads

**Step 4: Controlled Re-deployment**
1. Deploy fix to staging
2. Test for 24 hours
3. Gradually re-enable (10% → 50% → 100% of traffic)
4. Monitor closely for 48 hours

---

## 8. Incident Response Plan

### Severity Levels

**P0 - Critical:**
- System completely down
- Data loss or corruption
- Security breach
- **Response time:** Immediate
- **Resolution SLA:** 4 hours

**P1 - High:**
- Partial functionality loss
- Error rate >10%
- API cost spike
- **Response time:** 1 hour
- **Resolution SLA:** 24 hours

**P2 - Medium:**
- Degraded performance
- Non-critical feature broken
- Monitoring alerts
- **Response time:** 4 hours
- **Resolution SLA:** 72 hours

**P3 - Low:**
- Minor bugs
- Enhancement requests
- Documentation updates
- **Response time:** Next business day
- **Resolution SLA:** 2 weeks

### Incident Response Workflow

```
┌─────────────┐
│ Alert fired │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Create incident  │
│ ticket in Notion │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐      ┌──────────────┐
│ Assess severity  │─────►│ P0/P1: Page  │
└──────┬───────────┘      │ Lucas via SMS│
       │                  └──────────────┘
       ▼
┌──────────────────┐
│ Investigate root │
│ cause            │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Implement fix    │
│ or rollback      │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Verify resolved  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Post-mortem doc  │
│ + preventions    │
└──────────────────┘
```

### Incident Log Template

```markdown
# Incident Report: [Brief Title]

**Severity:** P0/P1/P2/P3  
**Status:** Investigating / Mitigated / Resolved  
**Started:** 2026-05-18 14:32 UTC  
**Resolved:** 2026-05-18 16:45 UTC  
**Duration:** 2h 13m  

## Impact
- X leads not processed
- Y hours of downtime
- €Z in potential lost opportunities

## Timeline
- 14:32 - Alert fired: "Webhook 500 errors"
- 14:35 - Lucas notified via Slack
- 14:42 - Investigation started
- 15:10 - Root cause identified: Anthropic API key expired
- 15:15 - New API key generated and deployed
- 15:20 - Workflow reactivated
- 16:45 - Monitoring confirms full recovery

## Root Cause
Anthropic API key expired after 90 days. No automated renewal process in place.

## Resolution
1. Generated new API key
2. Updated n8n environment variables
3. Reactivated workflow
4. Manually processed 8 leads that failed during outage

## Prevention
- [ ] Set up API key expiration monitoring (30 days before)
- [ ] Document API key rotation procedure
- [ ] Add to quarterly maintenance checklist
- [ ] Consider using rotating keys with longer expiration
```

---

## 9. Maintenance Schedule

### Daily Tasks (Automated)

- [ ] Health check ping (n8n cron: 9 AM CET)
- [ ] Backup n8n workflow to GitHub
- [ ] Export Supabase data to Google Drive
- [ ] Cost tracking update (API usage)

### Weekly Tasks (Manual - 30 min)

- [ ] Review error logs
- [ ] Spot-check 5 random leads for scoring accuracy
- [ ] Update cost tracking spreadsheet
- [ ] Review and archive Slack alerts

### Monthly Tasks (Manual - 2 hours)

- [ ] Generate performance report
- [ ] Review and optimize API costs
- [ ] Update scoring weights if needed
- [ ] Security audit (check for exposed credentials)
- [ ] Dependency updates (Python packages, n8n version)

### Quarterly Tasks (Manual - 4 hours)

- [ ] Full system audit
- [ ] Load testing (simulate 500 leads/hour)
- [ ] Review and update documentation
- [ ] Competitive analysis (new tools/APIs)
- [ ] Cost-benefit analysis and ROI calculation

---

## 10. Operations Runbook

### Common Issues & Solutions

#### Issue: Webhook returning 500 errors

**Symptoms:** Slack alerts showing "Webhook 500 errors", form submissions not reaching HubSpot

**Diagnosis:**
```bash
# Check n8n workflow status
curl https://n8n-instance/api/v1/workflows/1

# Check recent executions
curl https://n8n-instance/api/v1/executions?workflowId=1&limit=10

# Test webhook directly
curl -X POST https://n8n-instance/webhook/lead-intake \
  -H "Content-Type: application/json" \
  -d @test_payload.json
```

**Resolution:**
1. Check n8n execution log for error message
2. Common causes:
   - API key expired → Renew key
   - Rate limit hit → Add backoff logic
   - Invalid payload → Fix validation
3. Redeploy workflow
4. Test with sample payload

**Prevention:**
- Set up API key expiration monitoring
- Implement circuit breaker for rate limits
- Add payload validation at webhook entry

---

#### Issue: Leads scoring incorrectly (consistent low/high scores)

**Symptoms:** All leads scoring 90+ or all scoring <40, not matching manual assessment

**Diagnosis:**
```bash
# Pull last 10 leads from Supabase
psql $SUPABASE_URL -c "SELECT * FROM leads ORDER BY created_at DESC LIMIT 10"

# Compare agent scores vs manual assessment
# Check if specific industry/budget causing bias
```

**Resolution:**
1. Review scoring prompt in n8n
2. Adjust weights if needed:
   - Industry fit: 40%
   - Budget: 25%
   - Timeline: 20%
   - Needs clarity: 15%
3. Test with 10 sample leads
4. Deploy updated prompt
5. Monitor next 20 leads for improvement

**Prevention:**
- Monthly scoring accuracy review
- A/B test scoring variations
- Collect feedback from sales team

---

#### Issue: High API costs (>€50/day)

**Symptoms:** Daily cost alerts, Anthropic usage spike

**Diagnosis:**
```bash
# Check Anthropic dashboard for token usage
# Review n8n execution count
curl https://n8n-instance/api/v1/executions?limit=100

# Calculate tokens per lead
total_tokens / total_leads
```

**Resolution:**
1. Identify cause:
   - Traffic spike → Expected, monitor
   - Inefficient prompts → Optimize
   - Retry loops → Fix error handling
   - Duplicate executions → Debug n8n
2. Immediate mitigation:
   - Reduce max_tokens if possible
   - Add caching for common queries
   - Pause non-critical workflows
3. Long-term fix:
   - Optimize prompt length
   - Use cheaper models for simple tasks
   - Implement request deduplication

**Prevention:**
- Set daily spend limits on Anthropic
- Monitor tokens per lead metric
- Regular prompt optimization reviews

---

#### Issue: HubSpot sync failures

**Symptoms:** Leads processed but not appearing in HubSpot, "Contact already exists" errors

**Diagnosis:**
```bash
# Check HubSpot API logs
curl "https://api.hubapi.com/crm/v3/objects/contacts?limit=10" \
  -H "Authorization: Bearer $HUBSPOT_API_KEY"

# Test contact creation
curl -X POST "https://api.hubapi.com/crm/v3/objects/contacts" \
  -H "Authorization: Bearer $HUBSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d @test_contact.json
```

**Resolution:**
1. If contact exists:
   - Update logic to find-or-create instead of create-only
   - Use email as unique identifier
2. If API errors:
   - Check HubSpot custom properties exist
   - Verify API key permissions
   - Check rate limits
3. Redeploy n8n workflow with fix
4. Manually create missing deals if needed

**Prevention:**
- Implement find-or-create pattern
- Add HubSpot health checks to monitoring
- Set up HubSpot rate limit handling

---

### Emergency Contacts

**Primary On-Call:** Lucas Barrios  
**Email:** lucas@kairos-consulting.co  
**Phone:** +49 XXX XXXX XXXX  
**Slack:** @lucas  

**Backup (if Lucas unavailable):**  
**Name:** [Freelance Developer TBD]  
**Email:** TBD  
**Phone:** TBD  

**Vendor Support:**
- **n8n:** support@n8n.io (response: 24-48h)
- **Anthropic:** support@anthropic.com (response: 24h)
- **HubSpot:** developers.hubspot.com/support (response: 24h)
- **Supabase:** support@supabase.io (response: 24-48h)

---

## 11. Performance Benchmarks

### Target Performance (Phase 1)

| Metric | Target | Acceptable | Poor |
|--------|--------|------------|------|
| Webhook response time | <1s | <2s | >2s |
| End-to-end processing | <1 min | <2 min | >2 min |
| API success rate | >99.5% | >99% | <99% |
| Scoring accuracy | >85% | >80% | <80% |
| Cost per lead | <€0.50 | <€1.00 | >€1.00 |

### Load Testing Results

**Test Setup:**
- 100 concurrent form submissions
- Simulated over 60 seconds
- Mixed industries and budgets

**Results (to be filled after testing):**
- Median response time: ___ ms
- 95th percentile: ___ ms
- 99th percentile: ___ ms
- Error rate: ___%
- Throughput: ___ leads/minute

---

## 12. Security Checklist

### Pre-Production Security Audit

- [ ] All API keys stored in environment variables (not hardcoded)
- [ ] Webhook endpoint uses HTTPS only
- [ ] Request signature verification enabled
- [ ] IP whitelisting configured (if applicable)
- [ ] Supabase RLS policies enabled
- [ ] HubSpot API key has minimal required permissions
- [ ] Slack webhook URL not publicly exposed
- [ ] No sensitive data logged in plain text
- [ ] Rate limiting implemented on webhook
- [ ] Error messages don't expose system details

### Ongoing Security Practices

- [ ] Rotate API keys quarterly
- [ ] Review access logs monthly
- [ ] Update dependencies for security patches
- [ ] Monitor for unusual API usage patterns
- [ ] Regular penetration testing (annual)

---

**Document Version:** 1.0  
**Last Updated:** May 18, 2026  
**Next Review:** August 18, 2026  
**Maintained By:** Lucas Barrios
