PRG            = main
OBJ            = main.o
MCU_TARGET     = attiny24
OPTIMIZE       = -O2
F_CPU          = 8000000

# You should not have to change anything below here.

CC             = avr-gcc

# Override is only needed by avr-lib build system.

override CFLAGS =  -Wall $(OPTIMIZE) -mmcu=$(MCU_TARGET) $(DEFS) -DF_CPU=$(F_CPU)

OBJCOPY        = avr-objcopy
OBJDUMP        = avr-objdump

all: hex

$(PRG).elf: $(OBJ)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ $(LIBS)

clean:
	rm -rf *.o $(PRG).elf $(PRG).hex

hex:  $(PRG).hex

%.hex: %.elf
	$(OBJCOPY) -j .text -j .data -O ihex $< $@

install: load

load: $(PRG).hex
	avrdude -P usb -p t24 -c dragon_hvsp -U hfuse:w:0xfe:m -U flash:w:$<

load1: $(PRG).hex
	avrdude -P usb -p m24 -c usbtiny -U flash:w:$<

status:
	avrdude -P usb -p t24 -c dragon_hvsp -v
