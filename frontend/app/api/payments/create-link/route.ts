import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function POST(req: NextRequest) {
  const auth = req.headers.get("Authorization") || "";
  try {
    const body = await req.json();
    const res = await fetch(`${API_URL}/api/v1/payments/create-link`, {
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