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
  output: 'standalone',
  distDir: '.next',
  experimental: {
    esmExternals: 'loose'
  },
  // Ensure static export works properly
  assetPrefix: '',
  basePath: ''
}

export default nextConfig
