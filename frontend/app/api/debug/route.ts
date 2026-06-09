import { NextResponse } from "next/server";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "not set";

export async function GET() {
  const results: Record<string, unknown> = {
    api_url: API_URL,
    node_env: process.env.NODE_ENV,
    tests: [] as Record<string, unknown>[],
  };

  // Test 1: just DNS resolution attempt via health endpoint
  for (const url of [
    API_URL,
    `${API_URL}/health`,
    "https://alimquical-platform-production.up.railway.app/health",
    "http://alimquical-platform-production.up.railway.app/health",
  ]) {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 10000);
      const res = await fetch(url, { signal: controller.signal });
      clearTimeout(timeout);
      const text = await res.text();
      (results.tests as Record<string, unknown>[]).push({
        url,
        status: res.status,
        body: text.substring(0, 200),
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