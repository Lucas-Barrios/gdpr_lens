# Lab Summary: Autonomous Agent Challenge

## Reflection

The hardest part of planning this autonomous agent system was defining realistic scope boundaries between phases. I initially wanted to build the complete lead generation and qualification system (inbound + outbound prospecting + automated outreach) as the MVP, but quickly realized this was a 6-week production project, not a 60-minute lab. The discipline required to isolate Phase 1 (inbound qualification only) as the actual MVP - while documenting Phases 2-3 as future roadmap - was critical but difficult. It forced me to think like a consultant: what's the minimum that delivers real business value while setting up the foundation for future expansion?

If I were to do this differently, I would have started with a clearer definition of "what can I actually build and test in 60-90 minutes" versus "what's the complete vision for this system." The lab instructions said to plan first, then optionally build a prototype - but I treated planning as designing the full production system rather than scoping for the lab timeframe. This led to some scope creep in the planning phase itself. Next time, I'd lock down the MVP boundaries before writing the detailed technical plan.

The biggest open question is whether LangGraph is actually necessary for Phase 2's prospect research workflow, or if a simpler LangChain sequential chain would suffice. LangGraph adds complexity (state management, graph visualization, more code) but provides better control over multi-step research processes. I'm uncertain whether the added complexity is worth it for a relatively linear workflow: search → extract → score → draft. The decision hinges on how often the agent needs to backtrack or retry failed steps - if retries are rare, LangChain might be enough. If the research process is messy and requires complex error handling and state persistence, LangGraph justifies itself. I'll need to prototype both approaches to make an informed decision.

**Lab completed by:** Lucas Barrios  
**Date:** May 18, 2026  
**Program:** Ironhack AI Manager / AI Consulting Specialization
