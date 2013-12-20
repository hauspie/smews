/*
 * Copyright (c) 2013, Gregory Guche, Michaël Hauspie, Université Lille 1.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 */
#include "allocator.h"
#include "types.h"

/* RAM */
#ifndef ALLOCATOR_RAM_SIZE
#define ALLOCATOR_RAM_SIZE 1024*10
#endif

/* FLASH */
#ifndef ALLOCATOR_FLASH_ADDRESS
/* Get the first available free space in eeprom to store the data */
#define ALLOCATOR_FLASH_SIZE (11*4096)
const char allocator_flash_space[ALLOCATOR_FLASH_SIZE] __attribute__ ((section(".flash_storage"))) = {0};
#define ALLOCATOR_FLASH_ADDRESS (allocator_flash_space)
#endif

static char allocator_ram_buffer[ALLOCATOR_RAM_SIZE];
static char *allocator_last_ram_used = allocator_ram_buffer;

static const char * allocator_flash_buffer = ALLOCATOR_FLASH_ADDRESS;
static const char *allocator_last_flash_used   = ALLOCATOR_FLASH_ADDRESS;

void *allocator_ram_alloc(unsigned int size) {
    char *result;	

    result = allocator_last_ram_used;
    allocator_last_ram_used += ((size & 1) == 0) ? size : size + 1; /* align on an even address */
    if (allocator_last_ram_used >= allocator_ram_buffer + ALLOCATOR_RAM_SIZE)
	return NULL;
    return result;
}

void *allocator_flash_alloc(unsigned int size) {
    const char *result;	

    result = allocator_last_flash_used;
    allocator_last_flash_used += ((size & 1) == 0) ? size : size + 1; /* align on an even address */
    if (allocator_last_flash_used >= ALLOCATOR_FLASH_ADDRESS + ALLOCATOR_FLASH_SIZE)
	return NULL;
    return (void*)result;
}

#ifdef KERNEL_CONSOLE
#include "kernel_console.h"
static void allocator_console_display_usage(const char *cmd)
{
    KERNEL_CONSOLE_PRINT("Flash buffer start: %p\r\n", ALLOCATOR_FLASH_ADDRESS);
    KERNEL_CONSOLE_PRINT("Flash buffer size: %d bytes\r\n", ALLOCATOR_FLASH_SIZE);
    KERNEL_CONSOLE_PRINT("Next addr to use: %p\r\n", allocator_last_flash_used);
    KERNEL_CONSOLE_PRINT("Available flash storage: %d bytes\r\n", (ALLOCATOR_FLASH_ADDRESS+ALLOCATOR_FLASH_SIZE)-allocator_last_flash_used);


    KERNEL_CONSOLE_PRINT("RAM buffer start: %p\r\n", allocator_ram_buffer);
    KERNEL_CONSOLE_PRINT("RAM buffer size: %d bytes\r\n", ALLOCATOR_RAM_SIZE);
    KERNEL_CONSOLE_PRINT("Next addr to use: %p\r\n", allocator_last_ram_used);
    KERNEL_CONSOLE_PRINT("Available RAM storage: %d bytes\r\n", (allocator_ram_buffer+ALLOCATOR_RAM_SIZE)-allocator_last_ram_used);
}
void  allocator_add_console_handler(void)
{
    kernel_console_add_handler("allocator_usage", "au", "Displays the flash allocator usage", allocator_console_display_usage);
}
#endif
