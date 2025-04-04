import { Vector3 } from "./vector3.js"

export class Body {
    private pointMap: Map<string, number>
    private points: Vector3[]
    private triangles: ([number, number, number])[]

    constructor() {
        this.pointMap = new Map()
        this.points = []
        this.triangles = []
    }

    transform(f: (vector: Vector3) => Vector3) {
        const body = new Body()
        const points = this.points.map(f)

        body.points = points
        for (const [i, point] of points.entries()) {
            body.pointMap.set(point.toString(), i)
        }
        body.triangles = this.getTriangles()
    }

    private getPointIndex(vector: Vector3) {
        const index = this.pointMap.get(vector.toString())

        if (index == undefined) {
            const length = this.points.push(vector)
            return length - 1
        } else {
            return index
        }
    }

    addTriangle(a: Vector3, b: Vector3, c: Vector3) {
        this.triangles.push([
            this.getPointIndex(a),
            this.getPointIndex(b),
            this.getPointIndex(c)
        ])
    }

    getPoints(): Vector3[] {
        return [...this.points]
    }

    getTriangles(): [number, number, number][] {
        return this.triangles.map(t => [...t])
    }
}