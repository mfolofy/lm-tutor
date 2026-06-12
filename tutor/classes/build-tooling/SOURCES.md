# SOURCES — build-tooling (Modern Build Tooling)

## Primary standards

- **Biome docs** (biomejs.dev). <https://biomejs.dev/>
- **Oxlint / oxc** (oxc.rs). <https://oxc.rs/>
- **Lightning CSS** (lightningcss.dev). <https://lightningcss.dev/>
- **Vite docs** (vitejs.dev). <https://vitejs.dev/>
- **Turbopack docs**. <https://turbo.build/pack>
- **Bun docs** (bun.sh). <https://bun.sh/>

## Rule-to-standard map

| Rule ID | Primary Source |
|---------|---------------|
| `eslint-legacy` | Biome docs — migration guide, oxc.rs |
| `prettier-legacy` | Biome docs — formatter |
| `postcss-over-lightning` | Lightning CSS docs, Vite CSS docs |
| `webpack-over-vite` | Vite docs — comparisons |
| `no-lint-autofix` | Biome docs — CLI |
| `tsc-for-linting` | oxc.rs — type-aware linting, tsc docs |
| `dual-eslint-biome` | Biome docs — migration |
| `all-lint-rules-on` | Biome docs — rules |
| `no-cache-in-ci` | Biome docs — CLI |
| `js-tooling-default` | Biome/Vite/Oxlint docs |

## Coverage: ~50% Layer 1, ~50% teaching-only. Verified in tests/test_build_tooling.py.
