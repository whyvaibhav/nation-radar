import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"

const graphiqueFont = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-graphique",
  weight: ["400", "500", "600", "700", "800", "900"],
})

export const metadata: Metadata = {
  title: "Nation Radar Dashboard",
  description: "Social Media Monitoring Tool",
  generator: "v0.app",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <head>
        <style>{`
html {
  font-family: ${graphiqueFont.style.fontFamily};
  --font-sans: ${graphiqueFont.variable};
}
        `}</style>
      </head>
      <body className={`${graphiqueFont.variable} font-sans`}>{children}</body>
    </html>
  )
}
