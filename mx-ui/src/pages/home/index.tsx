import { HeroSection } from "@/components/sections/HeroSection";
import { FeaturesSection } from "@/components/sections/FeaturesSection";
import { ScreenshotsSection } from "@/components/sections/ScreenshotsSection";
import { TestimonialsSection } from "@/components/sections/TestimonialsSection";


export function HomePage() {
  return (
    <>
      <HeroSection />
      <FeaturesSection />
      <ScreenshotsSection />
      {/* <TutorialSection /> */}
      <TestimonialsSection />
    </>
  );
}
