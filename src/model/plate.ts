import { Vector3 } from "../math/vector3.js"
import { ElementPos } from "./options.js"

class PlateRect {
    readonly topLeft: Vector3
    readonly topRight: Vector3
    readonly bottomLeft: Vector3
    readonly bottomRight: Vector3

    constructor(topLeft: Vector3, topRight: Vector3, bottomLeft: Vector3, bottomRight: Vector3) {
        this.topLeft = topLeft
        this.topRight = topRight
        this.bottomLeft = bottomLeft
        this.bottomRight = bottomRight
    }

    translate(vector: Vector3) {
        return new PlateRect(
            this.topLeft.add(vector),
            this.topRight.add(vector),
            this.bottomLeft.add(vector),
            this.bottomRight.add(vector)
        )
    }
}

class Plate {
    readonly center: Vector3

    readonly normal: Vector3
    readonly down: Vector3
    readonly right: Vector3

    readonly rect: PlateRect

    readonly depth: number

    constructor(pos: ElementPos, width: number, height: number, depth: number) {
        this.center = pos.neutralPos

        this.normal = Vector3.fromTo(pos.pressedPos, pos.neutralPos).normalize()
        const nl = Vector3.fromTo(pos.neutralPos, pos.lowerPos)
        this.down = nl.subtract(this.normal.scale(nl.dot(this.normal))).normalize()
        this.right = this.normal.cross(this.down)

        const scaled_right = this.right.normalize().scale(width / 2)
        const scaled_down = this.down.normalize().scale(height / 2)
        const scaled_left = scaled_right.invert()
        const scaled_up = scaled_down.invert()

        this.rect = new PlateRect(
            scaled_left.add(scaled_up),
            scaled_right.add(scaled_up),
            scaled_left.add(scaled_down),
            scaled_right.add(scaled_down)
        )

        this.depth = depth
    }

    rectAt(depthScalar: number): PlateRect {
        return this.rect.translate(this.normal.scale(-depthScalar))
    }
}