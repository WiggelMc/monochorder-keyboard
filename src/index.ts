import {cylinder, hull, polygon, polyhedron, sphere, union, vector, vector3} from "scad-ts"
import * as fs from "fs"
import * as Path from "path"
import { linear_extrude, translate } from "scad-ts/dist/transformations"
import { generate, Output } from "./keyboard"



const OUT_DIR_NAME = "out"
const OUT_FILE_NAME = "model.scad"

fs.mkdirSync(Path.join(__dirname, "..", OUT_DIR_NAME), { recursive: true })

function generateFile(outputType: Output, filename: string) {
    const obj = generate(outputType)

    fs.writeFileSync(
        Path.join(__dirname, "..", OUT_DIR_NAME, filename),
        obj.serialize({$fn: 50})
    )
}

generateFile("VIEW", "view.scad")
generateFile("PRINT", "print.scad")
generateFile("INTERNAL", "internal.scad")

console.log("Successfully generated Model Files")
