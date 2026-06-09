"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sidebar } from "@/components/ui/sidebar";
import { useTranslation } from "@/lib/i18n";
import { Building2, Phone, Mail, Plus, Search, Star } from "lucide-react";

const suppliers = [
  { id: 1, name: "Cloud Services MX", contact: "Pedro Ramírez", email: "pedro@cloudservices.mx", phone: "+52 55 1111 2222", category: "Tecnología", rating: 4.8, status: "active" },
  { id: 2, name: "Consultoría Legal ABC", contact: "Lic. Laura Torres", email: "laura@legalabc.com", phone: "+52 55 3333 4444", category: "Legal", rating: 4.5, status: "active" },
  { id: 3, name: "Soluciones Contables Fiscales", contact: "CP. Jorge Núñez", email: "jorge@solcontables.com", phone: "+52 55 5555 6666", category: "Contabilidad", rating: 4.2, status: "active" },
  { id: 4, name: "Marketing Digital Pro", contact: "Sofía Herrera", email: "sofia@marketingpro.io", phone: "+52 55 7777 8888", category: "Marketing", rating: 4.0, status: "inactive" },
];

export default function ProveedoresPage() {
  const { t } = useTranslation();
  return (
    <Sidebar>
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">{t("suppliers.title")}</h1>
            <p className="text-sm text-muted-foreground">{t("suppliers.subtitle")}</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm"><Search className="mr-2 h-4 w-4" />{t("suppliers.search")}</Button>
            <Button size="sm"><Plus className="mr-2 h-4 w-4" />{t("suppliers.new")}</Button>
          </div>
        </div>
        <Card>
          <CardContent className="p-0">
            <div className="divide-y">
              {suppliers.map((s) => (
                <div key={s.id} className="flex items-center justify-between p-4 hover:bg-muted/50 transition-colors">
                  <div className="flex items-center gap-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-purple-100 text-purple-600 font-semibold">{s.name.charAt(0)}</div>
                    <div>
                      <p className="font-medium">{s.name}</p>
                      <p className="text-xs text-muted-foreground">{s.contact}</p>
                      <div className="flex items-center gap-3 mt-1 text-xs text-muted-foreground">
                        <span className="flex items-center gap-1"><Mail className="h-3 w-3" />{s.email}</span>
                        <span className="flex items-center gap-1"><Phone className="h-3 w-3" />{s.phone}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="text-right">
                      <div className="flex items-center gap-1 text-xs">
                        <Star className="h-3 w-3 text-yellow-500 fill-yellow-500" />
                        <span>{s.rating}</span>
                      </div>
                      <Badge variant="secondary" className="text-xs mt-1">{s.category}</Badge>
                    </div>
                    <Badge variant={s.status === "active" ? "success" : "secondary"}>{s.status === "active" ? t("suppliers.active") : t("suppliers.inactive")}</Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </Sidebar>
  );
}
