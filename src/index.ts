import * as fs from "fs"
import * as Path from "path"
import { generate, Output } from "./keyboard.js"



const OUT_DIR_NAME = "out"

const outDirPath = Path.join(import.meta.dirname, "..", OUT_DIR_NAME)


fs.mkdirSync(outDirPath, { recursive: true })

function generateFile(outputType: Output, filename: string) {
    const obj = generate(outputType)

    fs.writeFileSync(
        Path.join(outDirPath, filename),
        obj.serialize({$fn: 50})
    )
}

generateFile("VIEW", "view.scad")
generateFile("PRINT", "print.scad")
generateFile("INTERNAL", "internal.scad")

console.log("Successfully generated Model Files")
