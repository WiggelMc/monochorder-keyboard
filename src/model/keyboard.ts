import { cube, cylinder, polyhedron, ScadColor, ScadMethods, sphere, Union, union, vector3 } from "scad-ts";
import { Serializable } from "scad-ts/dist/util/Serializable.js";
import { Vector3 } from "../math/vector3.js";
import { FileOptions, ModelOptions, RenderOptions } from "./options.js";
import * as fs from "fs"
import * as Path from "path"
import { Body } from "../math/body.js";
import { polyhedronFromBody } from "./poly.js";
import { cubedPoint, point } from "./point.js";
import { Color } from "./color.js";

export class Keyboard {
    private fileOptions: FileOptions
    private modelOptions: ModelOptions

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

    private generate(renderOptions: RenderOptions): string {
        const body = new Body()
        const a = new Vector3(1, 1, 1)
        const b = new Vector3(12, 4, 1)
        const c = new Vector3(1, 14, 4)
        const d = new Vector3(3, 6, 20)

        body.addTriangle(a, b, c)
        body.addTriangle(a, d, b)
        body.addTriangle(a, c, d)
        body.addTriangle(b, d, c)

        const obj = union(
            polyhedronFromBody(body),
            ...(
                renderOptions.showPoints ? [
                    cubedPoint(Color.white, [1.0, 1.0, 0.0]).translate(a),
                    point([0.6, 0.5, 0.5]).translate(b),
                    point([0.4, 0.2, 0.3]).translate(c),
                    point(Color.black).translate(d)
                ] : []
            )
        )

        return obj.serialize({ $fn: 50 })
    }
}