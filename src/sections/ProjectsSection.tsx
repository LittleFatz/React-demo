import { FC } from "react";
import { projects } from "../data/projects";

const ProjectsSection: FC = () => (
  <section
    id="projects"
    className="mx-auto max-w-6xl px-6 py-24 text-apple-gray"
  >
    <div className="flex flex-col gap-6 pb-12">
      <span className="text-sm uppercase tracking-[0.4em] text-apple-gray/60">
        Projects
      </span>
      <h2 className="text-3xl font-semibold tracking-[-0.02em] md:text-4xl">
        精选项目
      </h2>
      <p className="max-w-2xl text-base text-apple-gray/70 md:text-lg">
        从系统体验到品牌叙事，每一个项目都以极致细节打造难忘体验。
      </p>
    </div>

    <div className="grid gap-8 md:grid-cols-3">
      {projects.map((project) => (
        <article
          key={project.id}
          className="flex flex-col gap-4 rounded-3xl border border-white/70 bg-white/90 p-8 shadow-soft-lg backdrop-blur"
        >
          <div className="text-sm uppercase tracking-[0.3em] text-apple-gray/50">
            {project.year}
          </div>
          <h3 className="text-2xl font-semibold tracking-[-0.02em]">
            {project.name}
          </h3>
          <p className="text-base text-apple-gray/70">{project.description}</p>
          <p className="text-sm text-apple-gray/60">{project.role}</p>
          <p className="text-xs text-apple-blue/90">{project.highlight}</p>
        </article>
      ))}
    </div>
  </section>
);

export default ProjectsSection;

