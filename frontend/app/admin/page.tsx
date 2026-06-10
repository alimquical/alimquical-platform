"use client";

import { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sidebar } from "@/components/ui/sidebar";
import { useTranslation } from "@/lib/i18n";
import {
  Users,
  UserCheck,
  Building2,
  DollarSign,
  Plus,
  Trash2,
  CreditCard,
  X,
} from "lucide-react";

interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  company_id?: string;
  is_active: boolean;
  plan?: string;
}

export default function AdminPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const { t } = useTranslation();

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch("/api/admin/users", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) setUsers(await res.json());
    } finally {
      setLoading(false);
    }
  };

  const createUser = async (e: React.FormEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const data = {
      name: (form.elements.namedItem("name") as HTMLInputElement).value,
      email: (form.elements.namedItem("email") as HTMLInputElement).value,
      password: (form.elements.namedItem("password") as HTMLInputElement).value,
      company_name: (form.elements.namedItem("company") as HTMLInputElement).value,
      role: (form.elements.namedItem("role") as HTMLSelectElement).value,
      plan: (form.elements.namedItem("plan") as HTMLSelectElement).value,
    };
    const token = localStorage.getItem("access_token");
    const res = await fetch("/api/admin/users", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify(data),
    });
    if (res.ok) {
      setShowCreate(false);
      fetchUsers();
    } else {
      alert(t("admin.error_connection"));
    }
  };

  const toggleUser = async (userId: string, current: boolean) => {
    const token = localStorage.getItem("access_token");
    await fetch(`/api/admin/users/${userId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ is_active: !current }),
    });
    fetchUsers();
  };

  const deleteUser = async (userId: string) => {
    if (!confirm(t("admin.delete_confirm"))) return;
    const token = localStorage.getItem("access_token");
    await fetch(`/api/admin/users/${userId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    fetchUsers();
  };

  const generatePaymentLink = async (userId: string) => {
    const token = localStorage.getItem("access_token");
    const res = await fetch("/api/payments/create-link", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ user_id: userId }),
    });
    if (res.ok) {
      const data = await res.json();
      window.open(data.url, "_blank");
    } else {
      alert(t("admin.error_link"));
    }
  };

  const activeUsers = users.filter((u) => u.is_active).length;
  const companies = [...new Set(users.map((u) => u.company_id).filter(Boolean))].length;

  return (
    <Sidebar>
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">{t("admin.title")}</h1>
            <p className="text-sm text-muted-foreground">{t("admin.subtitle")}</p>
          </div>
          <Button variant="outline" size="sm" onClick={() => setShowCreate(true)}>
            <Plus className="mr-2 h-4 w-4" />
            {t("admin.update")}
          </Button>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-3">
                <div className="rounded-lg bg-blue-100 p-2"><Users className="h-5 w-5 text-blue-600" /></div>
                <div>
                  <p className="text-2xl font-bold">{users.length}</p>
                  <p className="text-xs text-muted-foreground">{t("admin.total_users")}</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-3">
                <div className="rounded-lg bg-green-100 p-2"><UserCheck className="h-5 w-5 text-green-600" /></div>
                <div>
                  <p className="text-2xl font-bold">{activeUsers}</p>
                  <p className="text-xs text-muted-foreground">{t("admin.active_users")}</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-3">
                <div className="rounded-lg bg-purple-100 p-2"><Building2 className="h-5 w-5 text-purple-600" /></div>
                <div>
                  <p className="text-2xl font-bold">{companies}</p>
                  <p className="text-xs text-muted-foreground">{t("admin.companies")}</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-3">
                <div className="rounded-lg bg-orange-100 p-2"><DollarSign className="h-5 w-5 text-orange-600" /></div>
                <div>
                  <p className="text-2xl font-bold">$0</p>
                  <p className="text-xs text-muted-foreground">{t("admin.revenue")}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>{t("admin.registered_users")}</CardTitle>
            <Button size="sm" onClick={() => setShowCreate(true)}>
              <Plus className="mr-2 h-4 w-4" />
              {t("admin.create_user")}
            </Button>
          </CardHeader>
          <CardContent>
            {loading ? (
              <p className="text-sm text-muted-foreground">{t("admin.loading")}</p>
            ) : users.length === 0 ? (
              <p className="text-sm text-muted-foreground">{t("admin.no_users")}</p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b text-left">
                      <th className="pb-3 font-medium">{t("admin.name")}</th>
                      <th className="pb-3 font-medium">{t("admin.role")}</th>
                      <th className="pb-3 font-medium">{t("admin.company")}</th>
                      <th className="pb-3 font-medium">{t("admin.plan")}</th>
                      <th className="pb-3 font-medium">{t("admin.status")}</th>
                      <th className="pb-3 font-medium">{t("admin.actions")}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map((user) => (
                      <tr key={user.id} className="border-b last:border-0">
                        <td className="py-3">{user.name}</td>
                        <td className="py-3">{user.role}</td>
                        <td className="py-3 text-muted-foreground">{user.company_id || "-"}</td>
                        <td className="py-3">
                          <Badge variant="outline">{user.plan || "starter"}</Badge>
                        </td>
                        <td className="py-3">
                          <Badge variant={user.is_active ? "success" : "secondary"}>
                            {user.is_active ? t("admin.active") : t("admin.inactive")}
                          </Badge>
                        </td>
                        <td className="py-3">
                          <div className="flex gap-1">
                            <Button
                              variant="ghost" size="sm"
                              title={user.is_active ? t("admin.disable") : t("admin.enable")}
                              onClick={() => toggleUser(user.id, user.is_active)}
                            >
                              <UserCheck className="h-4 w-4" />
                            </Button>
                            <Button
                              variant="ghost" size="sm"
                              title={t("admin.generate_payment_link")}
                              onClick={() => generatePaymentLink(user.id)}
                            >
                              <CreditCard className="h-4 w-4" />
                            </Button>
                            <Button
                              variant="ghost" size="sm"
                              title={t("admin.delete")}
                              onClick={() => deleteUser(user.id)}
                            >
                              <Trash2 className="h-4 w-4 text-red-500" />
                            </Button>
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

      {showCreate && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={() => setShowCreate(false)}>
          <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold">{t("admin.create_user")}</h2>
              <button onClick={() => setShowCreate(false)}><X className="h-5 w-5" /></button>
            </div>
            <form onSubmit={createUser} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">{t("admin.name")}</label>
                <input name="name" className="w-full rounded-lg border px-4 py-2 text-sm" required />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">{t("admin.email_label")}</label>
                <input name="email" type="email" className="w-full rounded-lg border px-4 py-2 text-sm" required />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">{t("auth.password")}</label>
                <input name="password" type="password" className="w-full rounded-lg border px-4 py-2 text-sm" required />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">{t("admin.company")}</label>
                <input name="company" className="w-full rounded-lg border px-4 py-2 text-sm" required />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">{t("admin.role")}</label>
                <select name="role" className="w-full rounded-lg border px-4 py-2 text-sm">
                  <option value="user">{t("admin.user")}</option>
                  <option value="admin">{t("nav.admin")}</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">{t("admin.plan")}</label>
                <select name="plan" className="w-full rounded-lg border px-4 py-2 text-sm">
                  <option value="starter">Starter</option>
                  <option value="corporate">Corporate</option>
                  <option value="enterprise">Enterprise</option>
                </select>
              </div>
              <Button type="submit" className="w-full">
                {t("admin.creating")}
              </Button>
            </form>
          </div>
        </div>
      )}
    </Sidebar>
  );
}
