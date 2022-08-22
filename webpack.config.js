const path = require('path');
const version = require('./package.json').version;

// Custom webpack rules
const rules = [
  { test: /\.ts$/, loader: 'ts-loader' },
  { test: /\.js$/, loader: 'source-map-loader' },
  { test: /\.css$/, use: ['style-loader', 'css-loader']}
];

// Packages that shouldn't be bundled but loaded at runtime
const externals = ['@jupyter-widgets/base', '@jupyter-widgets/controls', 'module'];

const resolve = {
  // Add '.ts' and '.tsx' as resolvable extensions.
  extensions: [".webpack.js", ".web.js", ".ts", ".js"]
};

module.exports = (env, argv) => {
  const devtool = argv.mode === 'development' ? 'source-map' : false;
  return [
    /**
     * Notebook extension
     *
     * This bundle only contains the part of the JavaScript that is run on load of
     * the notebook.
     */
    {
      entry: './src/extension.ts',
      output: {
        filename: 'extension.js',
        path: path.resolve(__dirname, 'ipywidgets_extended', 'nbextension', 'static'),
        libraryTarget: 'amd'
      },
      devtool,
      resolve
    },

    {
      entry: ['./amd-public-path.js', './src/index.ts'],
      output: {
        filename: 'index.js',
        path: path.resolve(__dirname, 'ipywidgets_extended', 'nbextension', 'static'),
        libraryTarget: 'amd',
        library: 'ipywidgets-extended',
        publicPath: '',  // Set in amd-public-path.js
      },
      devtool,
      module: {
        rules: rules
      },
      externals,
      resolve
    },

    /**
     * Embeddable bundle
     *
     * This bundle is almost identical to the notebook extension bundle. The only
     * difference is in the configuration of the webpack public path for the
     * static assets.
     */
    {
      entry: ['./amd-public-path.js', './src/index.ts'],
      output: {
          filename: 'index.js',
          path: path.resolve(__dirname, 'dist'),
          libraryTarget: 'amd',
          library: "ipywidgets-extended",
          publicPath: ''  // Set in amd-public-path.js, old='https://unpkg.com/ipywidgets-extended@' + version + '/dist/'
      },
      devtool,
      module: {
          rules: rules
      },
      externals,
      resolve
    }


    /**
     * Documentation widget bundle
     *
     * This bundle is used to embed widgets in the package documentation.
     */
    // {
    //   entry: './src/index.ts',
    //   output: {
    //     filename: 'embed-bundle.js',
    //     path: path.resolve(__dirname, 'docs', 'source', '_static'),
    //     library: "ipywidgets-extended",
    //     libraryTarget: 'amd'
    //   },
    //   module: {
    //     rules: rules
    //   },
    //   devtool,
    //   externals,
    //   resolve,
    // }

  ];
}
