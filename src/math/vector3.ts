export class Vector3 {
    readonly x: number
    readonly y: number
    readonly z: number

    constructor(x: number, y: number, z: number) {
        this.x = x
        this.y = y
        this.z = z
    }

    static all(value: number): Vector3 {
        return new Vector3(value, value, value)
    }

    toString(): string {
        return `(${this.x}, ${this.y}, ${this.z})`
    }

    add(other: Vector3): Vector3 {
        return new Vector3(
            this.x + other.x,
            this.y + other.y,
            this.z + other.z
        )
    }

    subtract(other: Vector3): Vector3 {
        return new Vector3(
            this.x - other.x,
            this.y - other.y,
            this.z - other.z
        )
    }

    dot(other: Vector3): number {
        return (
            this.x * other.x 
            + this.y * other.y 
            + this.z * other.z
        )
    }

    cross(other: Vector3): Vector3 {
        return new Vector3(
            this.y * other.z - this.z * other.y,
            this.z * other.x - this.x * other.z,
            this.x * other.y - this.y * other.x
        )
    }

    magnitude(): number {
        return Math.sqrt(this.sqrMagnitude())
    }

    sqrMagnitude(): number {
        return (
            this.x * this.x
            + this.y * this.y
            + this.z * this.z
        )
    }

    scale(scalar: number): Vector3 {
        return new Vector3(
            this.x * scalar,
            this.y * scalar,
            this.z * scalar
        )
    }

    normalize(): Vector3 {
        return this.scale(1 / this.magnitude())
    }

    projectOnPlane(normal: Vector3): Vector3 {
        const component = normal.normalize()
        return this.subtract(
            component.scale(this.dot(component))
        )
    }

    static angleBetween(a: Vector3, b: Vector3): number {
        return Math.asin(
            a.cross(b).magnitude() 
            / (a.magnitude() * b.magnitude())
        )
    }

    static fromTo(from: Vector3, to: Vector3): Vector3 {
        return to.subtract(from)
    }

    static distance(a: Vector3, b: Vector3): number {
        return Vector3.fromTo(a,b).magnitude()
    }

    static sqrDistance(a: Vector3, b: Vector3): number {
        return Vector3.fromTo(a,b).sqrMagnitude()
    }

    static lerp(a: Vector3, b: Vector3, t: number): Vector3 {
        return a.add(Vector3.fromTo(a,b).scale(t))
    }

    static readonly zero = new Vector3(0,0,0)
    static readonly one = new Vector3(1,1,1)
}