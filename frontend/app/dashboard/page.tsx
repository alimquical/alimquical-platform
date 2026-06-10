"use client";

import { useState, useEffect } from "react";
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

interface Overview {
  meetings: { total: number; pending: number; recent_today: number };
  tasks: { total: number; active: number; overdue: number };
  clients: { total: number; active: number };
  documents: { total: number };
  company: { name: string; plan: string };
}

interface Activity {
  id: string; type: string; title: string; date: string;
  status: string; participants: string;
}

interface TaskItem {
  id: string; title: string; status: string;
  priority: string; due_date: string | null;
}

interface CalendarEvent {
  id: string; title: string; date: string;
  duration: number; participants: string;
}

interface Alert {
  type: string; message: string;
}

export default function DashboardPage() {
  const { t } = useTranslation();
  const [overview, setOverview] = useState<Overview | null>(null);
  const [activity, setActivity] = useState<Activity[]>([]);
  const [tasks, setTasks] = useState<TaskItem[]>([]);
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) return;

    const fetchData = async () => {
      try {
        const [overviewRes, activityRes, tasksRes, calRes, notifRes] = await Promise.all([
          fetch("/api/dashboard/overview", { headers: { Authorization: `Bearer ${token}` } }),
          fetch("/api/dashboard/activity", { headers: { Authorization: `Bearer ${token}` } }),
          fetch("/api/dashboard/tasks", { headers: { Authorization: `Bearer ${token}` } }),
          fetch("/api/dashboard/calendar", { headers: { Authorization: `Bearer ${token}` } }),
          fetch("/api/dashboard/notifications", { headers: { Authorization: `Bearer ${token}` } }),
        ]);
        if (overviewRes.ok) setOverview(await overviewRes.json());
        if (activityRes.ok) setActivity(await activityRes.json());
        if (tasksRes.ok) setTasks(await tasksRes.json());
        if (calRes.ok) setEvents(await calRes.json());
        if (notifRes.ok) setAlerts(await notifRes.json());
      } catch {
        setError(t("dashboard.error_loading"));
      }
    };
    fetchData();
  }, [t]);

  const stats = overview ? [
    { key: "stats_meetings", value: String(overview.meetings.total), change: `${overview.meetings.pending} pendientes`, icon: Calendar, color: "text-blue-600 bg-blue-100" },
    { key: "stats_clients", value: String(overview.clients.active), change: `${overview.clients.total} totales`, icon: Users, color: "text-green-600 bg-green-100" },
    { key: "stats_documents", value: String(overview.documents.total), change: "", icon: FileText, color: "text-purple-600 bg-purple-100" },
    { key: "stats_tasks", value: String(overview.tasks.active), change: `${overview.tasks.overdue} vencidas`, icon: CheckCircle2, color: "text-orange-600 bg-orange-100" },
  ] : [];

  return (
    <Sidebar>
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">{t("dashboard.title")}</h1>
            <p className="text-sm text-muted-foreground">
              {overview ? `${overview.company.name} • ${overview.company.plan}` : t("dashboard.welcome")}
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={() => window.location.href = "/agenda"}>
              <Clock className="mr-2 h-4 w-4" />
              {t("dashboard.history")}
            </Button>
            <Button size="sm" onClick={() => window.location.href = "/reuniones"}>
              <Plus className="mr-2 h-4 w-4" />
              {t("dashboard.new_meeting")}
            </Button>
          </div>
        </div>

        {alerts.map((alert, i) => (
          <div key={i} className={`flex items-center gap-2 rounded-lg border px-4 py-2 text-sm ${
            alert.type === "warning" ? "bg-yellow-50 border-yellow-200 text-yellow-800" : "bg-blue-50 border-blue-200 text-blue-800"
          }`}>
            <AlertCircle className="h-4 w-4" />
            {alert.message}
          </div>
        ))}

        {error && (
          <div className="rounded-lg bg-red-50 border border-red-200 px-4 py-2 text-sm text-red-700">
            {error}
          </div>
        )}

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat) => (
            <Card key={stat.key}>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div className={stat.color + " rounded-lg p-2"}>
                    <stat.icon className="h-5 w-5" />
                  </div>
                  {stat.change && (
                    <span className="flex items-center text-xs text-green-600 font-medium">
                      {stat.change}
                      <ArrowUpRight className="ml-1 h-3 w-3" />
                    </span>
                  )}
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
              {activity.length === 0 ? (
                <p className="text-sm text-muted-foreground">{t("dashboard.no_meetings")}</p>
              ) : (
                <div className="space-y-4">
                  {activity.map((item) => (
                    <div key={item.id} className="flex items-center justify-between border-b pb-3 last:border-0 last:pb-0">
                      <div className="flex-1">
                        <p className="text-sm font-medium">{item.title}</p>
                        <div className="flex items-center gap-2 mt-1">
                          <span className="text-xs text-muted-foreground">{new Date(item.date).toLocaleDateString()}</span>
                          <span className="text-xs text-muted-foreground">•</span>
                          <span className="text-xs text-muted-foreground">{item.participants || "0"} {t("dashboard.participants")}</span>
                        </div>
                      </div>
                      <Badge variant={item.status === "completed" ? "success" : "secondary"}>
                        {item.status === "completed" ? t("meetings.completed") : t("meetings.scheduled")}
                      </Badge>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">{t("dashboard.upcoming_events")}</CardTitle>
            </CardHeader>
            <CardContent>
              {events.length === 0 ? (
                <p className="text-sm text-muted-foreground">{t("dashboard.no_events")}</p>
              ) : (
                <div className="space-y-4">
                  {events.map((ev) => (
                    <div key={ev.id} className="flex items-center justify-between rounded-lg border p-3">
                      <div className="flex items-center gap-3">
                        <div className="rounded-lg bg-blue-100 p-2">
                          <Calendar className="h-4 w-4 text-blue-600" />
                        </div>
                        <div>
                          <p className="text-sm font-medium">{ev.title}</p>
                          <p className="text-xs text-muted-foreground">
                            {new Date(ev.date).toLocaleDateString()} • {ev.duration}min
                          </p>
                        </div>
                      </div>
                      <Badge variant="outline">{ev.participants || "0"} {t("dashboard.participants")}</Badge>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">{t("dashboard.active_tasks")}</CardTitle>
          </CardHeader>
          <CardContent>
            {tasks.length === 0 ? (
              <p className="text-sm text-muted-foreground">{t("dashboard.no_tasks")}</p>
            ) : (
              <div className="space-y-3">
                {tasks.map((task) => (
                  <div key={task.id} className="flex items-center justify-between rounded-lg border p-3">
                    <div className="flex items-center gap-3">
                      <div className={`rounded-lg p-2 ${
                        task.priority === "high" ? "bg-red-100" : task.priority === "medium" ? "bg-yellow-100" : "bg-gray-100"
                      }`}>
                        <CheckCircle2 className={`h-4 w-4 ${
                          task.priority === "high" ? "text-red-600" : task.priority === "medium" ? "text-yellow-600" : "text-gray-600"
                        }`} />
                      </div>
                      <div>
                        <p className="text-sm font-medium">{task.title}</p>
                        <p className="text-xs text-muted-foreground">
                          {task.due_date ? `${t("dashboard.due")}: ${new Date(task.due_date).toLocaleDateString()}` : t("dashboard.no_due")}
                        </p>
                      </div>
                    </div>
                    <Badge variant={task.status === "done" ? "success" : task.status === "in_progress" ? "secondary" : "outline"}>
                      {task.status === "done" ? t("tasks.done") : task.status === "in_progress" ? t("tasks.in_progress") : t("tasks.todo")}
                    </Badge>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </Sidebar>
  );
}
