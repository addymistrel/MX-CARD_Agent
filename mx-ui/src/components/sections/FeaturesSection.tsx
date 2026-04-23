import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { SectionHeading } from "@/components/shared/SectionHeading";
import { getIcon } from "@/helpers/icons";
import featuresData from "@/data/features.json";
import type { Feature } from "@/types";

const features: Feature[] = featuresData;

export function FeaturesSection() {
  return (
    <section id="features" className="py-20 sm:py-28">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeading
          title="Everything You Need to Code Faster"
          subtitle="A comprehensive suite of built-in tools that let the AI agent work autonomously on your codebase."
        />

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature) => {
            const Icon = getIcon(feature.icon);
            return (
              <Card
                key={feature.title}
                className="group relative overflow-hidden transition-all hover:shadow-lg hover:-translate-y-1"
              >
                <CardHeader>
                  <div className="mb-3 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary transition-colors group-hover:bg-primary group-hover:text-primary-foreground">
                    <Icon className="h-6 w-6" />
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                  <CardDescription className="text-sm leading-relaxed">
                    {feature.description}
                  </CardDescription>
                </CardHeader>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
}
