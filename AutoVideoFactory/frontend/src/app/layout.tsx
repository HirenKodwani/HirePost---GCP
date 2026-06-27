import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AutoVideoFactory",
  description: "Enterprise-grade autonomous AI video generation platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>
        <div className="flex h-screen overflow-hidden">
          <Sidebar />
          <main className="flex-1 overflow-y-auto p-6">{children}</main>
        </div>
      </body>
    </html>
  );
}

function Sidebar() {
  const links = [
    { href: "/", label: "Dashboard", icon: "LayoutDashboard" },
    { href: "/projects", label: "Projects", icon: "FolderKanban" },
    { href: "/queue", label: "Queue", icon: "ListOrdered" },
    { href: "/agents", label: "Agents", icon: "Bot" },
    { href: "/browser", label: "Browser", icon: "Globe" },
    { href: "/analytics", label: "Analytics", icon: "BarChart3" },
    { href: "/settings", label: "Settings", icon: "Settings" },
  ];

  return (
    <aside className="w-64 border-r border-border bg-card p-4 flex flex-col gap-2">
      <div className="text-xl font-bold mb-6 px-2 text-primary">AVF</div>
      <nav className="flex flex-col gap-1">
        {links.map((link) => (
          <a
            key={link.href}
            href={link.href}
            className="flex items-center gap-3 px-3 py-2 rounded-md text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
          >
            <span className="w-5 h-5">{getIcon(link.icon)}</span>
            <span className="text-sm">{link.label}</span>
          </a>
        ))}
      </nav>
    </aside>
  );
}

function getIcon(name: string) {
  const icons: Record<string, string> = {
    LayoutDashboard: "\u2302",
    FolderKanban: "\u2630",
    ListOrdered: "\u2261",
    Bot: "\u2699",
    Globe: "\u25C9",
    BarChart3: "\u2261",
    Settings: "\u2699",
  };
  return icons[name] || "\u2022";
}
