import { NextRequest, NextResponse } from "next/server";
import apiUrl from "@/lib/api-url";

export async function POST(req: NextRequest) {
  const errors: string[] = [];
  try {
    const body = await req.json();
    errors.push(`body_keys=${Object.keys(body).join(",")}`);
    errors.push(`apiUrl=${apiUrl}`);
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);
    const targetUrl = `${apiUrl}/api/v1/auth/login`;
    errors.push(`fetching=${targetUrl}`);
    const res = await fetch(targetUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
    clearTimeout(timeout);
    errors.push(`status=${res.status}`);
    const data = await res.json();
    return NextResponse.json({ ...data, _debug: errors }, { status: res.status });
  } catch (e) {
    errors.push(`error=${e instanceof Error ? e.message : String(e)}`);
    return NextResponse.json({ detail: "Error de conexión con el servidor", _debug: errors }, { status: 503 });
  }
}