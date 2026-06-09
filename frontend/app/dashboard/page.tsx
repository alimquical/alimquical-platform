"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sidebar } from "@/components/ui/sidebar";
import { useTranslation } from "@/lib/i18n";
import {
  Calendar,
  Users,
  FileText,
  TrendingUp,
  Clock,
  CheckCircle2,
  AlertCircle,
  Bot,
  ArrowUpRight,
  Plus,
} from "lucide-react";

const stats = [
  { key: "stats_meetings", value: "24", change: "+12%", icon: Calendar, color: "text-blue-600 bg-blue-100" },
  { key: "stats_clients", value: "156", change: "+8%", icon: Users, color: "text-green-600 bg-green-100" },
  { key: "stats_documents", value: "342", change: "+23%", icon: FileText, color: "text-purple-600 bg-purple-100" },
  { key: "stats_tasks", value: "89", change: "+18%", icon: CheckCircle2, color: "text-orange-600 bg-orange-100" },
];

const recentMeetings = [
  { id: 1, title: "Revisión trimestral Q2", date: { key: "today", time: "10:00" }, participants: 8, status: "completed" },
  { id: 2, title: "Sprint planning - Equipo Dev", date: { key: "today", time: "14:00" }, participants: 6, status: "scheduled" },
  { id: 3, title: "Presentación cliente nuevo", date: { key: "tomorrow", time: "09:00" }, participants: 4, status: "scheduled" },
  { id: 4, title: "Comité de calidad ISO 9001", date: { key: "yesterday", time: "11:00" }, participants: 12, status: "completed" },
];

const agents = [
  { name: "CEA - Director Ejecutivo", status: "active", tasks: 145, icon: Bot },
  { name: "Secretario de Reuniones", status: "active", tasks: 89, icon: Clock },
  { name: "Analista de Negocios", status: "active", tasks: 67, icon: TrendingUp },
  { name: "Agente CRM", status: "active", tasks: 234, icon: Users },
  { name: "Agente Legal", status: "inactive", tasks: 12, icon: AlertCircle },
  { name: "Agente Financiero", status: "active", tasks: 56, icon: TrendingUp },
];

export default function DashboardPage() {
  const { t } = useTranslation();

  return (
    <Sidebar>
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">{t("dashboard.title")}</h1>
            <p className="text-sm text-muted-foreground">{t("dashboard.welcome")}</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm">
              <Clock className="mr-2 h-4 w-4" />
              {t("dashboard.history")}
            </Button>
            <Button size="sm">
              <Plus className="mr-2 h-4 w-4" />
              {t("dashboard.new_meeting")}
            </Button>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat) => (
            <Card key={stat.key}>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div className={stat.color + " rounded-lg p-2"}>
                    <stat.icon className="h-5 w-5" />
                  </div>
                  <span className="flex items-center text-xs text-green-600 font-medium">
                    {stat.change}
                    <ArrowUpRight className="ml-1 h-3 w-3" />
                  </span>
                </div>
                <div className="mt-4">
                  <p className="text-2xl font-bold">{stat.value}</p>
                  <p className="text-xs text-muted-foreground">{t("dashboard." + stat.key)}</p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">{t("dashboard.recent_meetings")}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentMeetings.map((meeting) => (
                  <div key={meeting.id} className="flex items-center justify-between border-b pb-3 last:border-0 last:pb-0">
                    <div className="flex-1">
                      <p className="text-sm font-medium">{meeting.title}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-xs text-muted-foreground">{t("common." + meeting.date.key)}, {meeting.date.time}</span>
                        <span className="text-xs text-muted-foreground">•</span>
                        <span className="text-xs text-muted-foreground">{meeting.participants} {t("dashboard.participants")}</span>
                      </div>
                    </div>
                    <Badge variant={meeting.status === "completed" ? "success" : "secondary"}>
                      {meeting.status === "completed" ? t("meetings.completed") : t("meetings.scheduled")}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">{t("dashboard.agents_status")}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {agents.map((agent) => (
                  <div key={agent.name} className="flex items-center justify-between rounded-lg border p-3">
                    <div className="flex items-center gap-3">
                      <div className="rounded-lg bg-blue-100 p-2">
                        <agent.icon className="h-4 w-4 text-blue-600" />
                      </div>
                      <div>
                        <p className="text-sm font-medium">{agent.name}</p>
                        <p className="text-xs text-muted-foreground">{agent.tasks} {t("dashboard.tasks")}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`h-2 w-2 rounded-full ${agent.status === "active" ? "bg-green-500" : "bg-gray-300"}`} />
                      <span className="text-xs capitalize">{agent.status === "active" ? t("clients.active") : t("clients.inactive")}</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </Sidebar>
  );
}
