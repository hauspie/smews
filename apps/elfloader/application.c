#include "application.h"
#include "arm_elfloader/elfloader-deps/allocator.h"
#include "arm_elfloader/elfloader-deps/tiny-lib-c.h"

static struct elf_application_t application_buffer;

char application_add(const char *filename, uint16_t size, 
                     char *data_address, unsigned int data_size, 
                     struct elf_application_environment_t *environment) {
  struct elf_application_t *applicationInFlash;
  char   res;
  int    filenameLength;
  char   *data_source;

  if((filename == NULL) || (size == 0) || (environment == NULL))
		return 0;

  data_source = NULL;
  if(data_size > 0) {
    data_source = (char *)allocator_flash_alloc(data_size);
    if(APPLICATION_WRITE(data_source, data_address, data_size) != 0) {
      printf("FAILED to allocate data storage\r\n");
      return 0;
    }
  }

  if(environment->install) {
    int i = 0;
    while(environment->install[i] != NULL) {
      res = environment->install[i]();
      if(res != 0) {
        printf("Application %s failed to install (%d).\r\n", filename, res);
        return 0;
      }
      i++;
    }
  }

  /* Fill the application structure */
  /* +1 to keep the '\0' character */
  filenameLength = strlen(filename) + 1;
  application_buffer.filename = allocator_flash_alloc(filenameLength);
  if(APPLICATION_WRITE(application_buffer.filename, filename, filenameLength) != 0) {
    printf("FAILED TO WRITE application filename\r\n");
    return 0;
  }

  printf("Application name is %s\r\n", application_buffer.filename);

  application_buffer.size             = size;
  application_buffer.environment      = environment;
  application_buffer.parsing          = NULL;
  application_buffer.data_destination = data_address;
  application_buffer.data_source      = data_source;
  application_buffer.data_size        = data_size;

  applicationInFlash = (struct elf_application_t *)allocator_flash_alloc(sizeof(struct elf_application_t));
  
  res = APPLICATION_WRITE(applicationInFlash, &application_buffer, sizeof(struct elf_application_t));

  printf("Application In Flash : name %s, size %d, environment %p, parsing : %p\r\n",
         applicationInFlash->filename, applicationInFlash->size, applicationInFlash->environment, applicationInFlash->parsing);

  return elf_application_add(applicationInFlash);
}

void application_remove(const char *filename) {
  if(all_applications != NULL) {
    struct elf_application_t *application = all_applications;
    while(application) {
      if(strcmp(filename, application->filename) == 0) {

        elf_application_remove(application);

        if(application->environment->remove) {
          int i = 0;
          while(application->environment->remove[i] != NULL) {
            application->environment->remove[i]();
            i++;
          }
        }
	// @WARNING We should deallocate memory here but doesn't have any free function in elf_allocator.
	return;
      }
      application = application->next;
    }
  }
}
