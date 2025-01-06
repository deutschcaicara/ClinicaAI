const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.jsx', // Ponto de entrada principal
  output: {
    path: path.resolve(__dirname, 'dist'), // Diretório de saída
    filename: 'bundle.js',
    clean: true, // Limpa a pasta "dist" antes de compilar
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/, // Processa arquivos JS e JSX
        exclude: /node_modules/, // Ignora a pasta "node_modules"
        use: 'babel-loader',
        type: 'javascript/auto', // Garante que o Babel processa módulos corretamente
      },
      {
        test: /\.css$/, // Processa arquivos CSS
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.scss$/, // Processa arquivos SCSS/SASS
        use: ['style-loader', 'css-loader', 'sass-loader'],
      },
      {
        test: /\.(png|jpg|jpeg|gif|svg|ico)$/, // Processa imagens
        type: 'asset/resource',
        generator: {
          filename: 'assets/images/[hash][ext][query]', // Define saída para imagens
        },
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/, // Processa fontes
        type: 'asset/resource',
        generator: {
          filename: 'assets/fonts/[hash][ext][query]', // Define saída para fontes
        },
      },
    ],
    },

  resolve: {
    extensions: ['.js', '.jsx'], // Extensões que serão resolvidas automaticamente
    alias: {
      '@components': path.resolve(__dirname, 'src/components/'),
      '@context': path.resolve(__dirname, 'src/context/'), // Alias para context
      '@dashboard': path.resolve(__dirname, 'src/components/dashboard/'),
      '@pages': path.resolve(__dirname, 'src/pages/'), // Alias para pages
      '@services': path.resolve(__dirname, 'src/services/'), // Alias para services
      '@styles': path.resolve(__dirname, 'src/styles/'), // Alias para styles

  },
  
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html', // Template HTML principal
      favicon: './src/faviicon2.png', // Caminho para o favicon
    }),
  ],
  devServer: {
    static: {
        directory: path.join(__dirname, 'dist'), // Servir arquivos da pasta "dist"
    },
    historyApiFallback: true, // Garante que todas as rotas caiam no index.html
    hot: true, // Hot Module Replacement (HMR)
    port: 3000, // Porta do servidor
},
  devtool: 'source-map', // Gera mapas de origem para facilitar depuração
};
