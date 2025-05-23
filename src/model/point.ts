import { cube, ScadColor, ScadMethods, sphere, Union, union } from "scad-ts"
import { Color } from "scad-ts/dist/transformations/color.js"

export const DEFAULT_POINT_SIZE = 30

export function point(color: ScadColor, size: number = DEFAULT_POINT_SIZE): Color & ScadMethods {
    return sphere(size).color(color)
}

export function cubedPoint(colorA: ScadColor, colorB: ScadColor, size: number = DEFAULT_POINT_SIZE): Union & ScadMethods {
    return union(
        point(colorA, size),
        cube(size * 1.5, true).color(colorB)
    )
}