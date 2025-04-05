import { cylinder, polyhedron, ScadMethods, union, vector3 } from "scad-ts";
import { Serializable } from "scad-ts/dist/util/Serializable.js";
import { Vector3 } from "../math/vector3.js";
import { FileOptions, ModelOptions, RenderOptions } from "./options.js";
import * as fs from "fs"
import * as Path from "path"

export class Keyboard {
    private fileOptions: FileOptions
    private modelOptions: ModelOptions

    constructor(fileOptions: FileOptions,  modelOptions: ModelOptions) {
        this.fileOptions = fileOptions
        this.modelOptions = modelOptions
    }

    generateFile(name: string, renderOptions: RenderOptions): void {
        fs.writeFileSync(
            Path.join(this.fileOptions.outDirPath, this.fileOptions.outFileNamePattern(name)),
            this.generate(renderOptions)
        )
    }

    private generate(renderOptions: RenderOptions): string {
        const obj = union(
            // cylinder(1, 1),
            // hull(
            //     sphere(0.01).translate({x:1, y:1, z:1}),
            //     sphere(0.01).translate({x:1, y:1, z:10}),
            //     sphere(0.01).translate({x:1, y:10, z:1}),
            //     sphere(0.01).translate({x:1, y:10, z:1}),
            // ),
            // polygon([{x:0,y:0},{x:1,y:1},{x:2,y:5}], [[0,1,2,0]]).linear_extrude(0.1)
            polyhedron(
                [
                    [2,-10,16],
                    {x: 1, y: 2, z: 4},
                    {x: 5, y: 3, z: 7},
                    new Vector3(6, 1, 10),
                ],
                [
                    [0,1,2],
                    [1,2,3],
                    [2,3,0],
                    [0,3,1]
                ],
                10
            )
        )
        
        return obj.serialize({$fn: 50})
    }
}