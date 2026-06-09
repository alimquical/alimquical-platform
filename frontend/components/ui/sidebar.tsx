"use client";

import { cn } from "@/lib/utils";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Calendar,
  Users,
  Building2,
  FileText,
  CheckSquare,
  Bell,
  Settings,
  Shield,
  ChevronLeft,
  Bot,
  LogOut,
} from "lucide-react";
import { useState } from "react";
import { useTranslation } from "@/lib/i18n";
import { ThemeToggle } from "./theme-toggle";
import { LanguageToggle } from "./language-toggle";

interface SidebarProps {
  children: React.ReactNode;
}

export function Sidebar({ children }: SidebarProps) {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);
  const { t } = useTranslation();

  const navigation = [
    { name: t("nav.dashboard"), href: "/dashboard", icon: LayoutDashboard },
    { name: t("nav.reuniones"), href: "/reuniones", icon: Calendar },
    { name: t("nav.clientes"), href: "/clientes", icon: Users },
    { name: t("nav.proveedores"), href: "/proveedores", icon: Building2 },
    { name: t("nav.documentos"), href: "/documentos", icon: FileText },
    { name: t("nav.tareas"), href: "/tareas", icon: CheckSquare },
    { name: t("nav.agenda"), href: "/agenda", icon: Calendar },
    { name: t("nav.notificaciones"), href: "/notificaciones", icon: Bell },
    { name: t("nav.configuracion"), href: "/configuracion", icon: Settings },
    { name: t("nav.admin"), href: "/admin", icon: Shield },
  ];

  return (
    <div className="flex h-screen overflow-hidden">
      <aside
        className={cn(
          "flex flex-col border-r bg-sidebar text-sidebar-foreground transition-all duration-300",
          collapsed ? "w-16" : "w-64"
        )}
      >
        <div className="flex h-14 items-center justify-between border-b px-4">
          {!collapsed && (
            <Link href="/dashboard" className="flex items-center gap-2">
              <Bot className="h-6 w-6 text-blue-600" />
              <span className="font-bold text-blue-600">INTELLIWORK™</span>
            </Link>
          )}
          {collapsed && (
            <Link href="/dashboard" className="mx-auto">
              <Bot className="h-6 w-6 text-blue-600" />
            </Link>
          )}
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="rounded-lg p-1.5 hover:bg-sidebar-accent"
          >
            <ChevronLeft className={cn("h-4 w-4 transition", collapsed && "rotate-180")} />
          </button>
        </div>

        <nav className="flex-1 space-y-1 overflow-y-auto p-2">
          {navigation.map((item) => {
            const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors",
                  isActive
                    ? "bg-blue-600 text-white"
                    : "text-sidebar-foreground hover:bg-sidebar-accent",
                  collapsed && "justify-center px-2"
                )}
                title={item.name}
              >
                <item.icon className="h-4 w-4 shrink-0" />
                {!collapsed && <span>{item.name}</span>}
              </Link>
            );
          })}
        </nav>

        <div className="border-t p-2 space-y-1">
          <LanguageToggle collapsed={collapsed} />
          <div className={cn("flex items-center", collapsed ? "justify-center" : "justify-between px-3")}>
            {!collapsed && <span className="text-xs text-sidebar-foreground/60">{t("nav.dashboard") === "Dashboard" ? "Theme" : "Tema"}</span>}
            <ThemeToggle collapsed={collapsed} />
          </div>
          <button
            className={cn(
              "flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-sidebar-foreground hover:bg-sidebar-accent",
              collapsed && "justify-center px-2"
            )}
          >
            <LogOut className="h-4 w-4 shrink-0" />
            {!collapsed && <span>{t("nav.logout")}</span>}
          </button>
        </div>
      </aside>

      <main className="flex-1 overflow-y-auto bg-background">
        {children}
      </main>
    </div>
  );
}
