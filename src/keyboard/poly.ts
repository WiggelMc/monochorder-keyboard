import { Polyhedron, polyhedron, ScadMethods } from "scad-ts";
import { Body } from "../math/body.js";

function polyhedronFromBody(body: Body): Polyhedron & ScadMethods {
    return polyhedron(
        body.getPoints(),
        body.getTriangles(),
        10
    )
}