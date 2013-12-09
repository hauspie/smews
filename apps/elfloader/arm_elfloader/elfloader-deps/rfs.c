/*
 * Copyright (c) 2013, Gregory Guche, Michael Hauspie, Université Lille 1.
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
#include "../elfloader-debug.h"

#ifndef NULL
#define NULL ((void*)0)
#endif

void *memcpy(void *dest, const void *src, int n);

struct ram_fs_t {
    const char *base;
    const char *current;
    unsigned int size;
};

struct ram_fs_t RFS = {
    NULL, NULL, 0
};

void *rfs_open(void *aMemoryBank, int size) {
    RFS.base    = aMemoryBank;
    RFS.current = aMemoryBank;
    RFS.size = size;
    return &RFS;
}

void rfs_close(void *aHandle) {
    RFS.base    = 0;
    RFS.current = 0;
}

int rfs_seek(void *aHandle, int anOffset) {
    struct ram_fs_t *rfs = (struct ram_fs_t *)aHandle;

    if (anOffset >= rfs->size)
    {
	PRINTF("Failed to seek: %d %d\r\n", rfs->size, anOffset);
	return -1;
    }

    rfs->current = rfs->base + anOffset;
    return anOffset;
}
int rfs_read(void *aHandle, void *aBuffer, int aLength) {
    struct ram_fs_t *rfs = (struct ram_fs_t *)aHandle;

    

    if ((rfs->current - rfs->base) + aLength > rfs->size)
	aLength = (rfs->base+rfs->size) - rfs->current;
    if (aLength <= 0)
	return aLength;

    memcpy(aBuffer, rfs->current, aLength);
    rfs->current += aLength;
    return (aLength);
}
