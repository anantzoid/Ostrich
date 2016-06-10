var webpack = require('webpack');

module.exports = {
  devtool: 'cheap-module-source-map',
  entry: {
        app: './render_client.js'
  },
  module: {
    loaders: [{
      test: /\.jsx?$/,
      exclude: /node_modules/,
      loader: 'babel'
    }]
  },
  resolve: {
    extensions: ['', '.js', '.jsx']
  },
  output: {
    path: './dist/',
    publicPath: '/',
    filename: 'bundle.js'
  },
  devServer: {
    contentBase: './dist'
  },
  plugins: [
    new webpack.DefinePlugin({
        'process.env': {
            'NODE_ENV': JSON.stringify('production')
            }
        }),
    new webpack.optimize.UglifyJsPlugin()
  ]
};
