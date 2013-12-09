/*
<generator>
	<handlers init="initElfLoader" doPostOut="doPostOut" doPostIn="doPostIn"/>
	<content-types>
		<content-type type="application/x-object"/>
	</content-types>
	
</generator>
*/

#include "arm_elfloader/elfloader-otf.h"
#include "arm_elfloader/elfloader-deps/allocator.h"
#include "arm_elfloader/elfloader-deps/rfs.h"
#include "application.h"

#define DEBUG
#ifdef DEBUG
#define PRINTF(...) printf(__VA_ARGS__)
#else
#define PRINTF(...) do {} while(0)
#endif

struct file_t {
  char *filename;
  uint16_t size;
};

/* elf loader*/
const char *elf_loader_return_labels[] = {
 "ok", "Bad Elf Header", "No Symbol Table", "No String Table", "No Text section", "Symbol not found", "Segment not found", "No StartPoint",
 "Unhandled Relocation", "Out Of Range", "Relocation Not Sorted", "Input Error", "Output Error"
};

/* Flash temp buffer */
#ifndef ELF_ALLOCATOR_FLASH_STORAGE_ADDRESS
#define ELF_ALLOCATOR_FLASH_STORAGE_SIZE (16*1024) /* The maximum elf size that smews will be able to load is 16kB */
const char allocator_flash_storage_space[ELF_ALLOCATOR_FLASH_STORAGE_SIZE] __attribute__ ((section(".flash_storage"))) = {0};
#define ELF_ALLOCATOR_FLASH_STORAGE_ADDRESS (allocator_flash_storage_space)
#endif
const void * elf_allocator_storage = ELF_ALLOCATOR_FLASH_STORAGE_ADDRESS;


/* Pointer to the output handler (which will actually write the relocated code) */
extern struct elfloader_output *codeprop_output;


#ifdef DEBUG
void flash_dump() {
  int i, index, maxInfosPerLine;
  int allocatorSize = 256;
  char *flash = (char *)elf_allocator_storage;

  maxInfosPerLine = 16;
  
  PRINTF("\r\nFlash Dump:\r\n");
  PRINTF("---------\r\n");

  index = 0;
  while(allocatorSize > maxInfosPerLine) {

    PRINTF("%p ", flash + index);

    for(i = 0; i < maxInfosPerLine; i++, index++)
      PRINTF("%02X, ", flash[index]);

    PRINTF("\r\n");
    allocatorSize -= maxInfosPerLine;
  }

  if(allocatorSize>0) {
    PRINTF("%p ", flash + index);
    for(i = 0; i < allocatorSize; i++, index++)
      PRINTF("%02X, ", flash[index]);
    PRINTF("\r\n");
  }

  PRINTF("\r\n");
}
#endif
/*-----------------------------------------------------------------------------*/
static char initElfLoader() {
  
  elf_applications_init(allocator_flash_alloc, NULL);
  return 1;
}

/*-----------------------------------------------------------------------------*/
/* Buffered write to flash */
#define STORAGE_BUFFER_SIZE 512
struct flash_buffer {
    int ram_offset;
    int flash_offset;
    uint8_t storage_buffer[STORAGE_BUFFER_SIZE];
};
static struct flash_buffer flash_buffer;
static void flash_buffer_reset(void)
{
    PRINTF("Reset flash buffer\r\n");
    flash_buffer.ram_offset = 0;
    flash_buffer.flash_offset = 0;
}
static int flash_buffer_flush(void)
{
    if (flash_buffer.ram_offset <= 0)
	return 0;
    PRINTF("Flushing %d bytes\r\n", flash_buffer.ram_offset);
    if(APPLICATION_WRITE(((uint8_t *)elf_allocator_storage) + flash_buffer.flash_offset, flash_buffer.storage_buffer, STORAGE_BUFFER_SIZE) != 0) {
        PRINTF("An error happened while flushing elf to storage\r\n");
        return -1;
    }
}
static int flash_buffer_write_byte(uint8_t value)
{
    
    if (flash_buffer.flash_offset >=  ELF_ALLOCATOR_FLASH_STORAGE_SIZE)
    {
	PRINTF("No more flash space for receiving elf file\r\n");
	return -1;
    }
    if(flash_buffer.ram_offset < STORAGE_BUFFER_SIZE) 
    {
	flash_buffer.storage_buffer[flash_buffer.ram_offset] = value;
	flash_buffer.ram_offset++;
    } 
    else 
    {
	PRINTF("Writing buffer to flash offset %d\r\n", flash_buffer.flash_offset);
	/* Commit buffer */
	if(APPLICATION_WRITE(((uint8_t *)elf_allocator_storage) + flash_buffer.flash_offset, flash_buffer.storage_buffer, STORAGE_BUFFER_SIZE) != 0) {
	    PRINTF("An error happened while flashing elf to storage\r\n");
	    return -1;
      }

      flash_buffer.flash_offset += STORAGE_BUFFER_SIZE;
      flash_buffer.storage_buffer[0] = value;
      flash_buffer.ram_offset = 1;
    }
    return 0;
}
/* End of flash buffer functions */
/*-----------------------------------------------------------------------------*/



/*-----------------------------------------------------------------------------*/
static char doPostIn(uint8_t content_type, /*uint16_t content_length,*/ uint8_t call_number, 
                     char *filename, void **post_data) {
  uint16_t i = 0;
  short value;
  PRINTF("%s IN\r\n", __FUNCTION__);

  if(!filename)  return 1;

  /* Leave when data is already available.. */
  if(*post_data) return 1;

  struct file_t *file = mem_alloc(sizeof(struct file_t));
  if(!file)
    return 1;

  /* Filename */
  while(filename[i++] != '\0');

  file->filename = mem_alloc(i * sizeof(char));
  if(!file->filename) {
    mem_free(file, sizeof(struct file_t));
    return 1;
  }

  i = 0;
  do {
    file->filename[i] = filename[i];
  }while(filename[i++] != '\0');

  /* When receiving the elf file from post, 
     store it directly in flash without relocation.
     The relocation will be performed in the postOut handler.

     File writes to flash are buffered using the storage_buffer RAM buffer.
   */
  i = 0;
  flash_buffer_reset();
  while((value = in()) != -1) {
      if (flash_buffer_write_byte(value) == -1)
	  return 1;
      i++;
  }
  if (flash_buffer_flush() == -1)
      return 1;

  file->size = i;

  /* The post_data pointer is used to retrieve the file structure in the postOut handler */
  *post_data = file;
  return 1;
}

void clean_up(struct file_t *file) {
    uint16_t i = 0;
    while(file->filename[i++] != '\0');

    mem_free(file->filename, i * sizeof(char));
    mem_free(file, sizeof(struct file_t));
}

/* Implements functions needed by elfloader (see elfloader-deps.h) */
int elf_read(void *fd, char *buf, int len)
{
    return rfs_read(fd, buf, len);
}

int elf_seek(void *fd, int offset)
{
    return rfs_seek(fd, offset);
}


/*-----------------------------------------------------------------------------*/
static char doPostOut(uint8_t content_type, void *data) {

    struct file_t *file =  (struct file_t*)data;
    void *storage_handle;
    int loading;

    PRINTF("%s IN\r\n", __FUNCTION__);
    if (!file)
    {
	out_str("Please provide a file");
	return 1;
    }

  
    /* Open the flash memory zone where the original elf file (not relocated)
       has been stored in the doPostIn handler. The handle will allow the elf
       loader to perform seeks and reads in the elf_file
    */
    storage_handle = rfs_open((void *)elf_allocator_storage, file->size);
  
    if(storage_handle == NULL) {
	out_str("Unable to open elf storage");
	clean_up(file);
	return 1;
    }

    elfloader_init();
    PRINTF("ElfLoader loading...\r\n");
    /* Perform the actual relocation of the elf file.  The elf will be read
       thanks to the storage_handle 'pseudo filesystem' and will be writen
       thanks to the functions pointed by the structure codeprop_outputs.  The
       implementations of the later function are given in the
       arm_elfloader/elfloader-deps/segments-ouput.c file
    */
    loading = elfloader_load(storage_handle, codeprop_output);

    PRINTF("Loading = %d\r\n", loading);
    if(loading == ELFLOADER_OK) {
	/*flash_dump();*/
	PRINTF("Elf Application Environment is %p\r\n", elf_application_environment);

	PRINTF("Install function is %p\r\n", elf_application_environment->install);
	PRINTF("Remove function is %p\r\n", elf_application_environment->remove);
	PRINTF("URLS Tree is %p\r\n", elf_application_environment->urls_tree);
	PRINTF("Resources index is %p\r\n", elf_application_environment->resources_index);

	PRINTF("Resources index[0] %p\r\n", elf_application_environment->resources_index[0]);
	PRINTF("Resources index[1] %p\r\n", elf_application_environment->resources_index[1]);
	PRINTF("Resources index[2] %p\r\n", elf_application_environment->resources_index[2]);
	PRINTF("Resources index[3] %p\r\n", elf_application_environment->resources_index[3]);

	/* The elf_application_enfironment is a pointer to a structure that is exported by the loaded elf file.
	   This structure holds function pointers to install and remove function as well as pointers
	   to the urls_tree parsing tree and resources_index array (the resources provided by the loaded elf file).
	*/
	if(!application_add(file->filename, file->size, data_address, data_size, elf_application_environment)) {
	    out_str("Failed to add application ");
	    out_str(file->filename);
	    out_str(".");
	    PRINTF("Failed to add application %s.\r\n", file->filename);
	    clean_up(file);
	    return 1;
	} 

	out_str("The file \"");
	out_str(file->filename);
	out_str("\" has been uploaded successfully (");
	out_uint(file->size);
	out_str(" bytes)\n");

    } else {

	if(loading < 0) {
	    out_str("An internal error happened\r\n");
	} else {
	    out_str("An error happened while loading ");
	    out_str(file->filename);
	    out_str(" : ");
	    out_str(elf_loader_return_labels[loading]);
	}

	rfs_close(storage_handle);
	clean_up(file);

    }
    PRINTF("%s OUT\r\n", __FUNCTION__);
    return 1;
}
