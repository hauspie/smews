/*
* Copyright or © or Copr. 2010, Thomas SOETE
* 
* Author e-mail: thomas@soete.org
* Library website : http://mbed.org/users/Alkorin/libraries/SimpleLib/
* 
* This software is governed by the CeCILL license under French law and
* abiding by the rules of distribution of free software.  You can  use, 
* modify and/ or redistribute the software under the terms of the CeCILL
* license as circulated by CEA, CNRS and INRIA at the following URL
* "http://www.cecill.info". 
* 
* As a counterpart to the access to the source code and  rights to copy,
* modify and redistribute granted by the license, users are provided only
* with a limited warranty  and the software's author,  the holder of the
* economic rights,  and the successive licensors  have only  limited
* liability. 
* 
* In this respect, the user's attention is drawn to the risks associated
* with loading,  using,  modifying and/or developing or reproducing the
* software by the user in light of its specific status of free software,
* that may mean  that it is complicated to manipulate,  and  that  also
* therefore means  that it is reserved for developers  and  experienced
* professionals having in-depth computer knowledge. Users are therefore
* encouraged to load and test the software's suitability as regards their
* requirements in conditions enabling the security of their systems and/or 
* data to be ensured and,  more generally, to use and operate it in the 
* same conditions as regards security. 
* 
* The fact that you are presently reading this means that you have had
* knowledge of the CeCILL license and that you accept its terms.
*/

#ifndef __SIMPLELIB_LEDS_H__
#define __SIMPLELIB_LEDS_H__

#include "mbed_globals.h"

/** Bits **/
#define LEDS_OFF 0
#define LED1 (1 << 18)
#define LED2 (1 << 20)
#define LED3 (1 << 21)
#define LED4 (1 << 23)
#define LEDS_MASK (LED1 | LED2 | LED3 | LED4)

/** Macros **/
#define LEDS_INIT()     LPC_GPIO1->FIODIR |= LEDS_MASK;

#define LEDS_SET(value) do {                                 \
                            LPC_GPIO1->FIOMASK = ~LEDS_MASK; \
                            LPC_GPIO1->FIOPIN = (value);     \
                        } while(0)

#endif