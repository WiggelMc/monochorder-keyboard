import { Keyboard } from "../model/keyboard.js"
import { Vector3 } from "../math/vector3.js"
import { ElementPos, FileOptions, FingerProperties, ModelOptions, PositionOptions, SocketProperties } from "../model/options.js"
import { DeepPartial } from "../types/partial.js"


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

const leftHandPositions = {
    plate: {
        neutralPos: new Vector3(67775.47156219452, -522206.5845597438, -257100.47685789928),
        pressedPos: new Vector3(7551.165674431212, -58039.660180230916, -28227.866294711082),
        lowerPos: new Vector3(288.99540638709624, -1568.8785884482531, -894.2460346543179)
    },
    socket: {
        topSocket: {
            neutralPos: new Vector3(48.91273013393393, 319.6813612315598, 347.45233088843946),
            pressedPos: new Vector3(48.78013530029204, 329.5291086092243, 380.61447124041865),
            lowerPos: new Vector3(50.93440463716172, 304.68779242787156, 310.9954754309209)
        },
        bottomSocket: {
            neutralPos: new Vector3(143.83557377481984, -302.3910686689303, -144.91354045322544),
            pressedPos: new Vector3(158.812759914361, -496.19747782853693, -276.96100802564104),
            lowerPos: new Vector3(147.4123276519656, -330.0881426550283, -163.22997940598177)
        }
    },
    finger: {
        pinky: {
            neutralPos: new Vector3(138.89807299489027, -413.3537103216333, -234.2827395545861),
            pressedPos: new Vector3(141.93539270017735, -427.1207849698413, -241.8226986506282),
            lowerPos: new Vector3(146.25254587605247, -420.2213697048074, -234.53440182567695)
        },
        ringFinger: {
            neutralPos: new Vector3(329.38253200137086, -2050.4353294700622, -1118.995166495777),
            pressedPos: new Vector3(340.5012350626496, -2120.952547488061, -1157.1720830662744),
            lowerPos: new Vector3(405.97620607519235, -2520.1167975533776, -1364.413272130732)
        },
        middleFinger: {
            neutralPos: new Vector3(-145.81457075967606, 1733.8618861074283, 836.2054388999757),
            pressedPos: new Vector3(-149.27268104813996, 1784.682643850802, 844.0581477264842),
            lowerPos: new Vector3(-140.69928806164376, 1748.7576693199294, 776.4694124756975)
        },
        indexFinger: {
            neutralPos: new Vector3(-19.183623633856648, 850.7571397194303, 608.4215828016282),
            pressedPos: new Vector3(-25.283219974575413, 910.780641542663, 613.6493518894958),
            lowerPos: new Vector3(-10.836956013549626, 847.0069425687793, 557.2635025993008)
        },
        thumb: {
            neutralPos: new Vector3(47.51263991791994, 360.02591818171345, 395.7263374377238),
            pressedPos: new Vector3(24.749263077546086, 579.4151276106086, 488.61832120758004),
            lowerPos: new Vector3(29.607029428123912, 561.5006103902106, 478.42172346025404)
        }
    }
} as const satisfies DeepPartial<PositionOptions, ElementPos>

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
        ...leftHandPositions,
        finger: {
            ...leftHandPositions.finger,
            resetButton: leftHandPositions.finger.thumb
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