import { Star } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { SectionHeading } from "@/components/shared/SectionHeading";
import testimonialsData from "@/data/testimonials.json";
import type { Testimonial } from "@/types";

const testimonials: Testimonial[] = testimonialsData;

export function TestimonialsSection() {
  return (
    <section id="testimonials" className="py-20 sm:py-28 bg-muted/30">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeading
          title="Loved by Developers"
          subtitle="See what developers around the world are saying about MX-CARD Agent."
        />

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {testimonials.map((t) => (
            <Card key={t.name} className="flex flex-col">
              <CardContent className="flex flex-1 flex-col p-6">
                {/* Stars */}
                <div className="flex gap-0.5 mb-4">
                  {Array.from({ length: 5 }).map((_, i) => (
                    <Star
                      key={i}
                      className={`h-4 w-4 ${
                        i < t.rating
                          ? "fill-yellow-400 text-yellow-400"
                          : "text-muted-foreground/30"
                      }`}
                    />
                  ))}
                </div>

                {/* Content */}
                <p className="flex-1 text-sm leading-relaxed text-muted-foreground">
                  "{t.content}"
                </p>

                {/* Author */}
                <div className="mt-4 flex items-center gap-3 pt-4 border-t">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-primary text-sm font-bold">
                    {t.avatar}
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-foreground">{t.name}</p>
                    <p className="text-xs text-muted-foreground">{t.role}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
