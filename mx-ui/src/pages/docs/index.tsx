import { Card, CardContent, CardHeader } from "@/components/ui/card";

const modules = [
  {
    title: "Terminal-first workflow",
    description:
      "Launch the agent with a project directory, prompt it naturally, and work from the terminal instead of a browser-only dashboard.",
    bullets: [
      "Persistent chat session and project context",
      "Local state saved between runs",
      "Single command startup with optional prompt input",
    ],
  },
  {
    title: "File and shell tools",
    description:
      "The agent can inspect existing files, edit code, create new files, and run shell commands in the project environment.",
    bullets: [
      "read_file and write_file for source control work",
      "shell execution with timeout protection",
      "undo tracking for file changes",
    ],
  },
  {
    title: "Approval and safety",
    description:
      "Critical commands can be gated through approval policies so the agent stays transparent before executing risky actions.",
    bullets: [
      "on-request, on-failure, auto, and never modes",
      "Explicit confirmation before sensitive actions",
      "Per-session safety controls for command execution",
    ],
  },
  {
    title: "Memory and context",
    description:
      "Useful facts can be retained across runs so the agent remembers project conventions, notes, and preferences without manual repetition.",
    bullets: [
      "Memory tool for durable notes",
      "Context management for conversation continuity",
      "Session statistics and checkpoint restores",
    ],
  },
  {
    title: "Subagents and MCP",
    description:
      "Complex tasks can be split into specialist sub-agents and connected to external MCP tools when they are available.",
    bullets: [
      "Nested agent execution for targeted work",
      "MCP server discovery and tool registration",
      "Structured tool calling with metadata and output tracing",
    ],
  },
  {
    title: "Authentication and session control",
    description:
      "Each request checks whether the user is signed in and logs them out automatically after a fixed local timeout window.",
    bullets: [
      "Terminal sign-in flow with callback URL",
      "Local session expiry protection",
      "Re-authentication required after timeout",
    ],
  },
];

export function DocsPage() {
  return (
    <section className="mx-auto max-w-6xl px-4 py-20 sm:px-6 lg:px-8">
      <div className="mb-12 max-w-3xl">
        <p className="mb-3 text-sm font-medium uppercase tracking-[0.2em] text-primary">
          Documentation
        </p>
        <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
          Real workflows for an autonomous coding agent.
        </h1>
        <p className="mt-4 text-lg text-muted-foreground">
          MX-CARD Agent is built for codebases that need direct access to the
          filesystem, the shell, and the project context that makes debugging
          and iteration fast.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {modules.map((item) => (
          <Card key={item.title} className="h-full border-border/80 bg-card/90">
            <CardHeader>
              <div className="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-sm font-semibold text-primary">
                {item.title.slice(0, 1).toUpperCase()}
              </div>
              <h2 className="text-xl font-semibold text-foreground">
                {item.title}
              </h2>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm leading-6 text-muted-foreground">
                {item.description}
              </p>
              <ul className="space-y-2 text-sm text-muted-foreground">
                {item.bullets.map((bullet) => (
                  <li key={bullet} className="flex gap-2">
                    <span className="mt-1 inline-block h-2 w-2 rounded-full bg-primary" />
                    <span>{bullet}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}
