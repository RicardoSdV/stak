#pragma once

#include <stddef.h>

#include "stak_macros.h"

STAK_ECB

extern char stak_is_dev;
extern char** stak_silent_files;
extern size_t stak_silent_files_cnt;

STAK_API void stak_set_is_dev(char is_dev);
STAK_API void stak_set_silent_files(size_t cnt, const char** paths);

STAK_ECE
