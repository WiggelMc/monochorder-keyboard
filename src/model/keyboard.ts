import { cube, cylinder, polyhedron, ScadColor, ScadMethods, sphere, Union, union, vector3 } from "scad-ts";
import { Serializable } from "scad-ts/dist/util/Serializable.js";
import { Vector3 } from "../math/vector3.js";
import { FileOptions, ModelOptions, RenderOptions } from "../model/options.js";
import * as fs from "fs"
import * as Path from "path"
import { Body } from "../math/body.js";
import { polyhedronFromBody } from "../model/poly.js";
import { cubedPoint, point } from "../model/point.js";
import { Color } from "../model/color.js";

export abstract class Keyboard {
    protected fileOptions: FileOptions
    protected modelOptions: ModelOptions

    constructor(fileOptions: FileOptions, modelOptions: ModelOptions) {
        this.fileOptions = fileOptions
        this.modelOptions = modelOptions
    }

    generateFile(name: string, renderOptions: RenderOptions): void {
        fs.writeFileSync(
            Path.join(this.fileOptions.outDirPath, this.fileOptions.outFileNamePattern(name, this.modelOptions.side)),
            this.generate(renderOptions)
        )
    }

    abstract generate(renderOptions: RenderOptions): string
}