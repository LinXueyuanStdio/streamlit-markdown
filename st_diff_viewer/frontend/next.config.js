/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  basePath: "/component/st_diff_viewer.st_diff_viewer",
  reactStrictMode: true,
  swcMinify: true,
  images: {
    unoptimized: true,
  },
  transpilePackages: [
    "streamlit-component-lib-react-hooks",
    "streamlit-component-lib",
  ],
};

module.exports = nextConfig;
