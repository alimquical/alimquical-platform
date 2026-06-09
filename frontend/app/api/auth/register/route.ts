import { NextResponse } from "next/server";
import apiUrl from "@/lib/api-url";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { name, email, password, company_name } = body;
    const res = await fetch(`${apiUrl}/api/v1/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Bypass-Tunnel-Reminder": "true" },
      body: JSON.stringify({ name, email, password, company_name }),
    });

    if (!res.ok) {
      const error = await res.json();
      return NextResponse.json(error, { status: res.status });
    }

    const data = await res.json();
    return NextResponse.json(data, { status: 201 });
  } catch {
    return NextResponse.json({ error: "Error del servidor" }, { status: 500 });
  }
}
