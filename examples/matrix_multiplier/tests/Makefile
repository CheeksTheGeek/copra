# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

TOPLEVEL_LANG ?= verilog
SIM ?= icarus

PWD=$(shell pwd)

# Matrix parameters
DATA_WIDTH ?= 32
A_ROWS ?= 10
B_COLUMNS ?= 4
A_COLUMNS_B_ROWS ?= 6

ifeq ($(TOPLEVEL_LANG),verilog)
    VERILOG_SOURCES = $(PWD)/../hdl/matrix_multiplier.sv

    # Set module parameters
    ifeq ($(SIM),icarus)
        COMPILE_ARGS += -Pmatrix_multiplier.DATA_WIDTH=$(DATA_WIDTH) -Pmatrix_multiplier.A_ROWS=$(A_ROWS) -Pmatrix_multiplier.B_COLUMNS=$(B_COLUMNS) -Pmatrix_multiplier.A_COLUMNS_B_ROWS=$(A_COLUMNS_B_ROWS)
    else ifneq ($(filter $(SIM),questa modelsim riviera activehdl nvc),)
        SIM_ARGS += -gDATA_WIDTH=$(DATA_WIDTH) -gA_ROWS=$(A_ROWS) -gB_COLUMNS=$(B_COLUMNS) -gA_COLUMNS_B_ROWS=$(A_COLUMNS_B_ROWS)
    else ifeq ($(SIM),vcs)
        COMPILE_ARGS += -pvalue+matrix_multiplier/DATA_WIDTH=$(DATA_WIDTH) -pvalue+matrix_multiplier/A_ROWS=$(A_ROWS) -pvalue+matrix_multiplier/B_COLUMNS=$(B_COLUMNS) -pvalue+matrix_multiplier/A_COLUMNS_B_ROWS=$(A_COLUMNS_B_ROWS)
    else ifeq ($(SIM),verilator)
        COMPILE_ARGS += -GDATA_WIDTH=$(DATA_WIDTH) -GA_ROWS=$(A_ROWS) -GB_COLUMNS=$(B_COLUMNS) -GA_COLUMNS_B_ROWS=$(A_COLUMNS_B_ROWS)
    else ifneq ($(filter $(SIM),ius xcelium),)
        EXTRA_ARGS += -defparam "matrix_multiplier.DATA_WIDTH=$(DATA_WIDTH)" -defparam "matrix_multiplier.A_ROWS=$(A_ROWS)" -defparam "matrix_multiplier.B_COLUMNS=$(B_COLUMNS)" -defparam "matrix_multiplier.A_COLUMNS_B_ROWS=$(A_COLUMNS_B_ROWS)"
    endif

    ifneq ($(filter $(SIM),riviera activehdl),)
        COMPILE_ARGS += -sv2k12
    endif

else ifeq ($(TOPLEVEL_LANG),vhdl)
    VHDL_SOURCES = $(PWD)/../hdl/matrix_multiplier_pkg.vhd $(PWD)/../hdl/matrix_multiplier.vhd

    ifneq ($(filter $(SIM),ghdl questa modelsim riviera activehdl nvc),)
        # ghdl, questa, and aldec all use SIM_ARGS with '-g' for setting generics
        SIM_ARGS += -gDATA_WIDTH=$(DATA_WIDTH) -gA_ROWS=$(A_ROWS) -gB_COLUMNS=$(B_COLUMNS) -gA_COLUMNS_B_ROWS=$(A_COLUMNS_B_ROWS)
    else ifneq ($(filter $(SIM),ius xcelium),)
        SIM_ARGS += -generic "matrix_multiplier:DATA_WIDTH=>$(DATA_WIDTH)" -generic "matrix_multiplier:A_ROWS=>$(A_ROWS)" -generic "matrix_multiplier:B_COLUMNS=>$(B_COLUMNS)" -generic "matrix_multiplier:A_COLUMNS_B_ROWS=>$(A_COLUMNS_B_ROWS)"
    endif

    ifeq ($(SIM),ghdl)
        EXTRA_ARGS += --std=08
        SIM_ARGS += --wave=wave.ghw
    else ifeq ($(SIM),nvc)
        EXTRA_ARGS += --std=08
        SIM_ARGS += --wave=wave.fst
    else ifneq ($(filter $(SIM),ius xcelium),)
        COMPILE_ARGS += -v200x
    else ifneq ($(filter $(SIM),questa modelsim riviera activehdl),)
        COMPILE_ARGS += -2008
    endif
else
    $(error A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG))
endif

COCOTB_TOPLEVEL     := matrix_multiplier
COCOTB_TEST_MODULES := copra.integration.autostub,matrix_multiplier_tests

ifeq ($(SIM),ghdl)

all:
	@echo "Skipping since GHDL doesn't support constants effectively"

clean::

else

include $(shell cocotb-config --makefiles)/Makefile.sim

endif

# Profiling

DOT_BINARY ?= dot

test_profile.pstat: sim

callgraph.svg: test_profile.pstat
	$(shell cocotb-config --python-bin) -m gprof2dot -f pstats ./$< | $(DOT_BINARY) -Tsvg -o $@

.PHONY: profile
profile:
	COCOTB_ENABLE_PROFILING=1 $(MAKE) callgraph.svg
