/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  // Remove static export for better compatibility
  // output: 'export',
  // trailingSlash: true,
  // distDir: 'out',
}

export default nextConfig
