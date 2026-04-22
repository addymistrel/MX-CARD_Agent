import { Link } from "react-router-dom";
import { ArrowRight, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { SITE_NAME, SITE_TAGLINE, SITE_DESCRIPTION } from "@/constants/site";

export function HeroSection() {
  return (
    <section className="relative overflow-hidden py-20 sm:py-32">
      {/* Background gradient */}
      <div className="pointer-events-none absolute inset-0 -z-10">
        <div className="absolute left-1/2 top-0 -translate-x-1/2 h-[600px] w-[600px] rounded-full bg-primary/10 blur-3xl" />
        <div className="absolute right-0 top-1/2 h-[400px] w-[400px] rounded-full bg-primary/5 blur-3xl" />
      </div>

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
        <Badge variant="secondary" className="mb-6 gap-1.5 px-3 py-1.5 text-sm">
          <Sparkles className="h-3.5 w-3.5" />
          Now with MCP Tool Integration
        </Badge>

        <h1 className="text-4xl font-extrabold tracking-tight sm:text-6xl lg:text-7xl">
          Meet{" "}
          <span className="bg-gradient-to-r from-primary to-purple-400 bg-clip-text text-transparent">
            {SITE_NAME}
          </span>
        </h1>

        <p className="mt-4 text-xl font-medium text-foreground/80 sm:text-2xl">
          {SITE_TAGLINE}
        </p>

        <p className="mx-auto mt-6 max-w-2xl text-base text-muted-foreground sm:text-lg leading-relaxed">
          {SITE_DESCRIPTION}
        </p>

        <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link to="/auth">
            <Button size="lg" className="gap-2 text-base px-8">
              Get Started <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
          <a href="#features">
            <Button variant="outline" size="lg" className="text-base px-8">
              Learn More
            </Button>
          </a>
        </div>

        {/* Terminal preview */}
        <div className="mx-auto mt-16 max-w-3xl rounded-xl border bg-card shadow-2xl overflow-hidden">
          <div className="flex items-center gap-2 border-b px-4 py-3 bg-muted/50">
            <div className="h-3 w-3 rounded-full bg-red-400" />
            <div className="h-3 w-3 rounded-full bg-yellow-400" />
            <div className="h-3 w-3 rounded-full bg-green-400" />
            <span className="ml-2 text-xs text-muted-foreground font-mono">mx-card-agent</span>
          </div>
          <div className="p-6 text-left font-mono text-sm leading-relaxed">
            <p className="text-muted-foreground">$ python main.py</p>
            <p className="mt-2 text-primary">✦ MX-CARD Agent v1.0</p>
            <p className="text-muted-foreground">  Model: gpt-4o &nbsp;│&nbsp; CWD: ~/my-project</p>
            <p className="mt-3 text-foreground">&gt; Fix the authentication bug in auth.py</p>
            <p className="mt-2 text-muted-foreground">
              <span className="text-green-500">✓</span> Reading auth.py...
            </p>
            <p className="text-muted-foreground">
              <span className="text-green-500">✓</span> Found issue on line 42
            </p>
            <p className="text-muted-foreground">
              <span className="text-green-500">✓</span> Applied fix &amp; verified
            </p>
            <p className="mt-2 text-primary">Done in 3.2s - 1 file changed</p>
          </div>
        </div>
      </div>
    </section>
  );
}
