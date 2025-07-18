import { Vector3 } from "../math/vector3.js"

export interface AbsoluteElementPos {
    neutralPos: Vector3
    pressedPos: Vector3
    lowerPos: Vector3
}

export interface ElementPos {
    neutralPos: Vector3
    normal: Vector3
    down: Vector3
}

export function convertPos(pos: AbsoluteElementPos): ElementPos {
    const normal = Vector3.fromTo(pos.pressedPos, pos.neutralPos).normalize()
    const nl = Vector3.fromTo(pos.neutralPos, pos.lowerPos)
    return {
        neutralPos: pos.neutralPos,
        normal: normal,
        down: nl.subtract(normal.scale(nl.dot(normal))).normalize()
    }
}

export interface FileOptions {
    outDirPath: string,
    outFileNamePattern: (name: string) => string
}
