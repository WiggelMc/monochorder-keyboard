import { polyhedron, ScadMethods, union, vector3 } from "scad-ts";
import { Serializable } from "scad-ts/dist/util/Serializable.js";
import { Vector3 } from "./math/vector3.js";


export type Output = "VIEW" | "INTERNAL" | "PRINT"

export function generate(outputType: Output) : Serializable {
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
                [2,-10,15],
                {x: 1, y: 2, z: 4},
                {x: 5, y: 3, z: 7},
                {x: 6, y: 1, z: 4},
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

    return obj
}