import { Download, ExternalLink, Terminal } from "lucide-react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

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

      <Card className="mb-10 border-primary/30 bg-primary/5">
        <CardContent className="flex flex-col gap-6 p-6 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-medium uppercase tracking-[0.2em] text-primary">
              Windows installer
            </p>
            <h2 className="mt-2 text-2xl font-semibold">
              Install MX-CARD Agent in a few minutes.
            </h2>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-muted-foreground">
              Download the installer, enter your OpenRouter API key, then run
              <code className="mx-1 rounded bg-muted px-1.5 py-0.5">mxcagent</code>
              from any new terminal.
            </p>
          </div>
          <a href="/downloads/mxcagent-installer.exe" download>
            <Button size="lg" className="gap-2 whitespace-nowrap">
              <Download className="h-4 w-4" />
              Download installer
            </Button>
          </a>
        </CardContent>
      </Card>

      <p className="mb-10 rounded-lg border border-border bg-muted/40 p-4 text-center text-sm text-muted-foreground">
        Linux and macOS installers are coming soon. The source installation
        workflow is currently available on all supported platforms.
      </p>

      <div className="mb-10 grid gap-6 lg:grid-cols-2">
        <Card className="border-border/80 bg-card/90">
          <CardHeader>
            <h2 className="text-2xl font-semibold">Use locally from source</h2>
          </CardHeader>
          <CardContent className="space-y-4 text-sm leading-6 text-muted-foreground">
            <p>Use Python 3.11 or newer and an OpenRouter-compatible API key.</p>
            <pre className="overflow-x-auto rounded-lg bg-muted p-4 text-xs text-foreground">
{`git clone https://github.com/addymistrel/MX-CARD_Agent.git
cd MX-CARD_Agent
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt`}
            </pre>
            <p>
              Create a <code className="rounded bg-muted px-1.5 py-0.5">.env</code>
              file in the project root, then start the interactive agent:
            </p>
            <pre className="overflow-x-auto rounded-lg bg-muted p-4 text-xs text-foreground">
{`MX_CARD_API_KEY=your-openrouter-key
MX_CARD_BASE_URL=https://openrouter.ai/api/v1

python main.py`}
            </pre>
          </CardContent>
        </Card>

        <Card className="border-border/80 bg-card/90">
          <CardHeader>
            <h2 className="text-2xl font-semibold">Install on Windows</h2>
          </CardHeader>
          <CardContent className="space-y-4 text-sm leading-6 text-muted-foreground">
            <ol className="list-decimal space-y-3 pl-5">
              <li>Download and run the installer above.</li>
              <li>
                Create an OpenRouter account and an API key at{" "}
                <a
                  className="text-primary underline underline-offset-4"
                  href="https://openrouter.ai/workspaces/default/keys"
                  target="_blank"
                  rel="noreferrer"
                >
                  OpenRouter Keys <ExternalLink className="inline h-3 w-3" />
                </a>
                .
              </li>
              <li>Enter the key when the installer prompts you.</li>
              <li>Open a new PowerShell window so the PATH update is available.</li>
              <li>Run <code className="rounded bg-muted px-1.5 py-0.5">mxcagent</code>.</li>
            </ol>
            <div className="rounded-lg border border-border p-4">
              <p className="font-medium text-foreground">Start in any project</p>
              <pre className="mt-3 overflow-x-auto text-xs text-foreground">
{`cd C:\\Projects\\my-app
mxcagent`}
              </pre>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="mb-10 border-border/80 bg-card/90">
        <CardHeader>
          <h2 className="flex items-center gap-2 text-2xl font-semibold">
            <Terminal className="h-5 w-5 text-primary" />
            Command-line usage
          </h2>
        </CardHeader>
        <CardContent className="grid gap-6 text-sm leading-6 text-muted-foreground md:grid-cols-2">
          <div>
            <p>Interactive mode keeps a session open for multiple requests.</p>
            <pre className="mt-3 overflow-x-auto rounded-lg bg-muted p-4 text-xs text-foreground">
{`mxcagent

# Or from source:
python main.py`}
            </pre>
          </div>
          <div>
            <p>Run one prompt and exit, optionally targeting another folder.</p>
            <pre className="mt-3 overflow-x-auto rounded-lg bg-muted p-4 text-xs text-foreground">
{`mxcagent "Explain this project"
mxcagent -c C:\\Projects\\my-app "Find the auth bug"

# From source:
python main.py -c D:\\Projects\\my-app "Review the API"`}
            </pre>
          </div>
        </CardContent>
      </Card>

      <h2 className="mb-6 text-3xl font-bold tracking-tight">Agent commands</h2>
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

      <div className="mt-10 grid gap-6 lg:grid-cols-2">
        <Card className="border-border/80 bg-card/90">
          <CardHeader>
            <h2 className="text-2xl font-semibold">Useful slash commands</h2>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 font-mono text-xs text-muted-foreground">
              <li><span className="text-foreground">/help</span> — show all commands</li>
              <li><span className="text-foreground">/model &lt;name&gt;</span> — change the model</li>
              <li><span className="text-foreground">/model-helper</span> — find free models</li>
              <li><span className="text-foreground">/approval &lt;mode&gt;</span> — change safety mode</li>
              <li><span className="text-foreground">/clear</span> — clear conversation history</li>
              <li><span className="text-foreground">/undo</span> — undo the last file change</li>
              <li><span className="text-foreground">/save</span> and <span className="text-foreground">/resume</span> — manage sessions</li>
              <li><span className="text-foreground">/exit</span> — close the agent</li>
            </ul>
          </CardContent>
        </Card>
        <Card className="border-border/80 bg-card/90">
          <CardHeader>
            <h2 className="text-2xl font-semibold">Troubleshooting</h2>
          </CardHeader>
          <CardContent className="space-y-3 text-sm leading-6 text-muted-foreground">
            <p><strong className="text-foreground">Command not found:</strong> open a new terminal after installation, or run the executable from <code className="rounded bg-muted px-1.5 py-0.5">%LOCALAPPDATA%\\MXCardAgent</code>.</p>
            <p><strong className="text-foreground">Missing API key:</strong> rerun the installer and enter a valid OpenRouter key, or configure the local <code className="rounded bg-muted px-1.5 py-0.5">.env</code>.</p>
            <p><strong className="text-foreground">Model errors:</strong> use <code className="rounded bg-muted px-1.5 py-0.5">/model-helper</code> to compare models and then set one with <code className="rounded bg-muted px-1.5 py-0.5">/model &lt;model name&gt;</code>.</p>
          </CardContent>
        </Card>
      </div>
    </section>
  );
}
