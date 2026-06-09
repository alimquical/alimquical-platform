"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useTranslation } from "@/lib/i18n";
import { useTheme } from "next-themes";
import { Sun, Moon, Languages } from "lucide-react";
import { useEffect } from "react";

export default function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [company, setCompany] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const { t, locale, setLocale } = useTranslation();
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password, company_name: company }),
      });
      if (res.ok) {
        router.push("/login");
      }
    } catch {
      // handle error
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-600 to-blue-900 p-4 relative">
      <div className="absolute top-4 right-4 flex items-center gap-2">
        {mounted && (
          <button
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="rounded-lg bg-white/10 p-2 text-white hover:bg-white/20 transition-colors"
          >
            {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </button>
        )}
        <button
          onClick={() => setLocale(locale === "es" ? "en" : "es")}
          className="rounded-lg bg-white/10 px-2 py-2 text-xs font-medium text-white hover:bg-white/20 transition-colors"
        >
          <Languages className="h-4 w-4 inline" /> {locale === "es" ? "EN" : "ES"}
        </button>
      </div>
      <div className="w-full max-w-md space-y-8 rounded-2xl bg-white p-8 shadow-2xl">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-blue-600">INTELLIWORK™</h1>
          <p className="mt-2 text-sm text-gray-600">{t("auth.create_account_title")}</p>
        </div>
        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">{t("auth.full_name")}</label>
              <input type="text" value={name} onChange={(e) => setName(e.target.value)}
                className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                placeholder={t("auth.name_placeholder")} required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">{t("auth.email")}</label>
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)}
                className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                placeholder={t("auth.email_placeholder")} required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">{t("auth.company")}</label>
              <input type="text" value={company} onChange={(e) => setCompany(e.target.value)}
                className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                placeholder={t("auth.company_placeholder")} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">{t("auth.password")}</label>
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                placeholder="••••••••" required />
            </div>
          </div>
          <button type="submit" disabled={loading}
            className="w-full rounded-lg bg-blue-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:opacity-50">
            {loading ? t("auth.create_account_loading") : t("auth.create_account")}
          </button>
          <p className="text-center text-sm text-gray-600">
            {t("auth.has_account")}{" "}
            <Link href="/login" className="font-medium text-blue-600 hover:text-blue-500">{t("auth.login")}</Link>
          </p>
        </form>
      </div>
    </div>
  );
}
