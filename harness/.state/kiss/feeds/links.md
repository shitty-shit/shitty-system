# Links feed — every bullet becomes a link cube on the deck

Format: `- [title](url) — description`. `{{ROOT}}` is expanded to this
workspace's file:// path at generation time. Add a line, run
`python .state/kiss/gen_kiss.py`, done — that's the whole recipe for one kind of content.

- [KISS deck]({{ROOT}}/.state/kiss/index.html) — the deck itself
- [Projects board]({{ROOT}}/.state/projects/index.html) — all projects, one board
- [Agent dashboard]({{ROOT}}/.state/dash.html) — open sessions, tasks, day brief
- [KISS inbox]({{ROOT}}/.state/kiss/inbox) — briefs waiting for agents
- [ShittyShit.co](https://shittysh.co) — the mothership
- [LiteLLM gateway](http://localhost:4000) — token front desk
- [AnythingLLM](http://localhost:3001) — memory loop workspace