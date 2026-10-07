import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { getEnvironmentVariable } from "@/helpers/envHelper";

const CONTACT_EMAIL =
  getEnvironmentVariable("VITE_CONTACT_EMAIL") ?? "hello@mx-card-agent.dev";

export function ContactPage() {
  const [form, setForm] = useState({ name: "", email: "", message: "" });
  const [status, setStatus] = useState<
    "idle" | "sending" | "success" | "error"
  >("idle");
  const [feedback, setFeedback] = useState("");

  const handleChange = (key: keyof typeof form, value: string) => {
    setForm((current) => ({ ...current, [key]: value }));
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setStatus("sending");
    setFeedback("");

    const subject = encodeURIComponent(
      `MX-CARD Agent enquiry from ${form.name}`,
    );
    const body = encodeURIComponent(
      `Name: ${form.name}\nEmail: ${form.email}\n\n${form.message}`,
    );

    window.location.href = `mailto:${CONTACT_EMAIL}?subject=${subject}&body=${body}`;

    setStatus("success");
    setFeedback("Your email client is opening with the message ready to send.");
    setForm({ name: "", email: "", message: "" });
  };

  return (
    <section className="mx-auto max-w-4xl px-4 py-20 sm:px-6 lg:px-8">
      <Card className="border-border/80 bg-card/90 shadow-sm">
        <CardHeader>
          <p className="text-sm font-medium uppercase tracking-[0.2em] text-primary">
            Contact
          </p>
          <h1 className="text-4xl font-bold tracking-tight">
            Let&apos;s build better tooling together.
          </h1>
        </CardHeader>
        <CardContent className="space-y-6 text-muted-foreground">
          <p>
            Questions, product feedback, or collaboration ideas? Fill the form
            and your default mail client will open with the message prepared.
          </p>

          <form className="space-y-4" onSubmit={handleSubmit}>
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <label
                  htmlFor="name"
                  className="text-sm font-medium text-foreground"
                >
                  Name
                </label>
                <Input
                  id="name"
                  value={form.name}
                  onChange={(event) => handleChange("name", event.target.value)}
                  placeholder="Your name"
                  required
                />
              </div>
              <div className="space-y-2">
                <label
                  htmlFor="email"
                  className="text-sm font-medium text-foreground"
                >
                  Email
                </label>
                <Input
                  id="email"
                  type="email"
                  value={form.email}
                  onChange={(event) =>
                    handleChange("email", event.target.value)
                  }
                  placeholder="you@example.com"
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <label
                htmlFor="message"
                className="text-sm font-medium text-foreground"
              >
                Message
              </label>
              <textarea
                id="message"
                value={form.message}
                onChange={(event) =>
                  handleChange("message", event.target.value)
                }
                className="min-h-32 w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:border-ring focus:outline-none focus:ring-2 focus:ring-ring/20"
                placeholder="Tell us what you are building or what you need help with."
                required
              />
            </div>

            <div className="flex flex-wrap items-center gap-4">
              <Button type="submit" disabled={status === "sending"}>
                {status === "sending" ? "Preparing..." : "Send message"}
              </Button>
              <a
                href="https://github.com/addymistrel/MX-CARD_Agent"
                target="_blank"
                rel="noreferrer"
              >
                <Button variant="outline" type="button">
                  GitHub
                </Button>
              </a>
            </div>

            {feedback && (
              <p
                className={
                  status === "success"
                    ? "text-sm text-primary"
                    : "text-sm text-destructive"
                }
              >
                {feedback}
              </p>
            )}
          </form>
        </CardContent>
      </Card>
    </section>
  );
}
