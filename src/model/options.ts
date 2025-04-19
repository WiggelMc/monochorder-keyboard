import { Vector3 } from "../math/vector3.js"

export interface ShellOptions {
    thickness: number
    margin: number
    curveSmoothness: number
}

export interface FingerProperties {
    bevel: number
    depthOffset: number
    switchRotation: number
}

export interface FingerOptions {
    pinky: FingerProperties
    ringFinger: FingerProperties
    middleFinger: FingerProperties
    indexFinger: FingerProperties
    thumb: FingerProperties
    resetButton: FingerProperties
}

export interface SocketProperties {
    thickness: number
    holeDiameter: number
    outerDiameter: number
}

export interface SocketOptions {
    topSocket: SocketProperties
    bottomSocket: SocketProperties
}

export interface ControllerOptions {
    thickness: number
    width: number
    length: number
    backSlotWidth: number
    backSlotDepth: number
    portOffset: number
    portDepth: number
    surfaceOffset: number
}

export interface RJ9Options {
    holeHeight: number
    holeWidth: number
    slotDepth: number
    slotDepthOffset: number
    slotTopOffset: number
    slotBottomOffset: number
}

export interface PlateOptions {
    controller: ControllerOptions
    rj9: RJ9Options
}

export interface MeasurementOptions {
    shell: ShellOptions
    finger: FingerOptions
    socket: SocketOptions
    plate: PlateOptions
}




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

export interface FingerPositionOptions {
    pinky: ElementPos
    ringFinger: ElementPos
    middleFinger: ElementPos
    indexFinger: ElementPos
    thumb: ElementPos
    resetButton: ElementPos
}

export interface SocketPositionOptions {
    topSocket: ElementPos
    bottomSocket: ElementPos
}

export interface PositionOptions {
    finger: FingerPositionOptions
    socket: SocketPositionOptions
    plate: ElementPos
}




export type Side = "Left" | "Right"

export interface ModelOptions {
    side: Side
    measurements: MeasurementOptions
    positions: PositionOptions
}

export interface RenderOptions {
    printCut: boolean
    showHull: boolean
    showPoints: boolean
    showComponents: boolean
}

export interface FileOptions {
    outDirPath: string,
    outFileNamePattern: (name: string, side: Side) => string
}
