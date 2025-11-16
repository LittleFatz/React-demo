export type Project = {
  id: string;
  name: string;
  description: string;
  role: string;
  year: string;
  highlight: string;
};

export const projects: Project[] = [
  {
    id: "aurora",
    name: "Aurora OS",
    description: "以自然光影为灵感的智能家居体验系统。",
    role: "Creative Director · 系统体验设计",
    year: "2025",
    highlight: "（概念影片入选 IF Design Award）"
  },
  {
    id: "atlas",
    name: "Atlas Mobility",
    description: "重新定义城市通勤的无缝票务与导览服务。",
    role: "Lead Designer · 产品策略",
    year: "2024",
    highlight: "（5 个月内上线 MVP）"
  },
  {
    id: "muse",
    name: "Muse Studio",
    description: "结合 AI 的创作者协作工具，强调故事叙事。",
    role: "Design Partner · 品牌叙事",
    year: "2023",
    highlight: "（提升留存率 38%）"
  }
];

