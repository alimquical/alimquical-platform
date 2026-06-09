import { NextRequest, NextResponse } from "next/server";
import apiUrl from "@/lib/api-url";

export async function GET(req: NextRequest) {
  const auth = req.headers.get("Authorization") || "";
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);
    const res = await fetch(`${apiUrl}/api/v1/admin/users`, {
      headers: { Authorization: auth },
      signal: controller.signal,
    });
    clearTimeout(timeout);
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch {
    return NextResponse.json({ detail: "Error de conexión con el servidor" }, { status: 503 });
  }
}

export async function POST(req: NextRequest) {
  const auth = req.headers.get("Authorization") || "";
  try {
    const body = await req.json();
    const res = await fetch(`${apiUrl}/api/v1/admin/users`, {
      method: "POST",
      headers: { Authorization: auth, "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch {
    return NextResponse.json({ detail: "Error de conexión con el servidor" }, { status: 503 });
  }
}
