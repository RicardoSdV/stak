#pragma once

#include <stdarg.h>

#include "stak_macros.h"


STAK_ECB

STAK_API void stak_toggle_logging(char isLogging);
void stak_log(const char* fmt, ...);

STAK_ECE
