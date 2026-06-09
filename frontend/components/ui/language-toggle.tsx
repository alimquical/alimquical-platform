"use client";

import { useTranslation } from "@/lib/i18n";
import { Languages } from "lucide-react";

export function LanguageToggle({ collapsed }: { collapsed?: boolean }) {
  const { locale, setLocale } = useTranslation();

  return (
    <button
      onClick={() => setLocale(locale === "es" ? "en" : "es")}
      title={locale === "es" ? "English" : "Español"}
      className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-sidebar-foreground hover:bg-sidebar-accent transition-colors"
    >
      <Languages className="h-4 w-4 shrink-0" />
      {!collapsed && <span>{locale === "es" ? "EN" : "ES"}</span>}
    </button>
  );
}
