Q&A:
https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708107

Video:
https://www.youtube.com/playlist?list=PLqFaTIg4myu8AFXUjrVhDkUGp0A9kK8CX

## Assignments
- Day1 codelab 1: https://codelabs.developers.google.com/getting-started-google-antigravity#8
- Day1 codelab 2: https://codelabs.developers.google.com/deploy-from-aistudio-to-run?hl=en#0
- 






### Day 1 Paper - New SDLC with Vibe Coding 

**Core thesis:** Software engineering is shifting from writing syntax to expressing intent. As of early 2026, 85% of professional developers regularly use AI coding agents, and ~41% of new code is AI-generated. This demands a rethinking of the entire SDLC.

**The vibe coding → agentic engineering spectrum**

"Vibe coding" (coined by Karpathy in Feb 2025) means prompting an AI, accepting its output, and copy-pasting errors back for fixes — minimal verification, high risk. "Agentic engineering" is the disciplined end: formal specs, automated test suites, CI/CD gates, human oversight of architecture. The key differentiator isn't *whether* you use AI, it's *how outputs get verified* — through deterministic tests (correct input/output) and evaluations (correct trajectory and reasoning).

**Context engineering as the central skill**

AI output quality depends less on prompt cleverness and more on the richness of context provided. Six context types matter: instructions, knowledge, memory, examples, tools, and guardrails. The key architectural decision is what lives in static context (always loaded, expensive) vs. dynamic context (loaded on demand via "Agent Skills"). This is a financial lever too — bloated static context burns tokens wastefully.

**The new SDLC**

AI compresses implementation from weeks to hours, but requirements, architecture, and verification remain human-paced. The paper walks through each SDLC phase:
- **Requirements:** AI generates user stories, edge cases, and prototypes from natural language
- **Architecture:** Still stubbornly human — trade-offs require business judgment AI can't fully grasp
- **Implementation:** Real productivity gains (25–39% per surveys), but one METR study found experienced devs took 19% *longer* on some tasks due to verification overhead
- **Testing:** Both output evals and trajectory evals are needed; tests become the primary way to communicate intent to agents
- **Maintenance:** Legacy codebases that were "too risky to touch" become navigable with AI assistance

**The factory model and the harness**

The developer's output is no longer code — it's the *system that produces code*. The key insight: `Agent = Model + Harness`. The harness (prompts, tools, sandboxes, orchestration logic, guardrails, observability) dominates agent behavior more than the underlying model. One benchmark showed moving an agent from outside the Top 30 to Top 5 *by changing only the harness*, with no model change.

**Developer roles: conductor vs. orchestrator**

- **Conductor:** Real-time, in-IDE, keystroke-level control — good for complex/unfamiliar code
- **Orchestrator:** Async, goal-level delegation to background agents — good for well-specified tasks like migrations or test generation

Most developers fluidly move between both modes.

**The 80% problem**

AI rapidly produces ~80% of a feature, but the remaining 20% — edge cases, error handling, subtle correctness — requires deep contextual knowledge models often lack. Errors have shifted from syntax mistakes to insidious *conceptual* failures that look correct and may pass basic tests.

**Economics**

Vibe coding = low CapEx, high OpEx (token burn, maintenance tax, security remediation). Agentic engineering = higher upfront CapEx (spec design, test suites, context structuring), but dramatically lower marginal cost per feature. Advanced setups use intelligent model routing — expensive frontier models for architecture/requirements, cheaper smaller models for test generation and CI monitoring.

**Conclusion: three durable principles**

1. *Structure scales, vibes don't* — production systems require agentic discipline
2. *AI amplifies your engineering culture* — it multiplies both strengths and weaknesses
3. *The human role is evolving, not diminishing* — judgment, specification, and verification are the new craft

