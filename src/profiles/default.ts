import { cube } from "scad-ts"
import { FileOptions } from "../model/options.js"
import { Vector3 } from "../math/vector3.js"
import { ScadFileWriter } from "../model/file_writer.js";

export function generate(fileOptions: FileOptions) {
    const fileWriter = new ScadFileWriter(fileOptions);

    const obj = cube(new Vector3(25, 0.2, 2));

    fileWriter.write("test", obj, { $fn: 50 })
}