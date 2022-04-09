module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    'airbnb-base',
  ],
  parserOptions: {
    ecmaVersion: 'latest',
  },
  rules: {
    'no-undef': 'off',
    camelcase: 'off',
    'no-unused-vars': 'off',
    indent: 'off',
    'arrow-parens': 'off',
    'no-use-before-define': 'off',
    'no-plusplus': 'off',
    quotes: 'off',
    'prefer-template': 'off',
    'prefer-destructuring': 'off',
    'no-var': 'off',
    'prefer-arrow-callback': 'off',
  },

};
