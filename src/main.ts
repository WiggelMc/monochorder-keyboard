import * as fs from "fs"
import * as Path from "path"
import { FileOptions } from "./model/options.js"

const OUT_DIR_NAME = "out"
const profileName = process.argv[2] ?? "default"

import(`./profiles/${profileName}.js`).then(profile => {
    const generate: (fileOptions: FileOptions) => void = profile.generate

    console.log(`Generating Files for Profile "${profileName}"...`)

    const outDirPath = Path.join(import.meta.dirname, "..", OUT_DIR_NAME, profileName)
    fs.mkdirSync(outDirPath, { recursive: true })

    generate({
        outDirPath: outDirPath,
        outFileNamePattern: (name) => `monochorder-${name}.scad`
    })

    console.log("Successfully generated Model Files")
}).catch(e => {
    if (e?.code == "ERR_MODULE_NOT_FOUND") {
        throw new Error(`Profile "${profileName}" not found`)
    } else {
        throw e
    }
})
