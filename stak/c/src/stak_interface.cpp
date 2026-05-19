/*

This is the cpp side of stak.

Compiler Version:
    - Windows: x86_64-w64-mingw32-g++ (GCC) 10-win32 20220113
    - Linux: TBD

Standard: C89 for most code C++17 for pybind11 integration.

Naming conventions:
    macros          : STAK_ALL_CAPS
    external linkage: stak_snake_case
    internal linkage: snake_case
    block scope     : camelCase

*/

#include "stak_interface.h"

#include "stak_interface.h"
#include "stak_logging.h"
#include "stak_settings.h"

void stak_init() {
    stak_log("Hello from the other side!\n");
}
