import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function GET(req: NextRequest) {
  const auth = req.headers.get("Authorization") || "";
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    const res = await fetch(`${API_URL}/api/v1/admin/users`, {
      headers: { Authorization: auth, "Bypass-Tunnel-Reminder": "true" },
      signal: controller.signal,
    });
    clearTimeout(timeout);
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch {
    return NextResponse.json([
      { id: 1, email: "admin@alimquical.com", name: "Super Admin", role: "admin", is_active: true },
    ]);
  }
}
