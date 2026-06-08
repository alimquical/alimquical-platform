"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sidebar } from "@/components/ui/sidebar";
import { CheckSquare, Plus, Clock, AlertCircle, ChevronDown, Filter } from "lucide-react";

const tasks = [
  { id: 1, title: "Preparar presentación trimestral", priority: "alta", status: "pendiente", due: "2026-06-18", assignee: "Carlos" },
  { id: 2, title: "Revisar contrato proveedor servicios", priority: "alta", status: "en_progreso", due: "2026-06-16", assignee: "María" },
  { id: 3, title: "Actualizar base de datos clientes", priority: "media", status: "pendiente", due: "2026-06-20", assignee: "Ana" },
  { id: 4, title: "Generar reporte de ventas junio", priority: "media", status: "completada", due: "2026-06-14", assignee: "Carlos" },
  { id: 5, title: "Configurar integración WhatsApp API", priority: "baja", status: "pendiente", due: "2026-06-25", assignee: "Roberto" },
  { id: 6, title: "Auditoría interna ISO 9001", priority: "alta", status: "en_progreso", due: "2026-06-17", assignee: "María" },
];

export default function TareasPage() {
  return (
    <Sidebar>
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Tareas</h1>
            <p className="text-sm text-muted-foreground">Gestión de tareas y seguimiento</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm">
              <Filter className="mr-2 h-4 w-4" />
              Filtrar
            </Button>
            <Button size="sm">
              <Plus className="mr-2 h-4 w-4" />
              Nueva tarea
            </Button>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-yellow-500" />
                Pendientes
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">3</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-blue-500" />
                En progreso
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">2</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-green-500" />
                Completadas
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">1</p>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardContent className="p-0">
            <div className="divide-y">
              {tasks.map((task) => (
                <div key={task.id} className="flex items-center justify-between p-4 hover:bg-muted/50 transition-colors">
                  <div className="flex items-start gap-3 flex-1">
                    <input type="checkbox" className="mt-1 h-4 w-4 rounded border-gray-300 text-blue-600" />
                    <div>
                      <p className={`font-medium ${task.status === "completada" ? "line-through text-muted-foreground" : ""}`}>{task.title}</p>
                      <div className="flex items-center gap-2 mt-1 text-xs text-muted-foreground">
                        <span className="flex items-center gap-1"><Clock className="h-3 w-3" />{task.due}</span>
                        <span>•</span>
                        <span>{task.assignee}</span>
                      </div>
                    </div>
                  </div>
                  <Badge variant={task.priority === "alta" ? "destructive" : task.priority === "media" ? "warning" : "secondary"}>
                    {task.priority}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </Sidebar>
  );
}
