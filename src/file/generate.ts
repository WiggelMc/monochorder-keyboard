import * as fs from "fs"
import * as Path from "path"
import { generate, GenerationConfig } from "../keyboard/keyboard.js"


const OUT_DIR_NAME = "out"
const outDirPath = Path.join(import.meta.dirname, "../..", OUT_DIR_NAME)

export function generateFile(name: string, config: GenerationConfig): void {
    fs.mkdirSync(outDirPath, { recursive: true })

    fs.writeFileSync(
        Path.join(outDirPath, `monochorder-${name}.scad`),
        generate(config)
    )
}