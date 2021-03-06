﻿
#include <stdio.h>

#ifdef WIN32
#include <windows.h>
#define WINAPI __stdcall
#define CPP_PYTHON_EXPORT __declspec(dllexport)
#else
#define WINAPI
#define CPP_PYTHON_EXPORT  __attribute__ ((visibility("default")))
#endif


#pragma pack(push,1)

struct ExportFunctions
{
    unsigned int cb;

    /*
      Nothing to do.
    */
    int (WINAPI * pfn_func_empty)();
    
    /*
        Change the value of param int.
    */
    int (WINAPI * pfn_func_change_value_int)(unsigned  * pvalue);
    
    /*
        Read the memory of param.
    */

    int (WINAPI * pfn_func_in_memory)(const char * ptr, unsigned  ptr_size);
    int (WINAPI * pfn_func_in_memoryw)(const wchar_t * ptr, unsigned  ptr_size);

    /*
        Call twice.
        First call (NULL, &size ) return the size of memory, include the terminating null character,
        Second call (&ptr, &size )  return the memory address and size, not include the terminating null character.
    */
    int (WINAPI * pfn_func_out_memory_noalloc)(const void ** out_ptr, unsigned  * out_ptr_size);
    int (WINAPI * pfn_func_out_memory_alloc)(void * out_ptr, unsigned  * out_ptr_size);

    /*
     Test use byte's array read and int' array read is the same memory.
     Function is 8 bytes alignment.
     */
    int (WINAPI * pfn_func_address_read)(const void ** , unsigned  *);
    int (WINAPI * pfn_func_out_memoryw)(wchar_t * , unsigned * );

};
#pragma pack(pop)


int WINAPI func_empty();
int WINAPI func_change_value_int(unsigned int *);
int WINAPI func_in_memory(const char *, unsigned int );
int WINAPI func_in_memoryw(const wchar_t *, unsigned int );
int WINAPI func_out_memory_noalloc(const void **, unsigned int *);
int WINAPI func_out_memory_alloc(void *, unsigned int *);
int WINAPI func_address_read(const void ** , unsigned  *);
int WINAPI func_out_memoryw(wchar_t *, unsigned *);


extern "C" 
CPP_PYTHON_EXPORT
int WINAPI InitExportFunctions(ExportFunctions *);

/*
    Function pointer type.
*/
typedef int (WINAPI * PFNInitExportFunctions)(ExportFunctions *);
