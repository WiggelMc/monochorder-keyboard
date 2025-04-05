import { Vector3 } from "../math/vector3.js"

export interface ShellOptions {
    thickness: number
    margin: number
    curveSmoothness: number
}

export interface FingerDefaultProperties {
    bevel: number
    depthOffset: number
    switchRotation: number
}

export interface ElementPos {
    neutralPos: Vector3
    pressedPos: Vector3
    lowerPos: Vector3
}

export type FingerProperties = Partial<FingerDefaultProperties> & ElementPos

export interface FingerOptions {
    defaults: FingerDefaultProperties
    pinky: FingerProperties
    ringFinger: FingerProperties
    middleFinger: FingerProperties
    indexFinger: FingerProperties
    thumb: FingerProperties
    resetButton: FingerProperties
}

export interface SocketDefaultProperties {
    thickness: number
    holeDiameter: number
    outerDiameter: number
}

export type SocketProperties = Partial<SocketDefaultProperties> & ElementPos

export interface SocketOptions {
    defaults: SocketDefaultProperties
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

export type PlateOptions = ElementPos & {
    controller: ControllerOptions
    rj9: RJ9Options
}

export interface ModelOptions {
    shell: ShellOptions
    finger: FingerOptions
    socket: SocketOptions
    plate: PlateOptions
}

export interface RenderOptions {
    printCut: boolean
    showHull: boolean
    showPoints: boolean
    showComponents: boolean
}

export interface FileOptions {
    outDirPath: string,
    outFileNamePattern: (name: string) => string
}