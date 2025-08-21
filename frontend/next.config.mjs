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
  // Use static export for Railway deployment
  output: 'export',
  trailingSlash: true,
  distDir: 'out',
  experimental: {
    esmExternals: 'loose'
  },
  // Ensure static export works properly
  assetPrefix: '',
  basePath: ''
}

export default nextConfig
