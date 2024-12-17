import { Vector3 } from "./vector3.js";

export abstract class Spline {
    abstract getPoint(t: number): Vector3

    approximateLength(samples: number = 100): number {
        const stepSize = 1 / samples

        let length = 0
        let lastPoint = this.getPoint(0)

        for (let i = 1; i <= samples; i++) {

            const point = this.getPoint(stepSize * i)
            length += Vector3.distance(point, lastPoint)
            lastPoint = point
        }

        return length
    }
}

export class CubicBezier extends Spline {
    readonly p0: Vector3
    readonly p1: Vector3
    readonly p2: Vector3
    readonly p3: Vector3

    constructor(p0: Vector3, p1: Vector3, p2: Vector3, p3: Vector3) {
        super()

        this.p0 = p0
        this.p1 = p1
        this.p2 = p2
        this.p3 = p3
    }

    override getPoint(t: number): Vector3 {
        const mt = 1 - t

        return (
            this.p0.scale(mt * mt * mt)
            .add(this.p1.scale(3 * mt * mt * t))
            .add(this.p2.scale(3 * mt * t * t))
            .add(this.p3.scale(t * t * t))
        )
    }
}
