import type { Metadata, Viewport } from "next";
import "@/styles/globals.css";

export const metadata: Metadata = {
  title: "INTELLIWORK™ - Intelligent Executive Workspace",
  description:
    "Plataforma empresarial con agentes de inteligencia artificial para reuniones, documentación y productividad ejecutiva",
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "INTELLIWORK",
  },
  icons: {
    icon: [
      { url: "/icons/icon-192.png", sizes: "192x192", type: "image/png" },
      { url: "/icons/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
    apple: [{ url: "/icons/icon-192.png", sizes: "192x192", type: "image/png" }],
  },
};

export const viewport: Viewport = {
  themeColor: "#1565C0",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es" suppressHydrationWarning>
      <head>
        <link rel="manifest" href="/manifest.json" />
        <meta name="application-name" content="INTELLIWORK" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="INTELLIWORK" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="theme-color" content="#1565C0" />
      </head>
      <body className="min-h-screen bg-background text-foreground antialiased">
        {children}
        <script
          dangerouslySetInnerHTML={{
            __html: `
              if ('serviceWorker' in navigator) {
                window.addEventListener('load', function() {
                  navigator.serviceWorker.register('/sw.js').then(function(reg) {
                    reg.addEventListener('updatefound', function() {
                      var installing = reg.installing;
                      installing.addEventListener('statechange', function() {
                        if (installing.state === 'installed' && navigator.serviceWorker.controller) {
                          installing.postMessage({action: 'skipWaiting'});
                        }
                      });
                    });
                  });
                });
                navigator.serviceWorker.addEventListener('controllerchange', function() {
                  window.location.reload();
                });
              }
            `,
          }}
        />
      </body>
    </html>
  );
}
