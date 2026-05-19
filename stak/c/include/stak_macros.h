#pragma once

#ifdef __cplusplus
#  define STAK_ECB extern "C" {
#  define STAK_ECE   }
#else
#  define STAK_ECB  // Extern C Begin
#  define STAK_ECE  // Extern C End
#endif


#if defined(_WIN32)
#  define STAK_API __declspec(dllexport)
#else
#  define STAK_API
#endif
