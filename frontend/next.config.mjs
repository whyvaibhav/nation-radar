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
  output: 'export',
  distDir: 'out',
  experimental: {
    esmExternals: 'loose'
  },
  // Configuration for Railway deployment
  assetPrefix: process.env.NODE_ENV === 'production' ? '' : '',
  basePath: ''
}

export default nextConfig
