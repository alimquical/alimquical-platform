"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sidebar } from "@/components/ui/sidebar";
import { User, Building, Bell, Shield, CreditCard, Palette, Globe, Key } from "lucide-react";

const sections = [
  { id: "perfil", title: "Perfil", description: "Información personal y preferencias", icon: User },
  { id: "empresa", title: "Empresa", description: "Configuración de la organización", icon: Building },
  { id: "notificaciones", title: "Notificaciones", description: "Canales y preferencias de notificación", icon: Bell },
  { id: "seguridad", title: "Seguridad", description: "Contraseña y autenticación 2FA", icon: Shield },
  { id: "suscripcion", title: "Suscripción", description: "Plan actual y facturación", icon: CreditCard },
  { id: "apariencia", title: "Apariencia", description: "Tema y personalización visual", icon: Palette },
  { id: "agentes", title: "Agentes IA", description: "Configuración de agentes inteligentes", icon: Globe },
  { id: "api", title: "API Keys", description: "Tokens de acceso para integraciones", icon: Key },
];

export default function ConfiguracionPage() {
  return (
    <Sidebar>
      <div className="p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold">Configuración</h1>
          <p className="text-sm text-muted-foreground">Administra tu cuenta y preferencias</p>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {sections.map((section) => (
            <Card key={section.id} className="hover:shadow-md transition-shadow cursor-pointer">
              <CardContent className="p-5">
                <div className="rounded-lg bg-blue-100 p-2 w-fit">
                  <section.icon className="h-5 w-5 text-blue-600" />
                </div>
                <p className="mt-3 font-medium">{section.title}</p>
                <p className="text-xs text-muted-foreground mt-1">{section.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Plan actual</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-lg">Plan Business</p>
                <p className="text-sm text-muted-foreground">500 reuniones/mes • 10 usuarios • Soporte prioritario</p>
              </div>
              <div className="flex items-center gap-3">
                <Badge variant="success" className="text-sm">Activo</Badge>
                <Button variant="outline" size="sm">Cambiar plan</Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </Sidebar>
  );
}
