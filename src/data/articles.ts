export type Article = {
  id: string;
  title: string;
  summary: string;
  publishedAt: string;
  readingTime: string;
  topics: string[];
  cta: string;
};

export const articles: Article[] = [
  {
    id: "design-language",
    title: "打造产品灵魂的设计语言",
    summary:
      "分享从品牌识别出发，如何建立一套一致且富有情感的设计语言，强化用户的情感连结。",
    publishedAt: "2025-07-12",
    readingTime: "阅读时间 6 分钟",
    topics: ["Design", "Branding"],
    cta: "探索设计理念"
  },
  {
    id: "crafting-experience",
    title: "专注细节，打造流畅体验",
    summary:
      "从用户旅程出发，拆解体验设计的关键细节，确保每一次互动都充满惊喜与效率。",
    publishedAt: "2025-06-27",
    readingTime: "阅读时间 8 分钟",
    topics: ["UX", "Product"],
    cta: "阅读完整文章"
  },
  {
    id: "storytelling",
    title: "用故事传递价值",
    summary:
      "谈谈内容策略如何与产品愿景呼应，通过故事引导用户理解并爱上你的产品。",
    publishedAt: "2025-05-18",
    readingTime: "阅读时间 5 分钟",
    topics: ["Storytelling", "Content"],
    cta: "了解叙事策略"
  }
];

