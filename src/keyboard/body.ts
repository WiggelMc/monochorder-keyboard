import { Vector3 } from "../math/vector3.js"
import { GenerationConfig } from "./keyboard.js"


export interface ConstructionConfig {
    smoothness: number
    resolution: number
    thickness: number
}

export interface BeltItem {
    position: Vector3
    up: Vector3
    right: Vector3
}

export function construct(items: BeltItem[], generationConfig: GenerationConfig, constructionConfig: ConstructionConfig) {
    
}