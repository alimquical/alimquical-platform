"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sidebar } from "@/components/ui/sidebar";
import { useState, useEffect } from "react";
import { Users, Shield, Activity, BarChart3, Trash2, CheckCircle, XCircle, RefreshCw, Plus, X } from "lucide-react";

interface UserData {
  id: string;
  email: string;
  name: string;
  role: string;
  is_active: boolean;
  company_name: string | null;
  plan: string;
  subscription_status: string;
  created_at: string;
}

export default function AdminPage() {
  const [users, setUsers] = useState<UserData[]>([]);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ name: "", email: "", password: "", company_name: "", plan: "starter", role: "user" });
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    const t = localStorage.getItem("access_token") || "";
    setToken(t);
    if (t) fetchUsers(t);
  }, []);

  const fetchUsers = async (tok: string) => {
    try {
      const res = await fetch("/api/admin/users", {
        headers: { Authorization: `Bearer ${tok}` },
      });
      if (res.ok) setUsers(await res.json());
    } catch { /* ignore */ }
    finally { setLoading(false); }
  };

  const toggleActive = async (userId: string, current: boolean) => {
    const res = await fetch(`/api/admin/users/${userId}`, {
      method: "PUT",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({ is_active: !current }),
    });
    if (res.ok) fetchUsers(token);
  };

  const deleteUser = async (userId: string) => {
    if (!confirm("¿Eliminar este usuario?")) return;
    const res = await fetch(`/api/admin/users/${userId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) fetchUsers(token);
  };

  const activeUsers = users.filter((u) => u.is_active).length;
  const companies = new Set(users.map((u) => u.company_name).filter(Boolean)).size;

  return (
    <Sidebar>
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Administración</h1>
            <p className="text-sm text-muted-foreground">Gestiona usuarios y suscripciones</p>
          </div>
          <Button variant="outline" size="sm" onClick={() => fetchUsers(token)}>
            <RefreshCw className="mr-2 h-4 w-4" />Actualizar
          </Button>
        </div>

        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="rounded-lg bg-blue-100 p-2"><Users className="h-5 w-5 text-blue-600" /></div>
              </div>
              <p className="text-2xl font-bold mt-4">{users.length}</p>
              <p className="text-xs text-muted-foreground">Total usuarios</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="rounded-lg bg-green-100 p-2"><CheckCircle className="h-5 w-5 text-green-600" /></div>
              </div>
              <p className="text-2xl font-bold mt-4">{activeUsers}</p>
              <p className="text-xs text-muted-foreground">Usuarios activos</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="rounded-lg bg-purple-100 p-2"><Shield className="h-5 w-5 text-purple-600" /></div>
              </div>
              <p className="text-2xl font-bold mt-4">{companies}</p>
              <p className="text-xs text-muted-foreground">Empresas</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="rounded-lg bg-orange-100 p-2"><BarChart3 className="h-5 w-5 text-orange-600" /></div>
              </div>
              <p className="text-2xl font-bold mt-4">$0</p>
              <p className="text-xs text-muted-foreground">Ingresos (pendiente Stripe)</p>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-lg">Usuarios registrados</CardTitle>
            <Button size="sm" onClick={() => setShowModal(true)}>
              <Plus className="mr-2 h-4 w-4" />Crear usuario
            </Button>
          </CardHeader>
          <CardContent>
            {loading ? (
              <p className="text-sm text-muted-foreground">Cargando...</p>
            ) : users.length === 0 ? (
              <p className="text-sm text-muted-foreground">No hay usuarios registrados</p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b text-left">
                      <th className="pb-3 font-medium">Nombre</th>
                      <th className="pb-3 font-medium">Email</th>
                      <th className="pb-3 font-medium">Rol</th>
                      <th className="pb-3 font-medium">Empresa</th>
                      <th className="pb-3 font-medium">Plan</th>
                      <th className="pb-3 font-medium">Estado</th>
                      <th className="pb-3 font-medium">Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map((u) => (
                      <tr key={u.id} className="border-b last:border-0">
                        <td className="py-3">{u.name}</td>
                        <td className="py-3 text-muted-foreground">{u.email}</td>
                        <td className="py-3">
                          <Badge variant={u.role === "admin" ? "default" : "secondary"}>{u.role}</Badge>
                        </td>
                        <td className="py-3">{u.company_name || "-"}</td>
                        <td className="py-3">
                          <Badge variant={u.plan === "corporate" ? "success" : "secondary"}>{u.plan}</Badge>
                        </td>
                        <td className="py-3">
                          <div className="flex items-center gap-2">
                            <span className={`h-2 w-2 rounded-full ${u.is_active ? "bg-green-500" : "bg-red-500"}`} />
                            <span className="text-xs">{u.is_active ? "Activo" : "Inactivo"}</span>
                          </div>
                        </td>
                        <td className="py-3">
                          <div className="flex gap-1">
                            <button
                              onClick={() => toggleActive(u.id, u.is_active)}
                              className="rounded p-1 hover:bg-gray-100"
                              title={u.is_active ? "Desactivar" : "Activar"}
                            >
                              {u.is_active ? <XCircle className="h-4 w-4 text-red-500" /> : <CheckCircle className="h-4 w-4 text-green-500" />}
                            </button>
                            <button
                              onClick={() => deleteUser(u.id)}
                              className="rounded p-1 hover:bg-gray-100"
                              title="Eliminar"
                            >
                              <Trash2 className="h-4 w-4 text-red-500" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={() => setShowModal(false)}>
          <div className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold">Crear usuario</h2>
              <button onClick={() => setShowModal(false)}><X className="h-5 w-5" /></button>
            </div>
            <form onSubmit={async (e) => {
              e.preventDefault(); setCreating(true);
              try {
                const res = await fetch("/api/admin/users", {
                  method: "POST",
                  headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
                  body: JSON.stringify(form),
                });
                if (res.ok) { setShowModal(false); setForm({ name: "", email: "", password: "", company_name: "", plan: "starter", role: "user" }); fetchUsers(token); }
                else { const d = await res.json(); alert(d.detail || "Error"); }
              } catch { alert("Error de conexión"); }
              finally { setCreating(false); }
            }} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Nombre</label>
                  <input type="text" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required
                    className="w-full rounded-lg border px-3 py-2 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Email</label>
                  <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required
                    className="w-full rounded-lg border px-3 py-2 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200" />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Contraseña</label>
                <input type="text" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required
                  className="w-full rounded-lg border px-3 py-2 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Empresa</label>
                <input type="text" value={form.company_name} onChange={(e) => setForm({ ...form, company_name: e.target.value })} required
                  className="w-full rounded-lg border px-3 py-2 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Rol</label>
                  <select value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}
                    className="w-full rounded-lg border px-3 py-2 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200">
                    <option value="user">Usuario</option>
                    <option value="manager">Manager</option>
                    <option value="admin">Admin</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Plan</label>
                  <select value={form.plan} onChange={(e) => setForm({ ...form, plan: e.target.value })}
                    className="w-full rounded-lg border px-3 py-2 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200">
                    <option value="starter">Starter</option>
                    <option value="corporate">Corporate</option>
                    <option value="enterprise">Enterprise</option>
                  </select>
                </div>
              </div>
              <button type="submit" disabled={creating}
                className="w-full rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-50">
                {creating ? "Creando..." : "Crear usuario"}
              </button>
            </form>
          </div>
        </div>
      )}
    </Sidebar>
  );
}
