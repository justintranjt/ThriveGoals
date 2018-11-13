'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  URI_CLIENT_ROOT: '"http://localhost:8080"',
  URI_SERVER_ROOT: '"http://localhost:5000"',
})
