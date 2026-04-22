import { SectionHeading } from "@/components/shared/SectionHeading";

const TUTORIAL_VIDEO_URL = "https://www.youtube.com/embed/dQw4w9WgXcQ";
const TUTORIAL_TITLE = "MX-CARD Agent - Getting Started Tutorial";

export function TutorialSection() {
  return (
    <section id="tutorial" className="py-20 sm:py-28">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeading
          title="Watch How It Works"
          subtitle="A quick walkthrough of setting up and using MX-CARD Agent for your projects."
        />

        <div className="mx-auto max-w-4xl">
          <div className="relative overflow-hidden rounded-xl border bg-card shadow-lg" style={{ paddingBottom: "56.25%" }}>
            <iframe
              className="absolute inset-0 h-full w-full"
              src={TUTORIAL_VIDEO_URL}
              title={TUTORIAL_TITLE}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
          <p className="mt-4 text-center text-sm text-muted-foreground">
            {TUTORIAL_TITLE}
          </p>
        </div>
      </div>
    </section>
  );
}
