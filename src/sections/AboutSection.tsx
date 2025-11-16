import { FC } from "react";

const AboutSection: FC = () => (
  <section
    id="about"
    className="relative overflow-hidden bg-white px-6 py-24 shadow-inner"
  >
    <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(0,113,227,0.12),_transparent_60%)]" />
    <div className="relative mx-auto flex max-w-6xl flex-col gap-10">
      <h2 className="text-3xl font-semibold tracking-[-0.02em] md:text-4xl">
        关于我
      </h2>
      <div className="grid gap-10 md:grid-cols-2">
        <p className="text-lg text-apple-gray/80">
          我相信设计的核心价值，是让复杂的科技变得温暖易懂。过去十年间，我协助多个新创与大型品牌完成从产品策略、界面设计到内容叙事的整体体验打造。
        </p>
        <div className="rounded-3xl bg-apple-light/60 p-8">
          <h3 className="text-sm uppercase tracking-[0.3em] text-apple-gray/60">
            专长领域
          </h3>
          <ul className="mt-4 grid gap-3 text-sm text-apple-gray/80">
            <li>产品体验与服务设计</li>
            <li>品牌定位与视觉策略</li>
            <li>内容叙事与故事设计</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
);

export default AboutSection;

