const webpack = require('webpack');  // Import webpack

module.exports = {
  devServer: {
    proxy: {
      '/login': {
        target: 'http://localhost:5000', // Flask server URL
        changeOrigin: true,
        pathRewrite: { '^/api': '' }
      },
      '/ws': {
        target: 'ws://localhost:5000',  // WebSocket proxy
        ws: true
      }
    }
  },
  configureWebpack: {   // ✅ Missing comma fixed here
    plugins: [
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(true)
      })
    ]
  }
};
