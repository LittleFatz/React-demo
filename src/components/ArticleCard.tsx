import { FC } from "react";
import type { Article } from "../data/articles";

type ArticleCardProps = {
  article: Article;
};

const ArticleCard: FC<ArticleCardProps> = ({ article }) => (
  <article className="group relative overflow-hidden rounded-3xl bg-white p-8 shadow-soft-lg transition-transform hover:-translate-y-1">
    <div className="absolute inset-0 bg-gradient-to-br from-white via-transparent to-white/60 opacity-0 transition-opacity duration-500 group-hover:opacity-100" />
    <div className="relative flex flex-col gap-4">
      <div className="flex items-center gap-3 text-xs uppercase tracking-[0.32em] text-apple-blue/80">
        <span>{new Date(article.publishedAt).toLocaleDateString("zh-TW")}</span>
        <span className="text-apple-gray/30">•</span>
        <span>{article.readingTime}</span>
      </div>
      <h3 className="text-2xl font-semibold tracking-[-0.02em] text-apple-gray transition-colors group-hover:text-apple-dark">
        {article.title}
      </h3>
      <p className="text-base text-apple-gray/70">{article.summary}</p>
      <div className="flex flex-wrap gap-2">
        {article.topics.map((topic) => (
          <span
            key={topic}
            className="rounded-full bg-apple-light px-3 py-1 text-xs font-medium text-apple-gray/80"
          >
            {topic}
          </span>
        ))}
      </div>
      <a
        href="#"
        className="mt-6 flex items-center gap-2 text-sm font-semibold text-apple-blue transition-transform group-hover:translate-x-1"
      >
        {article.cta}
        <span aria-hidden>→</span>
      </a>
    </div>
  </article>
);

export default ArticleCard;

