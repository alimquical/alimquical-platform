"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sidebar } from "@/components/ui/sidebar";
import { FileText, FileSpreadsheet, FileImage, File, Plus, Search, Download, Trash2 } from "lucide-react";

const documents = [
  { id: 1, name: "Reporte_Trimestral_Q2_2026.pdf", type: "pdf", size: "2.4 MB", uploaded: "2026-06-14", tags: ["reportes", "financiero"] },
  { id: 2, name: "Propuesta_Comercial_Cliente.pptx", type: "doc", size: "5.1 MB", uploaded: "2026-06-13", tags: ["propuestas", "ventas"] },
  { id: 3, name: "Acta_Reunion_2026-06-10.pdf", type: "pdf", size: "1.2 MB", uploaded: "2026-06-10", tags: ["reuniones", "actas"] },
  { id: 4, name: "Presupuesto_Anual_2026.xlsx", type: "xls", size: "856 KB", uploaded: "2026-06-08", tags: ["financiero", "presupuestos"] },
  { id: 5, name: "Contrato_Servicios_Cliente.pdf", type: "pdf", size: "3.7 MB", uploaded: "2026-06-05", tags: ["legal", "contratos"] },
  { id: 6, name: "Diagrama_Arquitectura_IA.png", type: "image", size: "1.8 MB", uploaded: "2026-06-03", tags: ["técnico", "arquitectura"] },
];

const getIcon = (type: string) => {
  switch (type) {
    case "pdf": return FileText;
    case "xls": return FileSpreadsheet;
    case "image": return FileImage;
    default: return File;
  }
};

export default function DocumentosPage() {
  return (
    <Sidebar>
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Documentos</h1>
            <p className="text-sm text-muted-foreground">Biblioteca de documentos e informes</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm">
              <Search className="mr-2 h-4 w-4" />
              Buscar
            </Button>
            <Button size="sm">
              <Plus className="mr-2 h-4 w-4" />
              Subir documento
            </Button>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {documents.map((doc) => {
            const Icon = getIcon(doc.type);
            return (
              <Card key={doc.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-5">
                  <div className="flex items-start justify-between">
                    <div className="rounded-lg bg-blue-100 p-2">
                      <Icon className="h-5 w-5 text-blue-600" />
                    </div>
                    <div className="flex gap-1">
                      <Button variant="ghost" size="icon" className="h-8 w-8">
                        <Download className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-red-500">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                  <p className="mt-3 font-medium text-sm truncate">{doc.name}</p>
                  <div className="mt-2 flex items-center gap-2 text-xs text-muted-foreground">
                    <span>{doc.size}</span>
                    <span>•</span>
                    <span>{doc.uploaded}</span>
                  </div>
                  <div className="mt-2 flex flex-wrap gap-1">
                    {doc.tags.map((tag) => (
                      <Badge key={tag} variant="secondary" className="text-xs">{tag}</Badge>
                    ))}
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
