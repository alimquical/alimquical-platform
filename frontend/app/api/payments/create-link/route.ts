import { NextRequest, NextResponse } from "next/server";
import apiUrl from "@/lib/api-url";

export async function POST(req: NextRequest) {
  const auth = req.headers.get("Authorization") || "";
  try {
    const body = await req.json();
    const res = await fetch(`${apiUrl}/api/v1/payments/create-link`, {
      method: "POST",
      headers: { Authorization: auth, "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch {
    return NextResponse.json({ detail: "Error de conexión" }, { status: 503 });
  }
}