"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Sidebar } from "@/components/ui/sidebar";
import { useTranslation } from "@/lib/i18n";
import { Bell, MessageSquare, CheckCheck, Settings } from "lucide-react";

const notifications = [
  { id: 1, title: "Reunión en 30 minutos", message: "Revisión trimestral Q2 comienza en 30 min", type: "recordatorio", time: { key: "min_ago", n: 5 }, read: false },
  { id: 2, title: "Nuevo cliente registrado", message: "TechSolutions SA se ha registrado en la plataforma", type: "sistema", time: { key: "min_ago", n: 15 }, read: false },
  { id: 3, title: "Tarea completada", message: "María completó 'Revisar contrato proveedor'", type: "tarea", time: { key: "hour_ago", n: 1 }, read: false },
  { id: 4, title: "Acta de reunión lista", message: "El acta de 'Comité de calidad' ya está disponible", type: "documento", time: { key: "hours_ago", n: 2 }, read: true },
  { id: 5, title: "Mensaje de WhatsApp", message: "Cliente: ¿Podemos agendar una reunión?", type: "whatsapp", time: { key: "hours_ago", n: 3 }, read: true },
  { id: 6, title: "Recordatorio de pago", message: "Tu suscripción Business se renovará en 7 días", type: "sistema", time: { key: "yesterday", n: 0 }, read: true },
];

const notificationsList = [
  { id: 1, title: "Reunión en 30 minutos", message: "Revisión trimestral Q2 comienza en 30 min", type: "recordatorio", read: false },
  { id: 2, title: "Nuevo cliente registrado", message: "TechSolutions SA se ha registrado en la plataforma", type: "sistema", read: false },
  { id: 3, title: "Tarea completada", message: "María completó 'Revisar contrato proveedor'", type: "tarea", read: false },
  { id: 4, title: "Acta de reunión lista", message: "El acta de 'Comité de calidad' ya está disponible", type: "documento", read: true },
  { id: 5, title: "Mensaje de WhatsApp", message: "Cliente: ¿Podemos agendar una reunión?", type: "whatsapp", read: true },
  { id: 6, title: "Recordatorio de pago", message: "Tu suscripción Business se renovará en 7 días", type: "sistema", read: true },
];

const getIcon = (type: string) => {
  switch (type) {
    case "whatsapp": return MessageSquare;
    case "tarea": return CheckCheck;
    default: return Bell;
  }
};

const getColor = (type: string) => {
  switch (type) {
    case "whatsapp": return "text-green-600 bg-green-100";
    case "recordatorio": return "text-blue-600 bg-blue-100";
    case "sistema": return "text-purple-600 bg-purple-100";
    default: return "text-gray-600 bg-gray-100";
  }
};

export default function NotificacionesPage() {
  const { t } = useTranslation();
  return (
    <Sidebar>
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">{t("notifications.title")}</h1>
            <p className="text-sm text-muted-foreground">{t("notifications.subtitle")}</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm">
              <CheckCheck className="mr-2 h-4 w-4" />
              {t("notifications.mark_read")}
            </Button>
            <Button variant="outline" size="sm">
              <Settings className="mr-2 h-4 w-4" />
              {t("notifications.configure")}
            </Button>
          </div>
        </div>
        <div className="space-y-2">
          {notificationsList.map((n) => {
            const Icon = getIcon(n.type);
            const color = getColor(n.type);
            return (
              <Card key={n.id} className={`hover:shadow-md transition-shadow ${!n.read ? "border-l-4 border-l-blue-500" : ""}`}>
                <CardContent className="p-4">
                  <div className="flex items-start gap-4">
                    <div className={`rounded-lg p-2 ${color}`}>
                      <Icon className="h-5 w-5" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium">{n.title}</p>
                        <span className="text-xs text-muted-foreground">-</span>
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">{n.message}</p>
                    </div>
                    {!n.read && <div className="h-2 w-2 rounded-full bg-blue-500 mt-2" />}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </Sidebar>
  );
}
