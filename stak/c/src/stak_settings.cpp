#include "stak_settings.h"

#include <stdio.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>

#include "stak_macros.h"
#include "stak_settings.h"
#include "stak_logging.h"


STAK_ECB

// Settings
char   stak_is_dev           = 0;
char** stak_silent_files     = NULL;
size_t stak_silent_files_cnt = 0;


void stak_set_is_dev(char isDev) {
    char newIsDev = isDev ? 1 : 0;
    stak_is_dev = newIsDev;
    stak_toggle_logging(newIsDev);
}

void stak_set_silent_files(size_t cnt, const char** paths) {
    size_t i;
    
    for (size_t i = 0; i < stak_silent_files_cnt; ++i)
        free(stak_silent_files[i]);
    free(stak_silent_files);

    stak_silent_files_cnt = cnt;
    if (cnt == 0 || paths == NULL) {
        stak_silent_files = NULL;
        return;
    }

    stak_silent_files = (char**)malloc(cnt * sizeof(char*));
    for (i = 0; i < cnt; ++i)
        stak_silent_files[i] = strdup(paths[i]);
}

STAK_ECE
