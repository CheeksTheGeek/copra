# Copyright cocotb contributors
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause

TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)

ifeq ($(TOPLEVEL_LANG),verilog)
    VERILOG_SOURCES = $(PWD)/../rtl/cpu.sv
    VERILOG_SOURCES += $(PWD)/../rtl/core.sv
    VERILOG_SOURCES += $(PWD)/../rtl/pipeline_stages.sv
    VERILOG_SOURCES += $(PWD)/../rtl/support_modules.sv
    VERILOG_SOURCES += $(PWD)/../rtl/clock_gen.sv
    # Compile options for SystemVerilog features
    ifeq ($(SIM),icarus)
        COMPILE_ARGS += -g2012
    endif
else
    $(error A valid value (verilog) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG))
endif

COCOTB_TOPLEVEL     := cpu
COCOTB_TEST_MODULES := copra.integration.autostub,test_cpu

# Use uv to run with cocotb 2.0
PYTHON ?= uv run python

export COPRA_STUB_DIR=$(PWD)/../copra_stubs
include $(shell uv run cocotb-config --makefiles)/Makefile.sim 
