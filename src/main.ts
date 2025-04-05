import * as fs from "fs"
import * as Path from "path"
import { Keyboard } from "./model/keyboard.js"
import { Vector3 } from "./math/vector3.js"

const OUT_DIR_NAME = "out"
const outDirPath = Path.join(import.meta.dirname, "..", OUT_DIR_NAME)
fs.mkdirSync(outDirPath, { recursive: true })

const keyboard = new Keyboard(outDirPath, {
    shell: {
        curveSmoothness: 10,
        margin: 10,
        thickness: 10
    },
    plate: {
        controller: {
            backSlotDepth: 10,
            backSlotWidth: 10,
            length: 10,
            portDepth: 10,
            portOffset: 10,
            surfaceOffset: 10,
            thickness: 10,
            width: 10
        },
        rj9: {
            holeHeight: 10,
            holeWidth: 10,
            slotBottomOffset: 10,
            slotDepth: 10,
            slotDepthOffset: 10,
            slotTopOffset: 10
        },
        neutralPos: new Vector3(0, 0, 0),
        pressedPos: new Vector3(0, 0, 0),
        lowerPos: new Vector3(0, 0, 0)
    },
    socket: {
        defaults: {
            thickness: 10,
            holeDiameter: 10,
            outerDiameter: 10
        },
        topSocket: {
            neutralPos: new Vector3(0, 0, 0),
            pressedPos: new Vector3(0, 0, 0),
            lowerPos: new Vector3(0, 0, 0)
        },
        bottomSocket: {
            neutralPos: new Vector3(0, 0, 0),
            pressedPos: new Vector3(0, 0, 0),
            lowerPos: new Vector3(0, 0, 0)
        }
    },
    finger: {
        defaults: {
            bevel: 10,
            depthOffset: 10,
            switchRotation: 0
        },
        pinky: {
            neutralPos: new Vector3(0, 0, 0),
            pressedPos: new Vector3(0, 0, 0),
            lowerPos: new Vector3(0, 0, 0)
        },
        ringFinger: {
            neutralPos: new Vector3(0, 0, 0),
            pressedPos: new Vector3(0, 0, 0),
            lowerPos: new Vector3(0, 0, 0)
        },
        middleFinger: {
            neutralPos: new Vector3(0, 0, 0),
            pressedPos: new Vector3(0, 0, 0),
            lowerPos: new Vector3(0, 0, 0)
        },
        indexFinger: {
            neutralPos: new Vector3(0, 0, 0),
            pressedPos: new Vector3(0, 0, 0),
            lowerPos: new Vector3(0, 0, 0)
        },
        thumb: {
            neutralPos: new Vector3(0, 0, 0),
            pressedPos: new Vector3(0, 0, 0),
            lowerPos: new Vector3(0, 0, 0)
        },
        resetButton: {
            neutralPos: new Vector3(0, 0, 0),
            pressedPos: new Vector3(0, 0, 0),
            lowerPos: new Vector3(0, 0, 0)
        }
    }
})

keyboard.generateFile("view", {
    printCut: false,
    showHull: true,
    showPoints: true,
    showComponents: true
})

keyboard.generateFile("view-raw", {
    printCut: false,
    showHull: true,
    showPoints: false,
    showComponents: false
})

keyboard.generateFile("internal", {
    printCut: false,
    showHull: false,
    showPoints: true,
    showComponents: true
})

keyboard.generateFile("print", {
    printCut: true,
    showHull: true,
    showPoints: false,
    showComponents: false
})


console.log("Successfully generated Model Files")
