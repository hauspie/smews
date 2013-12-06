#ifndef _ELF_ENV_H_
#define _ELF_ENV_H_

/* These are the symbols exported by the relocated code.
   The elf loader will look after the symbol elf_application_environement
   and will store its address in the elf_application_environement global variable.

   The elfloader is agnostic of the type of this struct, so it can be adapted
   for your application.

   In this sample, we get the function pointer that allows to blink some leds
*/
struct elf_application_environment_t {
    void (*step_leds)(void);
};

#endif /* _ELF_ENV_H_ */
