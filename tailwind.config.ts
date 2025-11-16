import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        "apple-gray": "#1d1d1f",
        "apple-blue": "#0071e3",
        "apple-light": "#f5f5f7",
        "apple-dark": "#000000"
      },
      fontFamily: {
        sans: [
          "SF Pro Display",
          "SF Pro Text",
          "Helvetica Neue",
          "Helvetica",
          "Arial",
          "sans-serif"
        ]
      },
      boxShadow: {
        "soft-lg":
          "0 20px 45px rgba(0, 0, 0, 0.2), 0 12px 24px rgba(0, 0, 0, 0.12)"
      }
    }
  },
  plugins: []
};

export default config;

