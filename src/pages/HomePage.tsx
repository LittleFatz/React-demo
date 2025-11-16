import { FC } from "react";
import Hero from "../components/Hero";
import AboutSection from "../sections/AboutSection";
import ArticlesSection from "../sections/ArticlesSection";

const HomePage: FC = () => (
  <>
    <Hero />
    <ArticlesSection />
    <AboutSection />
  </>
);

export default HomePage;

