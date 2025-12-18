"""
Injectors will use the last union. The united file is rewritten but not reloaded, instead its __dict__ is updated.

Some stuff is more convenient if computed, but really it only needs to be computed once, not every time the program is run.
So, the solution is to compute these things in this file & inject the results into stak.
Also, removes some clutter from the code.
Also, settings are injected by running this.

Since blocks are numbered it is very tedious to insert or delete a new block, yes it is essential that they be numbered.
Running this file will rename the appropriate files when one of them is deleted & insert & rename when "newBlockName" is
provided & more.

WARNING: Blocks that modify other modules outside stak, should not be imported here, (e.g. interceptor) since there is no
mechanism yet for hooking into the __del__ of ModuleType
"""

from .block00_autoImports import *


def padFlags(flags):  # type: (Seq[str]) -> Lst[str]
    maxFlagLen = max(len(flag) for flag in flags)
    return [': ' + flag + (' ' * (maxFlagLen - len(flag))) + ': ' for flag in flags]


def replaceInPlace(lines, lookingFor, dataStructure):  # type: (Lst[str], str, Any) -> None
    for i, line in enumerate(lines):
        if line.startswith(lookingFor):
            lines[i] = '%s%r  # Injected\n' % (lookingFor, dataStructure)
            return
    print '[STAK] ERROR: Looking for', lookingFor, 'prefix, not found'


def runInjectors():
    print 'runInjectors'

    constsPath = getAbsPathForBlockName('constants')
    constLines = readLines(constsPath)


    # Make new & old block files names and indexes
    # -----------------------------------------------------------------------------------------------------------------
    oldBlockFiles = []; oldBlockFilesApp = oldBlockFiles.append
    nonBlockFiles = []; nonBlockFilesApp = nonBlockFiles.append
    oldBlockNames = []; oldBlockNamesApp = oldBlockNames.append

    for path in os.listdir(absPackagePath):
        if path[nLenPyExt:] != pyExt:
            continue
        path = path[:nLenPyExt]

        if path[:lenBlockPrefix] != blockPrefix:
            nonBlockFilesApp(path)
            continue

        oldBlockFilesApp(path)
        path = path[lenBlockPrefix:]
        idx, name = path.split('_')
        oldBlockNamesApp(name)

    newBlockNames = blockNames
    newMaxBlockIdxLen = len(str(len(newBlockNames) - 1))
    newBlockFiles = [
        blockPrefix + str(i).zfill(newMaxBlockIdxLen) + '_' + name
        for i, name in enumerate(newBlockNames)
    ]
    # -----------------------------------------------------------------------------------------------------------------

    ## On blocks changed run block injection
    # -----------------------------------------------------------------------------------------------------------------
    if oldBlockFiles != newBlockFiles:
        ## Add / remove block names
        # -------------------------------------------------------------------------------------------------------------
        gSpace['__unitedModNames__'][:] = list(newBlockNames)
        gSpace['__unitedModPaths__'][:] = [osPathJoin(absPackagePath, f + pyExt) for f in newBlockFiles]

        oldBlockNamesSet = set(oldBlockNames)
        newBlockNamesSet = set(newBlockNames)

        blockNamesToRemove = oldBlockNamesSet - newBlockNamesSet
        blockNamesToAdd    = newBlockNamesSet - oldBlockNamesSet

        if blockNamesToRemove and blockNamesToAdd:
            print "[STAK] ERROR: Can't add & remove blocks at the same time, blockNamesToAdd", blockNamesToAdd, 'blockNamesToRemove', blockNamesToRemove
            sys.exit()

        removeFile = os.remove
        for name in blockNamesToRemove:
            fileName = oldBlockFiles[oldBlockNames.index(name)]

            if not input('DANGER sure of removing: %s ??' % fileName):
                sys.exit()

            removeFile(osPathJoin(absPackagePath, fileName + pyExt))

        for name in blockNamesToAdd:
            fileName = newBlockFiles[newBlockNames.index(name)]
            path = osPathJoin(absPackagePath, fileName + pyExt)
            writeLines(path, ('from .block00_autoImports import *\n',))
        # -------------------------------------------------------------------------------------------------------------

        ## Make new by old blocks. For renaming in files & therefore excludes new blocks.
        # -------------------------------------------------------------------------------------------------------------
        newByOldBlocks = []
        newByOldBlocksApp = newByOldBlocks.append
        enumOldBlockNames = list(enumerate(oldBlockNames))

        for newIdx, newName in enumerate(newBlockNames):
            for oldIdx, oldName in enumOldBlockNames:
                if oldName == newName:
                    break
            else:
                continue

            newByOldBlocksApp(
                (
                    oldBlockFiles[oldIdx],
                    blockPrefix + str(newIdx).zfill(newMaxBlockIdxLen) + '_' + newName,
                )
            )
        # -------------------------------------------------------------------------------------------------------------

        ## Rename block files.
        # -------------------------------------------------------------------------------------------------------------
        for oldBlock, newBlock in newByOldBlocks:
            newBlockPath = osPathJoin(absPackagePath, newBlock + pyExt)
            if oldBlock != newBlock:
                oldBlockPath = osPathJoin(absPackagePath, oldBlock + pyExt)
                osRename(oldBlockPath, newBlockPath)
        # -------------------------------------------------------------------------------------------------------------

    ## Constants injection:
    # Injection stopped making sense, but it is here because I want to support it because it will be easier to do that
    # than re implement it if I need it in the future.
    # -----------------------------------------------------------------------------------------------------------------
    paddedStakFlags  = padFlags(stakFlags)
    paddedTraceFlags = padFlags(traceFlags)

    valsByNames = (
        ('pStakFlags'  , paddedStakFlags ),
        ('pTraceFlags' , paddedTraceFlags),
    )
    for name, val in valsByNames:
        replaceInPlace(constLines, name + ' = ', val)
        gSpace[name] = val

    writeLines(getAbsPathForBlockName('constants'), constLines)
