import { Vector3 } from "./vector3.js"

export class Body {
    private pointMap: Map<string, number>
    private points: Vector3[]
    private triangleSet: Set<string>
    private triangles: ([number, number, number])[]

    constructor() {
        this.pointMap = new Map()
        this.points = []
        this.triangleSet = new Set()
        this.triangles = []
    }

    transform(f: (vector: Vector3) => Vector3) {
        const body = new Body()

        for (const [a, b, c] of this.getTriangleVectors()) {
            body.addTriangle(f(a), f(b), f(c))
        }

        return body
    }

    copy() {
        const body = new Body()

        for (const [a, b, c] of this.getTriangleVectors()) {
            body.addTriangle(a, b, c)
        }

        return body
    }

    private getPointIndex(vector: Vector3) {
        const index = this.pointMap.get(vector.toString())

        if (index == undefined) {
            const length = this.points.push(vector)
            const newIndex = length - 1

            this.pointMap.set(vector.toString(), newIndex)

            return newIndex
        } else {
            return index
        }
    }

    addTriangle(a: Vector3, b: Vector3, c: Vector3) {
        if (!this.triangleSet.has([a, b, c].toString())) {

            this.triangles.push([
                this.getPointIndex(a),
                this.getPointIndex(b),
                this.getPointIndex(c)
            ])

            this.triangleSet.add([a, b, c].toString())
        }
    }

    addBody(other: Body) {
        for (const [a, b, c] of other.getTriangleVectors()) {
            this.addTriangle(a, b, c)
        }
    }

    getTriangleVectors(): [Vector3, Vector3, Vector3][] {
        return this.triangles.map(t => [
            this.points[t[0]] as Vector3,
            this.points[t[1]] as Vector3,
            this.points[t[2]] as Vector3
        ])
    }

    getPoints(): Vector3[] {
        return [...this.points]
    }

    getTriangleConnections(): [number, number, number][] {
        return this.triangles.map(t => [...t])
    }
}