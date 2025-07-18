import { FileOptions } from "./options.js";
import * as fs from "fs"
import * as Path from "path"
import { ScadNumber, ScadSerializable } from "scad-ts";


export function generateFile(name: string, options: FileOptions, obj: ScadSerializable, vars?: Record<string, ScadNumber>): void {
    fs.writeFileSync(
        Path.join(options.outDirPath, options.outFileNamePattern(name)),
        obj.serialize(vars)
    )
}