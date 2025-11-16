import { FC, useMemo } from "react";
import ArticleCard from "../components/ArticleCard";
import { articles } from "../data/articles";

const ArticlesSection: FC = () => {
  const latestArticle = useMemo(() => articles[0], []);

  return (
    <section
      id="articles"
      className="mx-auto max-w-6xl px-6 pb-24 pt-16 md:pt-24"
    >
      <div className="flex flex-col gap-6 pb-12">
        <span className="text-sm uppercase tracking-[0.4em] text-apple-gray/60">
          Latest
        </span>
        <h2 className="max-w-2xl text-3xl font-semibold tracking-[-0.02em] text-apple-gray md:text-4xl">
          设计观点与洞察
        </h2>
        <p className="max-w-2xl text-base text-apple-gray/70 md:text-lg">
          以苹果官网般的细腻感呈现，聚焦于品牌叙事、产品体验与创意策略。
          通过每篇文章，看见设计背后的思考脉络。
        </p>
      </div>

      <div className="grid gap-8 md:grid-cols-3">
        <div className="md:col-span-2">
          <ArticleCard article={latestArticle} />
        </div>
        <div className="flex flex-col gap-6 rounded-3xl bg-apple-dark p-10 text-white">
          <h3 className="text-2xl font-semibold tracking-[-0.02em]">
            创意咨询
          </h3>
          <p className="text-sm text-white/80">
            需要为品牌或产品注入全新能量？我提供端到端的设计咨询与工作坊。
          </p>
          <a
            href="#contact"
            className="inline-flex items-center gap-2 self-start rounded-full bg-white px-5 py-3 text-sm font-semibold text-apple-dark transition-transform hover:scale-105"
          >
            预约交流
            <span aria-hidden>→</span>
          </a>
        </div>
      </div>

      <div className="mt-16 grid gap-8 md:grid-cols-3">
        {articles.slice(1).map((article) => (
          <ArticleCard key={article.id} article={article} />
        ))}
      </div>
    </section>
  );
};

export default ArticlesSection;

