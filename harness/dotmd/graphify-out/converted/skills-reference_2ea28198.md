<!-- converted from skills-reference.xlsx -->

## Sheet: Skills Reference
| Skill Name | Category | Definition / Description | How to Use / When to Activate | Example Prompt |
| --- | --- | --- | --- | --- |
| accessibility | Core | Audit and improve web accessibility following WCAG 2.2 guidelines. | Activate when asked to improve accessibility, run an a11y audit, achieve WCAG compliance, add screen reader support, fix keyboard navigation, or make a UI accessible. | 'Audit my landing page for WCAG 2.2 compliance and fix any issues.' |
| bash-defensive-patterns | Core | Master defensive Bash programming techniques for production-grade scripts. | Use when writing robust shell scripts, CI/CD pipelines, or system utilities that need fault tolerance and safety. | 'Review this deploy.sh script and apply defensive bash patterns.' |
| gepeto | Core | Guide for building 1-click launchers and building apps with launchers built-in using Pinokio. | Invoke when you want to create or package an app as a Pinokio launcher. | 'Help me build a Pinokio launcher for my Stable Diffusion workflow.' |
| pinokio | Core | Discover, launch, and use apps and tools for the current task. | Use when you need to find, install, or run an app/tool via Pinokio. | 'Find a Pinokio app that lets me run Whisper locally.' |
| remio | Core | Search, read, create, update, delete, or organize notes in the remio knowledge base, or ask questions over it via RAG. | Activate for any remio note-taking or knowledge-base task. | 'Search my remio notes for everything about pricing strategy.' |
| seo | Core | Optimize for search engine visibility and ranking. | Use when asked to improve SEO, optimize for search, fix meta tags, add structured data, optimize sitemaps, or perform search engine optimization. | 'Improve the SEO of my Next.js blog.' |
| zero | Core | Search for AI capabilities, call paid APIs, or access external services with automatic payment. | Activate when the user mentions zero, capability search, paid endpoints, x402, or needs a capability you don't natively have (image generation, translation, weather, etc.). | 'Use zero to find an image generation API and generate a logo.' |
| find-skills | Core | Helps users discover and install agent skills when they ask how to do something or express interest in extending capabilities. | Use when the user asks 'how do I do X', 'find a skill for X', or 'is there a skill that can...'. | 'Find a skill that can help me write better commit messages.' |
| graphify | Core | Turn any input (code, docs, papers, images) into a knowledge graph, cluster communities, and produce HTML + JSON + audit report. | Use when you want to visualize relationships in a body of knowledge. | 'Graphify this codebase and show me the module clusters.' |
| gsd-add-backlog | GSD | Add an idea to the backlog parking lot (999.x numbering). | Use when capturing future ideas that don't fit the current milestone. | 'Add an idea for dark mode to the backlog.' |
| gsd-add-phase | GSD | Add a phase to the end of the current milestone in the roadmap. | Use when planning new work within the current milestone. | 'Add a phase for API integration to the current milestone.' |
| gsd-add-tests | GSD | Generate tests for a completed phase based on UAT criteria and implementation. | Use after implementing a phase to create its test suite. | 'Generate tests for the auth phase I just finished.' |
| gsd-add-todo | GSD | Capture an idea or task as a todo from the current conversation context. | Use to turn any conversation item into a tracked todo. | 'Add a todo to refactor the database layer.' |
| gsd-analyze-dependencies | GSD | Analyze phase dependencies and suggest Depends on entries for ROADMAP.md. | Use when planning phases to identify and document dependencies. | 'Analyze dependencies between my frontend and backend phases.' |
| gsd-audit-fix | GSD | Autonomous audit-to-fix pipeline: find issues, classify, fix, test, commit. | Use when you want a full-cycle audit and automatic fixes. | 'Run an audit-fix cycle on the payment module.' |
| gsd-audit-milestone | GSD | Audit milestone completion against original intent before archiving. | Use before closing a milestone to verify everything was delivered. | 'Audit milestone 3 before archiving it.' |
| gsd-audit-uat | GSD | Cross-phase audit of all outstanding UAT and verification items. | Use to check what UAT items remain across the project. | 'Audit all outstanding UAT items.' |
| gsd-autonomous | GSD | Run all remaining phases autonomously: discuss, plan, execute per phase. | Use when you want the agent to drive the rest of the project. | 'Run the remaining roadmap phases autonomously.' |
| gsd-check-todos | GSD | List pending todos and select one to work on. | Use to see what todos are open and pick the next one. | 'Show me my pending todos.' |
| gsd-cleanup | GSD | Archive accumulated phase directories from completed milestones. | Use to clean up old phase artifacts after a milestone is done. | 'Clean up archived phase directories.' |
| gsd-code-review | GSD | Review source files changed during a phase for bugs, security issues, and code quality problems. | Use after a phase to review the changed code. | 'Review the code changed in phase 5.' |
| gsd-code-review-fix | GSD | Auto-fix issues found by code review in REVIEW.md. | Use after a code review to apply its fixes automatically. | 'Fix the issues from the latest code review.' |
| gsd-complete-milestone | GSD | Archive a completed milestone and prepare for the next version. | Use when a milestone is fully done. | 'Complete milestone 2 and prepare for v3.' |
| gsd-debug | GSD | Systematic debugging with persistent state across context resets. | Use for hard bugs that need structured investigation. | 'Debug why the login flow intermittently fails.' |
| gsd-discuss-phase | GSD | Gather phase context through adaptive questioning before planning. | Use before planning a phase to clarify requirements. Use --auto to skip interactive questions. | 'Discuss the upcoming payment phase with me.' |
| gsd-do | GSD | Route freeform text to the right GSD command automatically. | Use when you have a vague request and want it routed to the correct GSD skill. | 'I need to plan the next milestone.' |
| gsd-docs-update | GSD | Generate or update project documentation verified against the codebase. | Use when docs need to reflect the current code. | 'Update the README to match the latest API.' |
| gsd-execute-phase | GSD | Execute all plans in a phase with wave-based parallelization. | Use when a phase plan is ready and you want it executed. | 'Execute phase 4.2.' |
| gsd-explore | GSD | Socratic ideation and idea routing: think through ideas before committing to plans. | Use early in planning to explore possibilities. | 'Explore ideas for improving user onboarding.' |
| gsd-fast | GSD | Execute a trivial task inline with GSD guarantees but skip optional agents. | Use for very small, low-risk tasks. | 'Fast update the version number in package.json.' |
| gsd-forensics | GSD | Post-mortem investigation for failed GSD workflows. | Use after a GSD workflow fails to diagnose what went wrong. | 'Investigate why the last phase execution failed.' |
| gsd-health | GSD | Diagnose planning directory health and optionally repair issues. | Use to check the integrity of the .planning directory. | 'Check the health of my GSD planning directory.' |
| gsd-help | GSD | Show available GSD commands and usage guide. | Use when you need a quick reference of GSD commands. | 'Show me the GSD help.' |
| gsd-import | GSD | Ingest external plans with conflict detection against project decisions before writing anything. | Use when bringing in plans from outside the project. | 'Import this external product spec into the roadmap.' |
| gsd-insert-phase | GSD | Insert urgent work as a decimal phase (e.g., 72.1) between existing phases. | Use when something urgent needs to be added between planned phases. | 'Insert a hotfix phase between 7 and 8.' |
| gsd-intel | GSD | Query, inspect, or refresh codebase intelligence files in .planning/intel/. | Use to manage project intelligence artifacts. | 'Refresh the codebase intel files.' |
| gsd-join-discord | GSD | Join the GSD Discord community. | Use when the user wants community support or to join the GSD Discord. | 'How do I join the GSD Discord?' |
| gsd-list-phase-assumptions | GSD | Surface Codex's assumptions about a phase approach before planning. | Use to validate assumptions before committing to a plan. | 'List assumptions for the caching phase.' |
| gsd-list-workspaces | GSD | List active GSD workspaces and their status. | Use to see all current GSD workspaces. | 'List my GSD workspaces.' |
| gsd-manager | GSD | Interactive command center for managing multiple phases from one terminal. | Use when orchestrating many phases at once. | 'Open the GSD manager.' |
| gsd-map-codebase | GSD | Analyze codebase with parallel mapper agents to produce .planning/codebase/ documents. | Use when you need a structured map of the codebase. | 'Map this codebase for me.' |
| gsd-milestone-summary | GSD | Generate a comprehensive project summary from milestone artifacts for team onboarding and review. | Use when sharing milestone progress with stakeholders. | 'Generate a summary of milestone 1 for the team.' |
| gsd-new-milestone | GSD | Start a new milestone cycle: update PROJECT.md and route to requirements. | Use when beginning a new milestone. | 'Start milestone 3 for this project.' |
| gsd-new-project | GSD | Initialize a new project with deep context gathering and PROJECT.md. | Use when starting a brand new project with GSD. | 'Initialize a new GSD project for my app.' |
| gsd-new-workspace | GSD | Create an isolated workspace with repo copies and independent .planning/. | Use when you need a separate GSD workspace. | 'Create a new workspace for the experimental branch.' |
| gsd-next | GSD | Automatically advance to the next logical step in the GSD workflow. | Use when you want the agent to decide the next action. | 'What's next in the GSD workflow?' |
| gsd-note | GSD | Zero-friction idea capture: append, list, or promote notes to todos. | Use to quickly capture ideas without full planning. | 'Note: consider using Redis for session storage.' |
| gsd-pause-work | GSD | Create context handoff when pausing work mid-phase. | Use when stopping work and needing to resume later. | 'Pause work and create a handoff note.' |
| gsd-plan-milestone-gaps | GSD | Create phases to close all gaps identified by milestone audit. | Use after auditing a milestone to fill gaps. | 'Plan phases to close the gaps in milestone 2.' |
| gsd-plan-phase | GSD | Create a detailed phase plan (PLAN.md) with verification loop. | Use when planning a specific phase of work. | 'Plan phase 3 for the auth system.' |
| gsd-plant-seed | GSD | Capture a forward-looking idea with trigger conditions that surfaces automatically at the right milestone. | Use for ideas that should be revisited later. | 'Plant a seed to revisit mobile support when we hit v2.' |
| gsd-pr-branch | GSD | Create a clean PR branch by filtering out .planning/ commits for code review. | Use when preparing a GSD branch for pull request. | 'Create a PR branch for milestone 1.' |
| gsd-profile-user | GSD | Generate developer behavioral profile and create Codex-discoverable artifacts. | Use to build a profile of the user's working style. | 'Generate my developer profile.' |
| gsd-progress | GSD | Check project progress, show context, and route to next action. | Use to get a status update on the project. | 'Show me the project progress.' |
| gsd-quick | GSD | Execute a quick task with GSD guarantees (atomic commits, state tracking) but skip optional agents. | Use for small tasks where you still want GSD tracking. | 'Quickly fix the typo in the footer.' |
| gsd-reapply-patches | GSD | Reapply local modifications after a GSD update. | Use after updating GSD to restore local changes. | 'Reapply my patches after the GSD update.' |
| gsd-remove-phase | GSD | Remove a future phase from the roadmap and renumber subsequent phases. | Use when a planned phase is no longer needed. | 'Remove phase 4.2 from the roadmap.' |
| gsd-remove-workspace | GSD | Remove a GSD workspace and clean up worktrees. | Use when a workspace is no longer needed. | 'Remove the old feature workspace.' |
| gsd-research-phase | GSD | Research how to implement a phase (standalone; usually use /gsd-plan-phase instead). | Use when you need research before planning. | 'Research how to implement real-time sync for phase 5.' |
| gsd-resume-work | GSD | Resume work from a previous session with full context restoration. | Use when returning to a paused session. | 'Resume my previous session.' |
| gsd-review | GSD | Request cross-AI peer review of phase plans from external AI CLIs. | Use when you want external AI review of a plan. | 'Get a peer review of the migration plan.' |
| gsd-review-backlog | GSD | Review and promote backlog items to active milestone. | Use during planning to move backlog items into the current milestone. | 'Review the backlog and promote ready items.' |
| gsd-scan | GSD | Rapid codebase assessment: lightweight alternative to /gsd-map-codebase. | Use when you need a quick overview without full mapping. | 'Scan this codebase for me.' |
| gsd-secure-phase | GSD | Retroactively verify threat mitigations for a completed phase. | Use after a phase to check security mitigations. | 'Verify security mitigations for the auth phase.' |
| gsd-session-report | GSD | Generate a session report with token usage estimates, work summary, and outcomes. | Use at the end of a session to summarize work. | 'Generate a session report for today.' |
| gsd-set-profile | GSD | Switch model profile for GSD agents (quality/balanced/budget/inherit). | Use to control cost/quality tradeoffs for GSD agents. | 'Set the GSD profile to quality.' |
| gsd-settings | GSD | Configure GSD workflow toggles and model profile. | Use to change GSD behavior settings. | 'Open GSD settings.' |
| gsd-ship | GSD | Create PR, run review, and prepare for merge after verification passes. | Use when a feature is ready to ship. | 'Ship the feature branch.' |
| gsd-stats | GSD | Display project statistics: phases, plans, requirements, git metrics, and timeline. | Use when you want quantitative project insights. | 'Show me project stats.' |
| gsd-thread | GSD | Manage persistent context threads for cross-session work. | Use when working across multiple sessions on the same topic. | 'Create a new thread for the auth refactor.' |
| gsd-ui-phase | GSD | Generate a UI design contract (UI-SPEC.md) for frontend phases. | Use when planning frontend work that needs a design contract. | 'Create a UI spec for the dashboard phase.' |
| gsd-ui-review | GSD | Retroactive 6-pillar visual audit of implemented frontend code. | Use after implementing a UI to review its quality. | 'Review the implemented dashboard UI.' |
| gsd-undo | GSD | Safe git revert: roll back phase or plan commits using the phase manifest with dependency checks. | Use when you need to undo GSD commits safely. | 'Undo the last phase commit.' |
| gsd-update | GSD | Update GSD to the latest version with changelog display. | Use when updating the GSD tooling. | 'Update GSD to the latest version.' |
| gsd-validate-phase | GSD | Retroactively audit and fill Nyquist validation gaps for a completed phase. | Use after a phase to ensure validation is complete. | 'Validate phase 2 retroactively.' |
| gsd-verify-work | GSD | Validate built features through conversational UAT. | Use to run user acceptance testing conversationally. | 'Verify the checkout feature with me.' |
| gsd-workstreams | GSD | Manage parallel workstreams: list, create, switch, status, progress, complete, and resume. | Use when juggling multiple parallel tracks of work. | 'List my active workstreams.' |
| bring-to-source | Freebuff Built-in | Bring generated or referenced content into the project source tree. | Use when you want code, text, or assets moved into the actual project files. | 'Bring this generated component into the source code.' |
| commit | Freebuff Built-in | Create a git commit from current changes. | Use when you want the assistant to stage and commit changes with a message. | 'Commit these changes with a descriptive message.' |
| derisk | Freebuff Built-in | Analyze merge and deployment risk and advise how to reduce it. | Use before merging or deploying to identify risks. | 'Derisk this deployment.' |
| merge-local | Freebuff Built-in | Merge a branch locally without opening a PR. | Use when you want a local merge performed. | 'Merge the feature branch into main locally.' |
| merge-pr | Freebuff Built-in | Merge an open pull request. | Use when a PR is ready to be merged. | 'Merge PR #42.' |
| open-pr | Freebuff Built-in | Open a pull request from the current branch. | Use when you want to create a PR for the current branch. | 'Open a PR for this branch.' |
| preview | Freebuff Built-in | Preview the current web UI or app in a browser or live view. | Use when you want to see the result of frontend changes. | 'Preview this page in the browser.' |
| review | Freebuff Built-in | Request a code review of the current changes. | Use when you want feedback on code changes. | 'Review my latest changes.' |
| simplify | Freebuff Built-in | Simplify code, text, or a process. | Use when something feels overcomplicated and you want it simplified. | 'Simplify this function.' |
| test | Freebuff Built-in | Run tests for the project or a specific area. | Use when you want to verify code with tests. | 'Run the tests for the auth module.' |