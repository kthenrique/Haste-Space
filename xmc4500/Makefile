################################################################################
# USAGE:
# make           .... build the program image
# make debug     .... build the program image and invoke gdb
# make flash     .... build an flash the application
# make erase     .... re-initialize (erase) the memory of the chip 
# make doc       .... run doxygen - output will be in > doc
# make clean     .... remove intermediate and generated files

################################################################################
# define the name of the generated output file
#
TARGET        = main

################################################################################
# below only edit with care
#
BIN           = ./bin
SYS           = ./system
XMCLIB        = ./xmclib
SRCDIR        = ./src
INCDIR        = ./inc
SRC           = $(wildcard src/*.c)
VENDOR        = Infineon
TOOLCHAIN     = arm-none-eabi
UC            = XMC4500
UC_ID         = 4503
DEVICE        = XMC4500_F100x1024
CPU           = cortex-m4
FPU           = fpv4-sp-d16
FABI          = softfp  #soft, softfp, hard
LIBS          = -larm_cortexM4lf_math
LIBS         += -lxmclibcstubs
GDB_ARGS      = -ex "target remote :2331"
GDB_ARGS     += -ex "monitor reset"
GDB_ARGS     += -ex "load"
GDB_ARGS     += -ex "monitor reset"
# uncomment the following line for semi-hosted debugging and comment the
# RTT option below
#
GDB_ARGS     += -ex "monitor SWO EnableTarget 16000000 0 1 0"
#
# set the Region of the RTT Block manually
# GDB_ARGS     += -ex "monitor exec SetRTTAddr 0x20000C20"

CMSIS         = $(SYS)/CMSIS
CMSIS_INCDIR  = $(CMSIS)/Include
CMSIS_LIBDIR  = $(CMSIS)/Lib/GCC
CMSIS_DSPLIB  = $(CMSIS)/DSP_Lib/Source
INF_INCDIR    = $(CMSIS)/$(VENDOR)/Include
INF_LIBDIR    = $(CMSIS)/$(VENDOR)/Lib
XMC_INCDIR    = $(CMSIS)/$(VENDOR)/$(UC)_series/Include
XMC_LIBDIR    = $(CMSIS)/$(VENDOR)/$(UC)_series/Lib
XMC_SRCDIR    = $(CMSIS)/$(VENDOR)/$(UC)_series/Source
XMC_GCCDIR    = $(CMSIS)/$(VENDOR)/$(UC)_series/Source/GCC
XMC_LIBINCDIR = $(XMCLIB)/inc
XMC_LIBSRCDIR = $(XMCLIB)/src

INF_SRC       = $(INF_LIBDIR)/System_LibcStubs.c
XMC_SRC       = $(XMC_SRCDIR)/system_XMC4500.c
XMC_ASRC      = $(XMC_GCCDIR)/startup_XMC4500.S
#LINKER_FILE   = $(XMC_GCCDIR)/xmc4500-1024.ld
LINKER_FILE   = $(XMC_GCCDIR)/XMC4500x1024.ld
XMC_LIBSRC    = $(wildcard $(XMC_LIBSRCDIR)/*.c)

LIBS_DIR      = -L$(CMSIS_LIBDIR)
LIBS_DIR     += -L$(INF_LIBDIR)
LIBS_DIR     += -L$(XMC_LIBDIR)

AS   = $(TOOLCHAIN)-as
CC   = $(TOOLCHAIN)-gcc
CP   = $(TOOLCHAIN)-objcopy
OD   = $(TOOLCHAIN)-objdump
GDB  = $(TOOLCHAIN)-gdb
SIZE = $(TOOLCHAIN)-size

CFLAGS = -mthumb -mcpu=$(CPU)
CFLAGS+= -mfpu=$(FPU)
CFLAGS+= -mfloat-abi=$(FABI)
CFLAGS+= -fstack-usage
CFLAGS+= -O0
CFLAGS+= -ffunction-sections -fdata-sections
CFLAGS+= -MD -std=c99 -Wall -fms-extensions
CFLAGS+= -DUC_ID=$(UC_ID) -DARM_MATH_CM4 -D$(DEVICE)
CFLAGS+= -g3 -fmessage-length=0
CFLAGS+= -I$(SRCDIR)
CFLAGS+= -I$(CMSIS_DSPLIB)/BasicMathFunctions
CFLAGS+= -I$(CMSIS_DSPLIB)/CommonTables
CFLAGS+= -I$(CMSIS_DSPLIB)/ComplexMathFunctions
CFLAGS+= -I$(CMSIS_DSPLIB)/ControllerFunctions
CFLAGS+= -I$(CMSIS_DSPLIB)/FastMathFunctions
CFLAGS+= -I$(CMSIS_DSPLIB)/FilteringFunctions
CFLAGS+= -I$(CMSIS_DSPLIB)/MatrixFunctions
CFLAGS+= -I$(CMSIS_DSPLIB)/StatisticsFunctions
CFLAGS+= -I$(CMSIS_DSPLIB)/SupportFunctions
CFLAGS+= -I$(CMSIS_DSPLIB)/TransformFunctions
CFLAGS+= -I$(SYS)
CFLAGS+= -I$(CMSIS_INCDIR)
CFLAGS+= -I$(INF_INCDIR)
CFLAGS+= -I$(XMC_INCDIR)
CFLAGS+= -I$(XMC_LIBINCDIR)
CFLAGS+= -I$(INCDIR)
AFLAGS = -x assembler-with-cpp
LFLAGS = -nostartfiles $(LIBS_DIR) -Wl,--gc-sections -Wl,-Map=bin/$(TARGET).map
CPFLAGS = -Obinary
ODFLAGS = -S

OBJS = $(SRC:.c=.o)
OBJS+= $(INF_SRC:.c=.o)
OBJS+= $(XMC_SRC:.c=.o)
OBJS+= $(XMC_LIBSRC:.c=.o)
OBJS+= $(XMC_ASRC:.asm=.o)

#### Rules ####
all: $(OBJS) $(TARGET).elf $(TARGET)

%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@
	@echo ""
	

%.o: %.asm
	$(CC) -c $(CFLAGS) $(AFLAGS) $< -o $@
	@echo ""
	


$(TARGET).elf: $(OBJS)
ifeq ($(shell echo "check_quotes"),"check_quotes")
	mkdir $(subst /,\\,$(BIN)) || (exit 0)
else
	mkdir -p bin/
endif
	$(CC) -T $(LINKER_FILE) $(LFLAGS) $(CFLAGS) -o $(BIN)/$(TARGET).elf $(OBJS) $(LIBS)
	@echo ""
	

$(TARGET): $(TARGET).elf
	$(CP) $(CPFLAGS) $(BIN)/$(TARGET).elf $(BIN)/$(TARGET).bin
	@echo ""
	$(OD) $(ODFLAGS) $(BIN)/$(TARGET).elf > $(BIN)/$(TARGET).lst
	@echo ""
	$(SIZE) $(BIN)/$(TARGET).elf

debug: $(TARGET)
ifeq ($(shell echo "check_quotes"),"check_quotes")
# optional: starts a new instance the JLinkGDBServer every time
	CMD /C start JLinkGDBServer -Device XMC4500-1024 -if SWD
else
	xterm -e "JLinkGDBServer -Device XMC4500-1024 -if SWD" &
	sleep 1 && xterm -e "telnet localhost 2333" & 
endif
	$(GDB) -q $(BIN)/$(TARGET).elf $(GDB_ARGS)


flash: $(TARGET)
ifeq ($(shell echo "check_quotes"),"check_quotes")
	(echo h && echo loadbin $(BIN)/$(TARGET).bin,0xC000000 && echo r && echo g && echo q) | JLink -Device XMC4500-1024 -if SWD -speed 4000
else
	echo -e 'h\nloadbin bin/$(TARGET).bin,0xC000000\nr\ng\nq' | JLinkExe -Device XMC4500-1024 -if SWD -speed 4000
endif

erase: $(TARGET)
ifeq ($(shell echo "check_quotes"),"check_quotes")
	(echo erase && echo r && echo q) | JLink -Device XMC4500-1024 -if SWD -speed 4000
else
	echo -e 'erase\nr\nq' | JLinkExe -Device XMC4500-1024 -if SWD -speed 4000
endif

doc: $(TARGET)
	doxygen

clean:
	rm -rf *~
	rm -f $(BIN)/*
	rm -f $(SRCDIR)/*.o $(SRCDIR)/*.d $(SRCDIR)/*.su  $(SRCDIR)/*~
	rm -f $(CMSIS_DSPLIB)/BasicMathFunctions/*.o $(CMSIS_DSPLIB)/BasicMathFunctions/*.d $(CMSIS_DSPLIB)/BasicMathFunctions/*.su $(CMSIS_DSPLIB)/BasicMathFunctions/*~
	rm -f $(CMSIS_DSPLIB)/CommonTables/*.o $(CMSIS_DSPLIB)/CommonTables/*.d $(CMSIS_DSPLIB)/CommonTables/*.su $(CMSIS_DSPLIB)/CommonTables/*~
	rm -f $(CMSIS_DSPLIB)/ComplexMathFunctions/*.o $(CMSIS_DSPLIB)/ComplexMathFunctions/*.d $(CMSIS_DSPLIB)/ComplexMathFunctions/*.su $(CMSIS_DSPLIB)/ComplexMathFunctions/*~	
	rm -f $(CMSIS_DSPLIB)/ControllerFunctions/*.o $(CMSIS_DSPLIB)/ControllerFunctions/*.d $(CMSIS_DSPLIB)/ControllerFunctions/*.su $(CMSIS_DSPLIB)/ControllerFunctions/*~
	rm -f $(CMSIS_DSPLIB)/FastMathFunctions/*.o $(CMSIS_DSPLIB)/FastMathFunctions/*.d $(CMSIS_DSPLIB)/FastMathFunctions/*.su $(CMSIS_DSPLIB)/FastMathFunctions/*~
	rm -f $(CMSIS_DSPLIB)/FilteringFunctions/*.o $(CMSIS_DSPLIB)/FilteringFunctions/*.d $(CMSIS_DSPLIB)/FilteringFunctions/*.su $(CMSIS_DSPLIB)/FilteringFunctions/*~
	rm -f $(CMSIS_DSPLIB)/MatrixFunctions/*.o $(CMSIS_DSPLIB)/MatrixFunctions/*.d $(CMSIS_DSPLIB)/MatrixFunctions/*.su $(CMSIS_DSPLIB)/MatrixFunctions/*~
	rm -f $(CMSIS_DSPLIB)/StatisticsFunctions/*.o $(CMSIS_DSPLIB)/StatisticsFunctions/*.d $(CMSIS_DSPLIB)/StatisticsFunctions/*.su $(CMSIS_DSPLIB)/StatisticsFunctions/*~
	rm -f $(CMSIS_DSPLIB)/SupportFunctions/*.o $(CMSIS_DSPLIB)/SupportFunctions/*.d $(CMSIS_DSPLIB)/SupportFunctions/*.su $(CMSIS_DSPLIB)/SupportFunctions/*~
	rm -f $(CMSIS_DSPLIB)/TransformFunctions/*.o $(CMSIS_DSPLIB)/TransformFunctions/*.d $(CMSIS_DSPLIB)/TransformFunctions/*.su $(CMSIS_DSPLIB)/TransformFunctions/*~	
	rm -f $(INCDIR)/*.o $(INCDIR)/*.d $(INCDIR)/*.su  $(INCDIR)/*~
	rm -f $(SYS)/*.o $(SYS)/*.d $(SYS)/*.su $(SYS)/*~
	rm -f $(XMC_SRCDIR)/*.o $(XMC_SRCDIR)/*.d $(XMC_SRCDIR)/*.su $(XMC_SRCDIR)/*~
	rm -rf $(XMC_GCCDIR)/*.o $(XMC_GCCDIR)/*.d $(XMC_GCCDIR)/*.su $(XMC_GCCDIR)/*~
	rm -rf $(XMC_LIBSRCDIR)/*.o $(XMC_LIBSRCDIR)/*.su $(XMC_LIBSRCDIR)/*.d $(XMC_LIBSRCDIR)/*~
	rm -rf $(INF_LIBDIR)/*.o $(INF_LIBDIR)/*.su $(INF_LIBDIR)/*.d $(INF_LIBDIR)/*~ 
	rm -rf doc/html
