import { CheckCircle2, Terminal, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export function AuthSuccessPage() {
  const navigate = useNavigate();

  return (
    <section className="flex min-h-[calc(100vh-4rem)] items-center justify-center py-12 px-4">
      <Card className="w-full max-w-md text-center border-emerald-500/30 bg-card shadow-lg">
        <CardHeader className="flex flex-col items-center space-y-4 pb-2">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-emerald-500/10 text-emerald-500">
            <CheckCircle2 className="h-10 w-10 text-emerald-500" />
          </div>
          <CardTitle className="text-2xl font-bold tracking-tight">Login Successful!</CardTitle>
          <CardDescription className="text-base text-muted-foreground">
            Now you can return back to the agent page.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6 pt-4">
          <div className="rounded-lg border bg-muted/40 p-4 text-left text-sm text-muted-foreground flex items-center gap-3">
            <Terminal className="h-5 w-5 text-primary shrink-0" />
            <div>
              <p className="font-medium text-foreground">Terminal Activated</p>
              <p className="text-xs">Your terminal session has been authenticated and focused.</p>
            </div>
          </div>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Button variant="outline" className="w-full sm:w-auto" onClick={() => navigate("/")}>
              Go to Home
            </Button>
            <Button className="w-full sm:w-auto" onClick={() => navigate("/docs")}>
              <span>View Docs</span>
              <ArrowRight className="h-4 w-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </section>
  );
}

