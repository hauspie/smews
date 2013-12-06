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

/* RAM */
#ifndef ALLOCATOR_RAM_SIZE
#define ALLOCATOR_RAM_SIZE 1024*10
#endif

/* FLASH */
#ifndef ALLOCATOR_FLASH_ADDRESS
extern char _text_end; /* defined by the link script to get the address of the end of the text space */
extern char _data_start;
extern char _data_end;
/* Get the first available free space in eeprom to store the data */
#define ALLOCATOR_FLASH_ADDRESS ((&_text_end) + (&_data_end - &_data_start))
#endif

static char allocator_ram_buffer[ALLOCATOR_RAM_SIZE];
static char *allocator_last_ram_used = 0;

static char *allocator_flash_buffer = 0;
static char *allocator_last_flash_used   = 0;

void *allocator_ram_alloc(unsigned int size) {
    char *result;	
    if(allocator_last_ram_used == 0)
	allocator_last_ram_used = allocator_ram_buffer;

    result = allocator_last_ram_used;
    allocator_last_ram_used += ((size & 1) == 0) ? size : size + 1; /* align on an even address */
    return result;
}

void *allocator_flash_alloc(unsigned int size) {
    char *result;	
    if (allocator_flash_buffer == 0)
	allocator_flash_buffer = ALLOCATOR_FLASH_ADDRESS;
    if(allocator_last_flash_used == 0)
	allocator_last_flash_used = (char *)allocator_flash_buffer;

    result = allocator_last_flash_used;
    allocator_last_flash_used += ((size & 1) == 0) ? size : size + 1; /* align on an even address */
    return result;
}
