import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "#0f172a", // Deep dark
                card: "#1e293b",       // Card background
                accent: {
                    DEFAULT: "#f59e0b", // Gold
                    hover: "#d97706",
                },
                text: {
                    DEFAULT: "#f8fafc",
                    muted: "#94a3b8",
                },
            },
        },
    },
    plugins: [],
};
export default config;
