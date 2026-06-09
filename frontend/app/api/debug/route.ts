import { NextResponse } from "next/server";
import apiUrl from "@/lib/api-url";

export async function POST(req: Request) {
  const results: Record<string, unknown> = {
    api_url: apiUrl,
    tests: [] as Record<string, unknown>[],
  };

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    body = null;
  }

  // Test login endpoint
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000);
    const res = await fetch(`${apiUrl}/api/v1/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body || { email: "admin@alimquical.com", password: "Admin123!" }),
      signal: controller.signal,
    });
    clearTimeout(timeout);
    const text = await res.text();
    (results.tests as Record<string, unknown>[]).push({
      url: `${apiUrl}/api/v1/auth/login`,
      status: res.status,
      body: text.substring(0, 500),
    });
  } catch (e: unknown) {
    (results.tests as Record<string, unknown>[]).push({
      url: `${apiUrl}/api/v1/auth/login`,
      error: e instanceof Error ? e.message : String(e),
    });
  }

  return NextResponse.json(results);
}

export async function GET() {
  const results: Record<string, unknown> = {
    api_url: apiUrl,
    node_env: process.env.NODE_ENV,
    tests: [] as Record<string, unknown>[],
  };

  for (const url of [
    apiUrl,
    `${apiUrl}/health`,
    `${apiUrl}/api/v1/auth/login`,
  ]) {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 10000);
      const opts: RequestInit = { signal: controller.signal };
      if (url.includes("/login")) {
        opts.method = "POST";
        opts.headers = { "Content-Type": "application/json" };
        opts.body = JSON.stringify({ email: "admin@alimquical.com", password: "Admin123!" });
      }
      const res = await fetch(url, opts);
      clearTimeout(timeout);
      const text = await res.text();
      (results.tests as Record<string, unknown>[]).push({
        url,
        status: res.status,
        body: text.substring(0, 500),
      });
    } catch (e: unknown) {
      (results.tests as Record<string, unknown>[]).push({
        url,
        error: e instanceof Error ? e.message : String(e),
      });
    }
  }

  return NextResponse.json(results);
}