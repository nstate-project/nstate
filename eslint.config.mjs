import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';
import { FlatCompat } from '@eslint/eslintrc';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: resolve(__dirname, 'apps/web'),
});

const eslintConfig = [
  { ignores: ['**/node_modules/**', '**/.next/**', 'apps/web/next-env.d.ts'] },
  ...compat.extends('next/core-web-vitals'),
];

export default eslintConfig;
