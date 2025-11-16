import { FC } from "react";
import { Link, useLocation } from "react-router-dom";

const links = [
  { label: "文章", path: "/", hash: "#articles" },
  { label: "项目", path: "/projects" },
  { label: "关于我", path: "/", hash: "#about" }
];

const NavBar: FC = () => {
  const location = useLocation();

  return (
    <header className="sticky top-0 z-50 backdrop-blur bg-apple-light/70 border-b border-white/40">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link
          to="/"
          className="text-lg font-semibold tracking-tight text-apple-gray"
        >
          Lin.S – Visionary Designer
        </Link>
        <div className="hidden gap-8 text-sm text-apple-gray/80 md:flex">
          {links.map((link) => {
            const isActive = location.pathname === link.path && !link.hash;
            const handleClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
              if (link.hash && location.pathname === link.path) {
                e.preventDefault();
                const element = document.querySelector(link.hash);
                if (element) {
                  element.scrollIntoView({ behavior: "smooth" });
                }
              }
            };
            
            return (
              <Link
                key={link.label}
                to={link.hash ? `${link.path}${link.hash}` : link.path}
                onClick={handleClick}
                className={`transition-colors ${
                  isActive ? "text-apple-gray" : "hover:text-apple-gray"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </div>
        <a
          className="rounded-full bg-apple-dark px-4 py-2 text-xs font-medium uppercase tracking-[0.2em] text-white transition-transform hover:scale-105"
          href="#contact"
        >
          联系我
        </a>
      </nav>
    </header>
  );
};

export default NavBar;

