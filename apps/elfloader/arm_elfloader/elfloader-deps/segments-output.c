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
#include <rflpc17xx/rflpc17xx.h>

#include "../elfloader-otf.h"
#include "../elfloader-debug.h"

#include "allocator.h"

/* Code needed to write in flash */
#define FLASH_WRITE(ret, dst, src, len) do {PRINTF("Writing in flash: %p %d\r\n", dst, len); (ret) = rflpc_iap_write_buffer(dst, src, len);} while(0)

struct ram_output
{
    struct elfloader_output output;
    char *base;
    unsigned int offset, type;
    void *text;
    void *rodata;
    void *data;
    void *bss;
    void *flashLimit;
};

static void *
allocate_segment(struct elfloader_output * const output,
		 unsigned int type, int size)
{
    struct ram_output * const ram = (struct ram_output *)output;
  
    switch(type) {
	case ELFLOADER_SEG_TEXT:
	    /*if (ram->text) mem_free(ram->text, ram->textSize);*/
	    ram->text = allocator_flash_alloc(size);
	    return ram->text;

	case ELFLOADER_SEG_RODATA:
	    /*if (ram->rodata) free(ram->rodata, ram->rodataSize);*/
	    ram->rodata = allocator_flash_alloc(size);
	    return ram->rodata;

	case ELFLOADER_SEG_DATA:
	    /*if (ram->data) free(ram->data, ram->dataSize);*/
	    ram->data = allocator_ram_alloc(size);
	    return ram->data;

	case ELFLOADER_SEG_BSS:
	    /*if (ram->bss) free(ram->bss, ram->bssSize);*/
	    ram->bss = allocator_ram_alloc(size);
	    return ram->bss;
    }
    return 0;
}

static int
start_segment(struct elfloader_output *output,
	      unsigned int type, void *addr, int size)
{
    ((struct ram_output*)output)->base   = addr;
    ((struct ram_output*)output)->offset = 0;
    ((struct ram_output*)output)->type   = type;
    return ELFLOADER_OK;
}

static int
end_segment(struct elfloader_output *output)
{
    return ELFLOADER_OK;
}

static int
write_segment(struct elfloader_output *output, const char *buf,
	      unsigned int len)
{
    struct ram_output * const memory = (struct ram_output *)output;
    PRINTF("ram-segments.write Base %p + Ram Offset %x = %p (%d bytes)\r\n", memory->base, memory->offset, memory->base + memory->offset,len);
    PRINTF("Output->ops %p 0\r\n", output->ops);
    switch(memory->type) {
	case ELFLOADER_SEG_TEXT :
	case ELFLOADER_SEG_RODATA : {
	    int ret;

	    if(memory->flashLimit) {
		if( ((memory->base + memory->offset) >= (char *) memory->flashLimit) ) {
		    PRINTF("No more available flash memory\r\n");
		    return -2;
		}
	    }

	    PRINTF("Output->ops %p 1 Memory %p\r\n", output->ops, memory->base + memory->offset);
	    FLASH_WRITE(ret, memory->base + memory->offset, buf, len);
	    PRINTF("Output->ops %p 2\r\n", output->ops);
	    if(ret != 0) {
		PRINTF("An error happened while writing to flash %d\r\n", ret);
		return ret;
	    }
	}
	
	    break;
	default :
	    memcpy(memory->base + memory->offset, buf, len);
	    break;

    }

    memory->offset += len;

    return len;
}

static unsigned int
segment_offset(struct elfloader_output *output)
{
    return ((struct ram_output*)output)->offset;
}

static const struct elfloader_output_ops elf_output_ops =
{
    allocate_segment,
    start_segment,
    end_segment,
    write_segment,
    segment_offset
};

static struct ram_output seg_output = {
    {&elf_output_ops},
    0, 0,
    0,
    0, 0, 0, 0, 0
};

struct elfloader_output *codeprop_output = &seg_output.output;

void output_set_flash_limit(void *aLimit) {
    seg_output.flashLimit = aLimit;
}

