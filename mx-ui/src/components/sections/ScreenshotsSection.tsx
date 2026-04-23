import { SectionHeading } from "@/components/shared/SectionHeading";
import screenshotsData from "@/data/screenshots.json";
import type { Screenshot } from "@/types";

const screenshots: Screenshot[] = screenshotsData;

export function ScreenshotsSection() {
  return (
    <section id="screenshots" className="py-20 sm:py-28 bg-muted/30">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeading
          title="See It in Action"
          subtitle="A clean, minimal terminal UI designed for productivity and clarity."
        />

        <div className="grid gap-8 md:grid-cols-3">
          {screenshots.map((shot) => (
            <div key={shot.alt} className="group">
              <div className="overflow-hidden rounded-xl border bg-card shadow-sm transition-all group-hover:shadow-lg">
                <img
                  src={shot.src}
                  alt={shot.alt}
                  className="w-full h-auto transition-transform group-hover:scale-105"
                  loading="lazy"
                />
              </div>
              <p className="mt-3 text-center text-sm text-muted-foreground">
                {shot.caption}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
