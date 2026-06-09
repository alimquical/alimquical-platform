import { NextRequest, NextResponse } from "next/server";
import apiUrl from "@/lib/api-url";

export async function PUT(req: NextRequest, { params }: { params: Promise<{ userId: string }> }) {
  const auth = req.headers.get("Authorization") || "";
  try {
    const { userId } = await params;
    const body = await req.json();
    const res = await fetch(`${apiUrl}/api/v1/admin/users/${userId}`, {
      method: "PUT",
      headers: { Authorization: auth, "Content-Type": "application/json", "Bypass-Tunnel-Reminder": "true" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch {
    return NextResponse.json({ error: "Error del servidor" }, { status: 500 });
  }
}

export async function DELETE(req: NextRequest, { params }: { params: Promise<{ userId: string }> }) {
  const auth = req.headers.get("Authorization") || "";
  try {
    const { userId } = await params;
    const res = await fetch(`${apiUrl}/api/v1/admin/users/${userId}`, {
      method: "DELETE",
      headers: { Authorization: auth, "Bypass-Tunnel-Reminder": "true" },
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch {
    return NextResponse.json({ error: "Error del servidor" }, { status: 500 });
  }
}
