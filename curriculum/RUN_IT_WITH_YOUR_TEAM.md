# Run the free agent course with your whole team

**Who it is for:** an engineering lead whose team has started (or is about to start) building an agent. It uses the free, public lab for the book *Production-Ready AI Agents* as the shared starting point: <https://github.com/ai-builders-group/build-production-ai-agents>.
**Time:** three sessions of 90 minutes, a week apart is easiest. Before session 1, each engineer works through the course's first three lessons on their own. Lesson 1 needs two free accounts (a model gateway key and a tracing key), so set those up first.
**Roles:** one facilitator (the lead or a senior engineer), one scribe. No expert from outside is needed. Nothing is shared outside the team.

## Session 1: Map the loop onto your own system (90 min)
Predict first (2 min): *which part of our agent decides what happens next: code or the model?*
1. **Recap (15 min).** Each engineer says in one sentence what the agent loop is, in the course's terms: the agent's state, its steps, the router that decides after each model call whether to use a tool or finish, and the tool step that runs it and feeds the result back for the next round.
2. **Map your own agent (50 min).** On one page, draw your agent as states and steps, then mark every tool it can call. Use Table 1 as the shape of the page.
3. **Gaps (20 min).** Circle each tool that can **change** something outside the agent (write, send, charge, delete). These are the ones the next session is about.
4. **Close (5 min).** Scribe photographs the page. Owner of each circled tool is named.

**Table 1.** The loop map: one row per tool, what it can change, and who owns it.

| Tool | Reads or changes? | What it can change (system, record, person) | Owner on call |
|---|---|---|---|
| | | | |

## Session 2: What can go wrong, and what repeats (90 min)
Predict first (2 min): *when this tool fails halfway and the agent tries again, what happens in the other system?*
1. **Recap of safe behaviour (15 min).** Walk through what lessons 6 to 8 add: a strict output schema; rules in the system prompt plus a sandboxed tool with path checks and an automated test; and lazy loading, retries, caching and graceful failure for tools. For each, say what it protects against and what it does not.
2. **Retry table (50 min).** For every circled tool from Table 1, fill Table 2. The question that matters is the third column: does a second attempt repeat the outward effect?
3. **Decide (20 min).** For each row where a retry repeats the effect, choose one: the receiver refuses the second copy; the team keeps its own record of what was already done; or a person approves the action. "We hope it does not happen" is not an option.
4. **Close (3 min).** Scribe records the open rows.

**Table 2.** The retry table: for each tool, what is retried and what a retry would repeat.

| Tool | What triggers a retry | What a second attempt repeats | Protection today | Open risk |
|---|---|---|---|---|
| | | | | |

*Where the lessons stop:* the course's retries and caching cover tools that look things up and analyse code, where repeating a call is harmless. Actions with outside effects, runs that outlive a crash, and who may approve need more care, and this table is where you find out how much.

## Session 3: Score it (90 min)
1. **Self-check (35 min).** Answer the ten questions in Table 3 for the agent you mapped. Score 2 (yes, and we have shown it), 1 (partly or not shown), 0 (no or do not know). Answer for the agent as it runs **today**.
2. **Discuss the lowest three (35 min).** For each, name the smallest change that would raise it and who would make it.
3. **Decide (20 min).** Pick one change to make this month and one question to re-score in 30 days. Write both on the page.

**Table 3.** The team self-check: ten questions, each scored 0, 1 or 2 for the agent as it runs today.

| # | Question | Score |
|---|---|---|
| 1 | Can you say in one sentence, with a number you could count, what the agent is for? | |
| 2 | Is there a written list of things it must never do, each one testable? | |
| 3 | Is each limit (amount, count, scope) stored once, with everything else reading from it? | |
| 4 | If the process dies mid-run, does the run continue from its last step? | |
| 5 | For each outward action, can you point to where the receiving system refuses a second copy, or to the approval that covers the gap? | |
| 6 | When a later step fails, what undoes the earlier ones, and who owns that undo? | |
| 7 | For anything irreversible, who approves, and how does the system know the approval is real? | |
| 8 | Can a code change land while runs are still in progress without breaking them? | |
| 9 | Are the agent's outputs checked the way their consumer will read them, not by scanning for words? | |
| 10 | On one screen, can you see every run that is waiting, stuck or retrying, and how old it is? | |

**Reading the score (out of 20):** 0–7, the agent is acting on trust; 8–13, you have some protections, and the lowest-scoring row is your next risk; 14–20, you are in good shape, and the thing to prove is that each "2" still holds after your next change. 

## What the team keeps
The loop map (Table 1), the retry table (Table 2), the scored self-check (Table 3), and one change with an owner and a date.

## After the three sessions
Re-score the one question you picked in 30 days. If you improved it, pick the next lowest. Questions about the course lessons belong in the repository's Issues tab.

