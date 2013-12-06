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
#include "tiny-lib-c.h"

/* not written for speed*/
int memcmp(const void *aPointer, const void *anotherPointer, int aSize) {
  const char *pointer = (const char *) aPointer;
  const char *nother  = (const char *) aPointer;
  int i = 0;
  for(i = 0; i < aSize; i++) {
    if(pointer[i] != nother[i])
	return pointer[i] - nother[i];
  }
  return 0;
}

int strlen(const char *aString) {
  int i = 0;
  while(aString[i] != '\0')
	i++;
  return i;
}

int strcmp(const char *aString, const char *anotherString) {
  while (*aString == *anotherString && *aString != '\0')
  {
	aString++;anotherString++;
  }
  return *aString - *anotherString;
}

int strncmp(const char *aString, const char *anotherString, int aSize) {
  while (*aString == *anotherString && *aString != '\0' && --aSize) {
	aString++;anotherString++;
  }
  return *aString - *anotherString;
}

