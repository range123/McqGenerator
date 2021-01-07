// const BundleAnalyzerPlugin = require("webpack-bundle-analyzer")
// .BundleAnalyzerPlugin;
module.exports = {
  productionSourceMap: false,
  // configureWebpack: {
  // plugins: [new BundleAnalyzerPlugin()]
  // },
  pwa: {
    name: "Mcq Generator",
    appleMobileWebAppCapable: "yes",
    workboxOptions: {
      skipWaiting: true
    }
  }
};
