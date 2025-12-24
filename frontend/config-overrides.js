module.exports = {
  webpack: function(config, env) {
    // Fix webpack dev server deprecation warnings
    config.devServer = {
      ...config.devServer,
      setupMiddlewares: (middlewares, devServer) => {
        // Apply any existing middleware setup here if needed
        return middlewares;
      }
    };
    
    return config;
  }
};
