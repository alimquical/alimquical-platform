import { NextResponse } from "next/server";
import apiUrl from "@/lib/api-url";

export async function GET() {
  try {
    const res = await fetch(`${apiUrl}/api/v1/payments/gateways`);
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch {
    return NextResponse.json([]);
  }
}