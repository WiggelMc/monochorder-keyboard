import { cube } from "scad-ts"
import { FileOptions } from "../model/options.js"
import { Vector3 } from "../math/vector3.js"
import { generateFile } from "../model/model_file.js";

export function generate(fileOptions: FileOptions) {
    const obj = cube(new Vector3(25, 23, 2));

    generateFile("test", fileOptions, obj, { $fn: 50 })
}