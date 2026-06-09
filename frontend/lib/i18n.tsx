"use client";

import { createContext, useContext, useState, useCallback, type ReactNode } from "react";

type Locale = "es" | "en";

const messages: Record<Locale, Record<string, any>> = {
  es: require("@/locales/es.json"),
  en: require("@/locales/en.json"),
};

interface I18nContext {
  locale: Locale;
  setLocale: (l: Locale) => void;
  t: (key: string, params?: Record<string, string | number>) => string;
}

const I18nCtx = createContext<I18nContext>({
  locale: "es",
  setLocale: () => {},
  t: () => "",
});

function resolve(obj: any, path: string): string | undefined {
  return path.split(".").reduce((acc, part) => acc?.[part], obj);
}

export function I18nProvider({ children }: { children: ReactNode }) {
  const [locale, setLocale] = useState<Locale>("es");

  const t = useCallback(
    (key: string, params?: Record<string, string | number>): string => {
      let val = resolve(messages[locale], key);
      if (!val) val = resolve(messages["es"], key);
      if (!val) return key;
      if (params) {
        for (const [k, v] of Object.entries(params)) {
          val = val.replace(`{${k}}`, String(v));
        }
      }
      return val;
    },
    [locale]
  );

  return (
    <I18nCtx.Provider value={{ locale, setLocale, t }}>
      {children}
    </I18nCtx.Provider>
  );
}

export function useTranslation() {
  return useContext(I18nCtx);
}
