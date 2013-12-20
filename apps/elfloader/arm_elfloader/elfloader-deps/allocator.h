#ifndef __ALLOCATOR_H__
#define __ALLOCATOR_H__

extern void *allocator_ram_alloc(unsigned int size);

extern void *allocator_flash_alloc(unsigned int size);

#ifdef KERNEL_CONSOLE
extern void allocator_add_console_handler(void);
#endif

#endif
