from .block00_autoImports import *

def onStakLoads_compileStakC():
    if not tryRecompile:
        DEBUG('[Compile] Skipping compilation, set tryRecompile truthy for this func to run.')
        return

    compileStakC()


def compileStakC():
    start = clock()

    newSourceModTime = 0.0
    for root, dirs, files in osWalk(stakCPath):
        for name in files:
            path = osPathJoin(root, name)
            try:
                newSourceModTime = max(newSourceModTime, osPathGetModTime(path))
            except OSError as e:
                DEBUG("[Compile] Can't find last source mod time, path = %s, error = %s" % (path, e))

    oldSourceModTime = float(read(sourceModTimePath))
    if int(newSourceModTime) == int(oldSourceModTime) and not forceRecompile and osPathExists(stakBinaryPath):
        INFO('[Compile] Binary found & up to date, skipping recompilation')
        return

    if osName not in validOSs:
        ERROR('[Compile] Can only use compile script for validOSs = %s, current = %s', validOSs, osName)
        return

    if pyVerJoint not in validPys:
        ERROR('[Compile] Can only use compile script for validPys = %s, current = %s', validPys, pyVerJoint)
        return

    if not osPathExists(stakBinaryDirPath):
        osMakeDirs(stakBinaryDirPath)

    args = []
    argsApp = args.append
    argsExt = args.extend

    argsApp('g++')
    argsApp('-shared')
    argsApp('-fPIC')

    if not isRelease:
        argsExt(('-O0', '-g', '-Wall', '-fwrapv', '-fno-strict-aliasing', '-rdynamic', '-fno-omit-frame-pointer'))

    # includes
    argsApp('-I' + sysConfig.get_python_inc(plat_specific=True))
    argsApp('-I' + pybind11.get_include())
    argsApp('-I' + stakIncludePath)

    if isRelease:
        compilerFlags = getConfigVar('CFLAGS')
        if compilerFlags:
            argsExt(compilerFlags.split())

        linkerFlags = getConfigVar('LDFLAGS')
        if linkerFlags:
            argsExt(linkerFlags.split())

        libDir = getConfigVar('LIBDIR')
        if libDir:
            argsApp('-L' + libDir)

        multiArch = getConfigVar('MULTIARCH')
        if multiArch and multiArch:
            argsApp('-L' + osPathJoin(libDir, multiArch))

    # Python library
    pyLib = getConfigVar('LDLIBRARY')
    if pyLib:
        if pyLib.startswith('lib'):
            pyLib = pyLib[3:]
        pyLib = '.'.join(pyLib.split('.')[:-1])
        argsApp('-l' + pyLib)

    # stak sources
    for root, dirs, files in osWalk(stakSrcPath):
        for fileName in files:
            if fileName[-4:] == '.cpp':
                argsApp(osPathJoin(root, fileName))

    # output
    argsApp('-o')
    argsApp(stakBinaryPath)

    fArgs = []; fArgsApp = fArgs.append
    for arg in args:
        if arg not in fArgs:
            fArgsApp(arg)

    INFO('[Compile] Compiling binaries: py=%s, os=%s, pybind=%s, args=%s', pyVerJoint, osName, pybind11.__version__, fArgs)

    process = openSubProcess(fArgs, stdout=subProcessPipe, stderr=subProcessPipe)
    stdout, stderr = process.communicate()

    INFO('[Compile] Compilation Finished, took: %s' % (clock() - start))

    if process.returncode == 0:
        INFO('[Compile] Great Success!')
        write(sourceModTimePath, str(newSourceModTime))
    else:
        ERROR('[Compile] Compilation Failed!\n out:\n%s\nerr:%s\n', stdout, stderr)
