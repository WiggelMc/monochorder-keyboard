import { Keyboard } from "../model/keyboard.js"
import { Vector3 } from "../math/vector3.js"
import { FileOptions, FingerProperties, ModelOptions, SocketProperties } from "../model/options.js"


const fileOptionOverrides: Partial<FileOptions> = {
    outFileNamePattern: (name, side) => `monochorder-${side.toLowerCase()}-${name}.scad`
}

// All Units are in millimeters and degrees

const fingerDefault = {
    bevel: 10,
    depthOffset: 10,
    switchRotation: 0
} as const satisfies FingerProperties

const socketDefault = {
    thickness: 10,
    holeDiameter: 10,
    outerDiameter: 10
} as const satisfies SocketProperties

const leftModelOptions: ModelOptions = {
    side: "Left",
    measurements: {
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
            }
        },
        socket: {
            topSocket: {
                ...socketDefault
            },
            bottomSocket: {
                ...socketDefault
            }
        },
        finger: {
            pinky: {
                ...fingerDefault
            },
            ringFinger: {
                ...fingerDefault
            },
            middleFinger: {
                ...fingerDefault
            },
            indexFinger: {
                ...fingerDefault
            },
            thumb: {
                ...fingerDefault
            },
            resetButton: {
                ...fingerDefault
            }
        }
    },
    positions: {
        plate: {
            neutralPos: new Vector3(1456.4706234146288, 316.3718739252763, -231.46281148893797),
            pressedPos: new Vector3(1420.6608552729783, 321.8127760784214, -235.0960398330124),
            lowerPos: new Vector3(1977.033216279087, 415.3340426809764, -342.58506884795753)
        },
        socket: {
            topSocket: {
                neutralPos: new Vector3(-904.3683238903282, -358.7175165545041, 220.88526459839568),
                pressedPos: new Vector3(-793.2338619489407, -316.17778816742486, 189.1650741239475),
                lowerPos: new Vector3(-825.1021157216409, -339.3617777064701, 190.54940625112422)
            },
            bottomSocket: {
                neutralPos: new Vector3(2165.8513080226535, 380.7011089903457, -365.3171142856409),
                pressedPos: new Vector3(2159.5886407696994, 384.57842104993824, -364.9070041806395),
                lowerPos: new Vector3(2083.024093800092, 401.9518668499276, -372.5649509937131)
            }
        },
        finger: {
            pinky: {
                neutralPos: new Vector3(1554.2560802455714, 466.1770360572437, -397.4813845374891),
                pressedPos: new Vector3(1522.1746959064412, 432.2745345901422, -377.24702362457907),
                lowerPos: new Vector3(1709.2865023886206, 415.4072540793262, -360.22957236030277)
            },
            ringFinger: {
                neutralPos: new Vector3(1348.6026392202211, 377.72556873886924, -365.771350395731),
                pressedPos: new Vector3(1321.3241102201896, 369.16959334356534, -345.07646939703454),
                lowerPos: new Vector3(1224.9141601304623, 375.7319157089071, -298.10263548346074)
            },
            middleFinger: {
                neutralPos: new Vector3(1041.2780074726293, 268.0107821194402, -302.02405546065603),
                pressedPos: new Vector3(981.2906594996211, 243.48354486731813, -272.00200840898685),
                lowerPos: new Vector3(853.4669740979748, 259.10092859673034, -215.3749190054778)
            },
            indexFinger: {
                neutralPos: new Vector3(586.0913118849629, 113.56836743021786, -180.8227818228707),
                pressedPos: new Vector3(531.863039687149, 96.20220723124721, -162.6844269011413),
                lowerPos: new Vector3(320.9187789403884, 93.05833098450742, -86.20735873582272)
            },
            thumb: {
                neutralPos: new Vector3(-621.9426186864059, -230.88216712819184, 154.32673132417383),
                pressedPos: new Vector3(-110.60105360602539, -79.16473858105687, 7.843036558805498),
                lowerPos: new Vector3(123.60472911006082, 53.102285629808556, -13.228235370826022)
            },
            resetButton: {
                neutralPos: new Vector3(-1210.500530526761, -165.94824847688236, 207.5957092833063),
                pressedPos: new Vector3(-829.5433817353334, -108.75946365361578, 148.19506705215102),
                lowerPos: new Vector3(-1009.5073818600199, -97.09490860946549, 171.78908516006703)
            }
        }
    }
}

const rightModelOptions: ModelOptions = {
    ...leftModelOptions,
    side: "Right"
}

export function generate(fileOptions: FileOptions) {

    const fullFileOptions: FileOptions = {
        ...fileOptions,
        ...fileOptionOverrides
    }

    const keyboards = [
        new Keyboard(fullFileOptions, leftModelOptions),
        new Keyboard(fullFileOptions, rightModelOptions)
    ]

    for (const keyboard of keyboards) {

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
    
    }
}