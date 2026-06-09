"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sidebar } from "@/components/ui/sidebar";
import { useTranslation } from "@/lib/i18n";
import { User, Building, Bell, Shield, CreditCard, Palette, Globe, Key } from "lucide-react";

const sections = [
  { id: "profile", titleKey: "profile", descKey: "profile_desc", icon: User },
  { id: "company", titleKey: "company", descKey: "company_desc", icon: Building },
  { id: "notifications", titleKey: "notifications", descKey: "notifications_desc", icon: Bell },
  { id: "security", titleKey: "security", descKey: "security_desc", icon: Shield },
  { id: "subscription", titleKey: "subscription", descKey: "subscription_desc", icon: CreditCard },
  { id: "appearance", titleKey: "appearance", descKey: "appearance_desc", icon: Palette },
  { id: "agents", titleKey: "agents", descKey: "agents_desc", icon: Globe },
  { id: "api_keys", titleKey: "api_keys", descKey: "api_keys_desc", icon: Key },
];

export default function ConfiguracionPage() {
  const { t } = useTranslation();
  return (
    <Sidebar>
      <div className="p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold">{t("settings.title")}</h1>
          <p className="text-sm text-muted-foreground">{t("settings.subtitle")}</p>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {sections.map((section) => (
            <Card key={section.id} className="hover:shadow-md transition-shadow cursor-pointer">
              <CardContent className="p-5">
                <div className="rounded-lg bg-blue-100 p-2 w-fit">
                  <section.icon className="h-5 w-5 text-blue-600" />
                </div>
                <p className="mt-3 font-medium">{t("settings." + section.titleKey)}</p>
                <p className="text-xs text-muted-foreground mt-1">{t("settings." + section.descKey)}</p>
              </CardContent>
            </Card>
          ))}
        </div>
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">{t("settings.current_plan")}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-lg">Plan Business</p>
                <p className="text-sm text-muted-foreground">500 reuniones/mes • 10 usuarios • Soporte prioritario</p>
              </div>
              <div className="flex items-center gap-3">
                <Badge variant="success" className="text-sm">{t("settings.active")}</Badge>
                <Button variant="outline" size="sm">{t("settings.change_plan")}</Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </Sidebar>
  );
}
