"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sidebar } from "@/components/ui/sidebar";
import { Users, Phone, Mail, Plus, Search } from "lucide-react";

const clients = [
  { id: 1, name: "TechSolutions SA", contact: "Carlos López", email: "carlos@techsolutions.com", phone: "+52 55 1234 5678", status: "activo", lastContact: "2026-06-14", deals: 12 },
  { id: 2, name: "Innovación Digital", contact: "María García", email: "maria@innovacion.digital", phone: "+52 55 8765 4321", status: "activo", lastContact: "2026-06-13", deals: 8 },
  { id: 3, name: "Grupo Empresarial MX", contact: "Juan Pérez", email: "juan@grupoempresarial.mx", phone: "+52 55 2468 1357", status: "lead", lastContact: "2026-06-10", deals: 0 },
  { id: 4, name: "Consultoría Estratégica", contact: "Ana Martínez", email: "ana@consultoria.com", phone: "+52 55 1357 2468", status: "inactivo", lastContact: "2026-05-20", deals: 3 },
  { id: 5, name: "DataCloud Systems", contact: "Roberto Sánchez", email: "roberto@datacloud.io", phone: "+52 55 9876 5432", status: "activo", lastContact: "2026-06-14", deals: 25 },
];

export default function ClientesPage() {
  return (
    <Sidebar>
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Clientes</h1>
            <p className="text-sm text-muted-foreground">Gestión de relaciones con clientes (CRM)</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm">
              <Search className="mr-2 h-4 w-4" />
              Buscar
            </Button>
            <Button size="sm">
              <Plus className="mr-2 h-4 w-4" />
              Nuevo cliente
            </Button>
          </div>
        </div>

        <Card>
          <CardContent className="p-0">
            <div className="divide-y">
              {clients.map((client) => (
                <div key={client.id} className="flex items-center justify-between p-4 hover:bg-muted/50 transition-colors">
                  <div className="flex items-center gap-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-blue-600 font-semibold">
                      {client.name.charAt(0)}
                    </div>
                    <div>
                      <p className="font-medium">{client.name}</p>
                      <p className="text-xs text-muted-foreground">{client.contact}</p>
                    </div>
                  </div>
                  <div className="hidden md:flex items-center gap-4 text-xs text-muted-foreground">
                    <span className="flex items-center gap-1"><Mail className="h-3 w-3" />{client.email}</span>
                    <span className="flex items-center gap-1"><Phone className="h-3 w-3" />{client.phone}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-xs text-muted-foreground">{client.deals} negocios</span>
                    <Badge variant={client.status === "activo" ? "success" : client.status === "lead" ? "warning" : "secondary"}>
                      {client.status}
                    </Badge>
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
