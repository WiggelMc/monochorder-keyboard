import { generateFile } from "./file/generate.js"


generateFile("view", {
    printCut: false,
    showHull: true,
    showPoints: true,
    showComponents: true
})

generateFile("view-raw", {
    printCut: false,
    showHull: true,
    showPoints: false,
    showComponents: false
})

generateFile("internal", {
    printCut: false,
    showHull: false,
    showPoints: true,
    showComponents: true
})

generateFile("print", {
    printCut: true,
    showHull: true,
    showPoints: false,
    showComponents: false
})


console.log("Successfully generated Model Files")
