"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sidebar } from "@/components/ui/sidebar";
import { useTranslation } from "@/lib/i18n";
import { Calendar, Clock, Plus, Mic, FileText } from "lucide-react";

const meetings = [
  { id: 1, title: "Revisión trimestral Q2", date: "2026-06-15", time: "10:00", duration: "1h 30m", participants: 8, status: "completed", summary: "Revisión de KPIs y objetivos del trimestre" },
  { id: 2, title: "Sprint planning", date: "2026-06-15", time: "14:00", duration: "1h", participants: 6, status: "scheduled" },
  { id: 3, title: "Presentación cliente nuevo", date: "2026-06-16", time: "09:00", duration: "45m", participants: 4, status: "scheduled" },
  { id: 4, title: "Comité de calidad ISO 9001", date: "2026-06-14", time: "11:00", duration: "2h", participants: 12, status: "completed", summary: "Auditoría interna programada para julio" },
  { id: 5, title: "Revisión presupuesto", date: "2026-06-14", time: "16:00", duration: "1h", participants: 3, status: "cancelled" },
];

export default function ReunionesPage() {
  const { t } = useTranslation();
  return (
    <Sidebar>
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">{t("meetings.title")}</h1>
            <p className="text-sm text-muted-foreground">{t("meetings.subtitle")}</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm">
              <Mic className="mr-2 h-4 w-4" />
              {t("meetings.record")}
            </Button>
            <Button size="sm">
              <Plus className="mr-2 h-4 w-4" />
              {t("meetings.new")}
            </Button>
          </div>
        </div>
        <Card>
          <CardContent className="p-0">
            <div className="divide-y">
              {meetings.map((meeting) => (
                <div key={meeting.id} className="flex items-center justify-between p-4 hover:bg-muted/50 transition-colors">
                  <div className="flex items-start gap-4 flex-1">
                    <div className="rounded-lg bg-blue-100 p-2 mt-1">
                      <Calendar className="h-4 w-4 text-blue-600" />
                    </div>
                    <div className="flex-1">
                      <p className="font-medium">{meeting.title}</p>
                      <div className="flex items-center gap-3 mt-1 text-xs text-muted-foreground">
                        <span className="flex items-center gap-1"><Clock className="h-3 w-3" />{meeting.time}</span>
                        <span>{meeting.date}</span>
                        <span>{meeting.duration}</span>
                        <span>{meeting.participants} {t("meetings.participants")}</span>
                      </div>
                      {meeting.summary && (
                        <p className="text-xs text-muted-foreground mt-2 italic">{meeting.summary}</p>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant={meeting.status === "completed" ? "success" : meeting.status === "scheduled" ? "secondary" : "destructive"}>
                      {meeting.status === "completed" ? t("meetings.completed") : meeting.status === "scheduled" ? t("meetings.scheduled") : t("meetings.cancelled")}
                    </Badge>
                    <Button variant="ghost" size="icon">
                      <FileText className="h-4 w-4" />
                    </Button>
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
