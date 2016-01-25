#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>

unsigned long timer = 0;

ISR(TIM0_OVF_vect) {
    
}

void cpuInit ();

int main() {

    cpuInit();
    
    for (;;) {

    }
}

void cpuInit () {
    /*
     * Nastaveni citace pro blikani
     */
    TCCR0B |= (1 << CS00) | (1 << CS02);
    TIMSK0 = 0;
    TIMSK0 = (1 << TOIE0);

    // povoleni preruseni
    sei();
}
