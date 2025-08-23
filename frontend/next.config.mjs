/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true
  },
  experimental: {
    esmExternals: 'loose'
  },
  // Static export for Railway
  output: 'export',
  distDir: 'out',
  trailingSlash: true,
  // Production settings
  assetPrefix: process.env.NODE_ENV === 'production' ? '' : '',
  basePath: ''
}

export default nextConfig
