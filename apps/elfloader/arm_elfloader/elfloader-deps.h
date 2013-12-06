/*
 * Copyright (c) 2013, Michaël Hauspie, Université Lille 1.
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

/* This file contains the signatures of the function needed by the elfloader.
   To use the elfloader, you must implement these functions in your code
*/
#ifndef _ELFLOADER_DEPS_H_
#define _ELFLOADER_DEPS_H_

#include <stddef.h> /* for size_t */

/************* LIBC standard functions *********************/
/* Following are the prototypes of the libc functions used by the elfloader.
   If your target does not provide libc, you must implement compatible ones.
*/

/** 
 * Performs a string comparison. Must comply with strcmp from libc
 */
int strcmp(const char *s1, const char *s2);

/** 
 * Performs a string comparison of the n first characters. Must comply with strncmp from libc
 */
int strncmp(const char *s1, const char *s2, size_t n);


/** 
 * Performs a memory comparison. Must comply with memcmp from libc.
 */
int memcmp(const void *s1, const void *s2, size_t n);

/** 
 * Performs a memory copy. Must comply with memcpy from libc.
 */
void *memcpy(void *dest, const void *src, size_t n);

/************ elf file access **********************/
/* This is the interface used by the elfloader to read the elf file it needs to
 * dynamically link.
 */

/** 
 * Reads len bytes from a file in buf
 * 
 * @param fd the descriptor of the file
 * @param buf pointer to a buffer to store read bytes
 * @param len maximum number of bytes to read
 * 
 * @return -1 if error, 0 if EOF, number of bytes actually read otherwise
 */
int elf_read(void *fd, char *buf, int len);

/** 
 * Seeks at offset in the giver file
 * 
 * @param fd the descriptor of the file
 * @param offset the offset to seek to in bytes
 * 
 * @return the new offset or -1 if error
 */
int elf_seek(void *fd, int offset);


#endif /* _ELFLOADER-DEPS_H_ */
