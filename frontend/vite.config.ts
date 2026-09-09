import { defineConfig } from 'vite';

/**
 * The card is shipped as a built bundle, because HACS does not run a build.
 * The output directory is mounted into the Home Assistant container during
 * development, so it must not be deleted - only its files are replaced.
 */
export default defineConfig({
  build: {
    outDir: '../custom_components/amberchest/frontend',
    emptyOutDir: false,
    target: 'es2022',
    lib: {
      entry: 'src/card.ts',
      formats: ['es'],
      fileName: () => 'amberchest-card.js',
    },
  },
});
