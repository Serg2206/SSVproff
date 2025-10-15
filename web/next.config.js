/** @type {import('next').NextConfig} */
const basePath = process.env.NEXT_BASE_PATH || "";
module.exports = {
  output: "export",
  images: { unoptimized: true },
  trailingSlash: true,
  basePath,
  assetPrefix: basePath ? `${basePath}/` : undefined,
};
