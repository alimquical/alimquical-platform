"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sidebar } from "@/components/ui/sidebar";
import { Calendar, Clock, Plus, ChevronLeft, ChevronRight } from "lucide-react";

const events = [
  { id: 1, title: "Revisión trimestral Q2", time: "10:00 - 11:30", type: "reunión", date: "Hoy" },
  { id: 2, title: "Sprint planning - Equipo Dev", time: "14:00 - 15:00", type: "reunión", date: "Hoy" },
  { id: 3, title: "Presentación cliente nuevo", time: "09:00 - 09:45", type: "reunión", date: "Mañana" },
  { id: 4, title: "Corte de nómina", time: "Todo el día", type: "deadline", date: "18 jun" },
  { id: 5, title: "Comité de calidad", time: "11:00 - 13:00", type: "reunión", date: "19 jun" },
  { id: 6, title: "Entrega reporte mensual", time: "17:00", type: "deadline", date: "20 jun" },
];

export default function AgendaPage() {
  return (
    <Sidebar>
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Agenda</h1>
            <p className="text-sm text-muted-foreground">Calendario y programación de eventos</p>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="icon"><ChevronLeft className="h-4 w-4" /></Button>
            <span className="text-sm font-medium">Junio 2026</span>
            <Button variant="outline" size="icon"><ChevronRight className="h-4 w-4" /></Button>
            <Button size="sm"><Plus className="mr-2 h-4 w-4" />Nuevo evento</Button>
          </div>
        </div>

        <div className="grid gap-6 lg:grid-cols-7">
          {["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"].map((day) => (
            <div key={day} className="text-center text-xs font-medium text-muted-foreground p-2">{day}</div>
          ))}
          {Array.from({ length: 30 }, (_, i) => i + 1).map((d) => (
            <div key={d} className={`min-h-20 rounded-lg border p-1 text-xs ${d === 15 ? "bg-blue-50 border-blue-200" : ""}`}>
              <span className={`inline-flex h-6 w-6 items-center justify-center rounded-full ${d === 15 ? "bg-blue-600 text-white" : ""}`}>{d}</span>
              {d === 15 && <div className="mt-1 rounded bg-blue-100 px-1 py-0.5 text-blue-700">Revisión Q2</div>}
              {d === 16 && <div className="mt-1 rounded bg-green-100 px-1 py-0.5 text-green-700">Presentación</div>}
            </div>
          ))}
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Eventos del día</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {events.filter(e => e.date === "Hoy").map((event) => (
                <div key={event.id} className="flex items-center gap-4 rounded-lg border p-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-100">
                    <Calendar className="h-5 w-5 text-blue-600" />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">{event.title}</p>
                    <p className="text-xs text-muted-foreground flex items-center gap-1"><Clock className="h-3 w-3" />{event.time}</p>
                  </div>
                  <Badge variant="secondary">{event.type}</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </Sidebar>
  );
}
