import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import path from 'path'

const ASSET_BASE_PATH = process.env.NODE_ENV === 'production' ? '/mapping-heat/' : '/';
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  base: ASSET_BASE_PATH, // <-- Add this line
  resolve: {
    alias: {
      $data: path.resolve('./data'),
      $lib: path.resolve('./src/lib')
    }
  }
})
