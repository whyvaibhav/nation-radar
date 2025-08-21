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
  // Production settings
  assetPrefix: process.env.NODE_ENV === 'production' ? '' : '',
  basePath: ''
}

export default nextConfig
