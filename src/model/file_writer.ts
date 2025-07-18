import { FileOptions } from "./options.js";
import * as fs from "fs"
import * as Path from "path"
import { ScadNumber, ScadSerializable } from "scad-ts";

export class ScadFileWriter {
    readonly options: FileOptions

    constructor(options: FileOptions) {
        this.options = options;
    }

    write(name: string, obj: ScadSerializable, vars?: Record<string, ScadNumber>): void {
        fs.writeFileSync(
            Path.join(this.options.outDirPath, this.options.outFileNamePattern(name)),
            obj.serialize(vars)
        )
    }
}