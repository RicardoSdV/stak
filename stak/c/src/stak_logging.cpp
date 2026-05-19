#include "stak_logging.h"

#include <stdarg.h>
#include <stdio.h>

#include "stak_macros.h"


// TODO: Macros for optimized builds no calls, linenos, files & call stacks.


STAK_ECB

static FILE* log_file = NULL;


void stak_toggle_logging(char doLog){
    doLog = doLog ? 1: 0;
    char isLogging = log_file != NULL;

    if (isLogging && !doLog){
        fclose(log_file);
        log_file = NULL;
    }
    else if (!isLogging && doLog){
        log_file = fopen("stak_c.log", "a");
    }
}


void stak_log(const char* fmt, ...){
    if (log_file == NULL)
        return;

    va_list args;
    va_start(args, fmt);
    vfprintf(log_file, fmt, args);
    va_end(args);
    
    fflush(log_file);
}

STAK_ECE
