// Republic of Zalvara — passport spread entry.
// Copies the rendered entry.png into the Make.fun output directory.
// Node 22 stdlib only: no dependencies, no network, no clock.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
if (!existsSync(src)) {
  throw new Error("entry.png missing next to main.ts; run generate_image.py first");
}
copyFileSync(src, join(outDir, "entry.png"));
console.log("entry.png -> " + join(outDir, "entry.png"));
