import { FC } from "react";

const Hero: FC = () => (
  <section className="relative overflow-hidden bg-apple-dark text-white">
    <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.18),rgba(0,0,0,0.85))]" />
    <div className="relative mx-auto flex max-w-6xl flex-col gap-8 px-6 py-24 text-balance">
      <span className="text-sm uppercase tracking-[0.4em] text-white/70">
        Creative Direction
      </span>
      <h1 className="max-w-3xl text-4xl font-semibold leading-tight tracking-[-0.03em] md:text-6xl">
        以设计的力量，将抽象愿景化为令人向往的体验。
      </h1>
      <p className="max-w-2xl text-base text-white/70 md:text-lg">
        我是 Lin，一位专注于产品体验与品牌叙事的创意设计师。灵感来自自然、科技与人文，我相信细节决定故事的深度。
      </p>
      <div className="flex flex-wrap gap-4">
        <a
          href="#articles"
          className="rounded-full bg-white px-6 py-3 text-sm font-semibold text-apple-dark transition-transform hover:scale-105"
        >
          最新洞察
        </a>
        <a
          href="#about"
          className="rounded-full border border-white/40 px-6 py-3 text-sm font-semibold text-white transition-all hover:border-white hover:bg-white/10"
        >
          认识我
        </a>
      </div>
    </div>
  </section>
);

export default Hero;

