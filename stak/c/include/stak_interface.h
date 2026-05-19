# pragma once

# include <stddef.h>

# include "stak_macros.h"

STAK_ECB

STAK_API void stak_init();
STAK_API void stak_set_is_dev(char is_dev);
STAK_API void stak_set_silent_files(size_t cnt, const char** paths);

STAK_ECE
