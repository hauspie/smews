/*
 * Copyright (c) 2005, Swedish Institute of Computer Science
 * Copyright (c) 2007, Simon Berg
 * Copyright (c) 2013, Gregory Guche, Michaël Hauspie, Université Lille 1
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
 * This file is part of the Contiki operating system.
 *
 */


#include <stdint.h>
#include "elfloader-arch-otf.h"
#include "elfloader-deps.h"
#include "elfloader-debug.h"

#define ELF32_R_TYPE(info)      ((unsigned char)(info))


/*Elf32_ST_TYPE*/
#define STT_NOTYPE  0
#define STT_OBJECT  1
#define STT_FUNC    2
#define STT_SECTION 3
#define STT_FILE    4
#define STT_LOPROC  13
#define STT_HIPROC  15

#define ELF32_ST_TYPE(i)        ((i)&0xf)


/* Supported relocations */
#define R_ARM_ABS32	2
#define R_ARM_THM_CALL	10
#define R_ARM_THM_MOVW_ABS_NC 47
#define R_ARM_THM_MOVT_ABS    48

struct mov_relocation_data {
  int offsets[4];
  int mask;
};

const struct mov_relocation_data movw_relocation_data = {
	{12, 11, 8, 0}, 0xFFFF
};

const struct mov_relocation_data movt_relocation_data = {
	{28, 27, 24, 16}, 0xFFFF0000
};

/* Adapted from elfloader-avr.c */
int
elfloader_arch_relocate(void *input_fd,
			struct elfloader_output *output,
			unsigned int sectionoffset,
			char *sectionaddr,
                        struct elf32_rela *rela, char *addr,
			struct elf32_sym *symbol)
{
  unsigned int type;

  type = ELF32_R_TYPE(rela->r_info);
  elf_seek(input_fd, sectionoffset + rela->r_offset);

/*   PRINTF("elfloader_arch_relocate: type %d\n", type);
   PRINTF("Addr: %p, Addend: %ld\n",   addr, rela->r_addend); */
  switch(type) {
  case R_ARM_ABS32:
    {
      int32_t addend;
      elf_read(input_fd, (char*)&addend, 4);
      addr += addend;
      elfloader_output_write_segment(output,(char*) &addr, 4);
      /*PRINTF("%p: addr: %p addend %p\r\n", sectionaddr +rela->r_offset,
	     addr, addend);*/
    }
    break;

  case R_ARM_THM_CALL: {
	uint16_t instr[2];
	int32_t offset;
	int32_t addend;

        elf_read(input_fd, (char *)instr, 4);

        // Build the addend from the instructions
	addend = (instr[0] & 0x7FF) << 12 | (instr[1] & 0x7FF) << 1;

	// Sign extent, when we have a negative number, we preserve it through shifting.
	if(addend & (1<<22))
	{
		//PRINTF("%x\r\n", addend);
		addend |= 0xFF8<<20;
		//PRINTF("%x\r\n", addend);
	}

	//PRINTF("R_ARM_THM_CALL addend : %x %d\r\n",addend, addend);
	// S + A
	offset = addend + (uint32_t)addr;

	//PRINTF("R_ARM_THM_CALL S + A : %x\r\n",offset);

	if(ELF32_ST_TYPE(symbol->st_info) == STT_FUNC) {
		// (S + A) | T
		offset |= 0x1;
		//PRINTF("elfloader-arm.c: R_ARM_THM_CALL Symbol is STT_FUNC\r\n");
	}

	//PRINTF("R_ARM_THM_CALL OFFSET (S + A) | T : %x\r\n",offset);

	// ((S+A) | T) - P
	offset = offset - ((uint32_t)sectionaddr + (rela->r_offset));

	//PRINTF("R_ARM_THM_CALL ((S+A) | T) - P: %x\r\n",offset);

	instr[0] = ((offset >> 12) & 0x7FF) | 0xF000;
	instr[1] = ((offset >> 1) & 0x7FF) | 0xF800;

	/*PRINTF("R_ARM_THM_CALL after relocation: %04x %04x\r\n",instr[0], instr[1]);*/
	elfloader_output_write_segment(output, (char*)instr, 4);
  }
   break;


  case R_ARM_THM_MOVW_ABS_NC : 
  case R_ARM_THM_MOVT_ABS : {
	uint16_t instr[2];
	uint32_t mask;
	int16_t addend = 0;
	uint32_t val;
	const struct mov_relocation_data *mov_relocation_data = 
		( type == R_ARM_THM_MOVW_ABS_NC ) ?
			&movw_relocation_data : &movt_relocation_data;

	elf_read(input_fd, (char*)instr, 4);

	/*PRINTF("elfloader-arm.c: relocation %d\r\n", type);
	PRINTF("elfloader-arm.c: R_ARM_THM_MOV before relocation %x %x\r\n", instr[0], instr[1]);*/

	// Build the 16 bit addend from the instructions
	addend |= (instr[0] & 0xF) << 12;
	addend |= ((instr[0] >> 10) & 0x1) << 11;
	addend |= ((instr[1]  >> 12) & 0x7) << 8;
	addend |= instr[1] & 0xF;

	/*PRINTF("A: %x %d\r\n", addend, addend);
	PRINTF("S: %x %d\r\n", addr, addr);*/

	// S + A
      val = (uint32_t) addr + addend;
      //PRINTF("S+A %d %x\r\n", val, val);
	
	if(type == R_ARM_THM_MOVW_ABS_NC) {
	// We are in thumb mode, we just have to check whether the symbol type is STT_FUNC
		if(ELF32_ST_TYPE(symbol->st_info) == STT_FUNC) {
			// (S + A) | T
			val = val | 0x1;
			//PRINTF("elfloader-arm.c: R_ARM_THM_MOVW_ABS_NC Symbol is STT_FUNC\r\n");
		}
	}

	// Result_Mask
        mask = val & mov_relocation_data->mask;

	instr[0] &= ~0xF;
	instr[0] |= (mask  >> mov_relocation_data->offsets[0]) & 0xF;
	instr[0] &= ~(1<<10);
	instr[0] |= ((mask >> mov_relocation_data->offsets[1]) & 0x1)<<10;
	
	instr[1] &= ~(0x7<<12);
	instr[1] |= ((mask >> mov_relocation_data->offsets[2]) & 0x7)<<12;
	instr[1] &= ~0xFF;
        instr[1] |= (mask >> mov_relocation_data->offsets[3]) & 0xFF;
	
        //PRINTF("elfloader-arm.c: R_ARM_THM_MOV after relocation %x %x\r\n", instr[0], instr[1]);
	elfloader_output_write_segment(output, (char*)instr, 4);
  }
  break;

  default:
    PRINTF("elfloader-arm.c: unsupported relocation type %d\n", type);
    return ELFLOADER_UNHANDLED_RELOC;
  }

  return ELFLOADER_OK;
}
