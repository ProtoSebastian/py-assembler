# ******************************************************************************* #
# Copyright (c) 2024 ProtoSebastian                                               #
#                                                                                 #
#  Permission is hereby granted, free of charge, to any person obtaining a copy   #
#  of this software and associated documentation files (the "Software"), to deal  #
#  in the Software without restriction, including without limitation the rights   #
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      #
#  copies of the Software, and to permit persons to whom the Software is          #
#  furnished to do so, subject to the following conditions:                       #
#                                                                                 #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     #
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       #
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    #
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         #
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  #
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  #
#  SOFTWARE.                                                                      #
# ******************************************************************************* #
from assembler import assemble, formatter, bake_constants, load_config, WORD_LENGTH
import sys
from common import *
from math import log2

# Help message
help_mess = """Usage: python main.py <options> -s <ROM size> file...
Options:
  -I --config-file <file>   Set config file. defaults to 'default.config'
  -O --output <file>        Set output file. defaults to 'output.mc'
  -s --rom-size <size>      Set ROM size in words. May be followed by suffixes-
                            for KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB. (the-
                            'iB' is optional. case-insensitive)
                            defaults to config.
  -o --rom-offset <offset>  Set ROM offset in words. This'll offset where the-
                            instructions physically are in the program.
                            defaults to config.
  -p --padding-word <word>  Set what the padding should be. hexadecimal or-
                            binary inputs should be prefixed with '0x' and '0b'-
                            respectively. defaults to config.
  -f --output-format <format>
                            Set the output format, possible formats are:
                            Matt, Raw, Image, Hexdump, Logisim3, Logisim2,-
                            DEBUG. (default is Matt, case-insensitive)
  -M --matt-mode            Enables Matt mode, which disables DB & ORG-
                            directives, and multi-line pseudo-instructions, to-
                            remove jumps in address and make every line-
                            translate to exactly 1 machine code line.
     --dump-instructions    Dump instructions, then exit. (native and pseudo)
     --dump-symbols         Dump symbols defined by the ISA, then exit.
     --dump-labels          Dump labels after assembly.
     --dump-definitions     Dump definitions after assembly.
  -v                        Verbose output. (more v's means higher verbosity,-
                            above level 4 there is no effect)
  -h --help                 Print this message and quit.
  -V --version              Print version and quit.
Notes:
  Parameters for single character options can be separated and unseparated, so:
  "-Ooutput.bin" and "-O output.bin" are both valid."""

# Credits/license message (TODO: Add license from original once it's licensed)
credits_mess = """Credits:
  Author of the base code (none of which remains now) is @MattBatWings at
   GitHub: https://github.com/MattBatWings
   YouTube: https://youtube.com/@MattBatWings

  ISA author is @SLicudis at
   GitHub: https://github.com/SLicudis
   YouTube: https://youtube.com/channel/UCh1aWTr9YdXR--Wv79PErZQ

  Code author is @ProtoSebastian at
   GitHub: https://github.com/ProtoSebastian"""

def print_version():
    print(credits_mess)

    version_string, version_format = render_version(VERSION, VER_FMT)

    print(f"\nVersion format: {version_format}")
    print(f"Version.......: {version_string}")

def print_help():
    print(help_mess)

def handle_unknown_switch(statement: str):
    print_help()
    fatal_error('main', f"Unknown switch statement '{statement}'.")

def interpret_int(input_string: str):
    try:
        return int(input_string, 0)
    except ValueError as _ERR:
        fatal_error('main', f"Could not interpret \'{input_string}\' as an integer.\n{_ERR}")

def main():
    # Fancy switch processing
    config_file = 'default.config' # default to 'default.config'
    input_file  = ''          # no defaults. I mean, why would you default an input file??
    output_file = 'output.mc' # default to 'output.mc'
    ROM_offset  = None
    ROM_size    = None
    padding_word= None
    format_style= 'matt'
    debug_flags = 0
    verbosity   = 0
    input_files = 0

    matt_mode = False

    dbg_input_size = dbg_input_specifier = None
    idx=1
    while(idx < len(sys.argv)):
        # Handle options
        term = sys.argv[idx]
        if(term.startswith('--')):
            match(term):
                # Help
                case '--help':
                    print_help()
                    exit()
                # Version
                case '--version':
                    print_version()
                    exit()
                # Config file
                case '--config-file':
                    idx += 1
                    config_file = sys.argv[idx]
                # Output file
                case '--output':
                    idx += 1
                    output_file = sys.argv[idx]
                # ROM size
                case '--rom-size':
                    idx += 1
                    ROM_size, dbg_input_size, dbg_input_specifier = calculate_size(sys.argv[idx], 'main')
                # ROM offset
                case '--rom-offset':
                    idx += 1
                    ROM_offset = interpret_int(sys.argv[idx])
                # Padding
                case '--padding-word':
                    idx += 1
                    padding_word = interpret_int(sys.argv[idx])
                # Dump instructions
                case '--dump-instructions':
                    debug_flags |= 4
                    ROM_size = 0
                    input_file = 'jomama'
                # Dump symbols
                case '--dump-symbols':
                    debug_flags |= 8
                    ROM_size = 0
                    input_file = 'jomama'
                # Dump labels
                case '--dump-labels':
                    debug_flags |= 1
                # Dump definitions
                case '--dump-definitions':
                    debug_flags |= 2
                # Format
                case '--output-format':
                    idx += 1
                    format_style = sys.argv[idx]
                # Matt mode
                case '--matt-mode':
                    idx += 1
                    matt_mode = True
                # Unknown
                case other:
                    handle_unknown_switch(term)
        elif(term.startswith('-')):
            match(term[:2]):
                # Help
                case '-h':
                    print_help()
                    exit()
                # Version
                case '-V':
                    print_version()
                    exit()
                # Config file
                case '-I':
                    if(len(sys.argv[idx])!=2):
                        config_file=sys.argv[idx][2:]
                    else:
                        idx += 1
                        config_file=sys.argv[idx]
                # Output file
                case '-O':
                    if(len(sys.argv[idx])!=2):
                        output_file=sys.argv[idx][2:]
                    else:
                        idx += 1
                        output_file=sys.argv[idx]
                # ROM size
                case '-s':
                    SIZE_PARAM = ''
                    if(len(sys.argv[idx])!=2):
                        SIZE_PARAM = sys.argv[idx][2:]
                    else:
                        idx += 1
                        SIZE_PARAM = sys.argv[idx]
                    ROM_size, dbg_input_size, dbg_input_specifier = calculate_size(SIZE_PARAM, 'main')
                # ROM offset
                case '-o':
                    PARAM = ''
                    if(len(sys.argv[idx])!=2):
                        PARAM = sys.argv[idx][2:]
                    else:
                        idx += 1
                        PARAM = sys.argv[idx]
                    ROM_offset = interpret_int(PARAM)
                # Padding
                case '-p':
                    PARAM = ''
                    if(len(sys.argv[idx])!=2):
                        PARAM = sys.argv[idx][2:]
                    else:
                        idx += 1
                        PARAM = sys.argv[idx]
                    padding_word = interpret_int(PARAM)
                # Format
                case '-f':
                    PARAM = ''
                    if(len(sys.argv[idx])!=2):
                        PARAM = sys.argv[idx][2:]
                    else:
                        idx += 1
                        PARAM = sys.argv[idx]
                    format_style = PARAM
                # Matt mode
                case '-M':
                    matt_mode = True
                # Verbosity
                case '-v':
                    PARAM = sys.argv[idx][1:]
                    verbosity = PARAM.count('v')
                    if(verbosity != len(PARAM)):
                        fatal_error('main', f"Unknown use of the verbose option \'{sys.argv[idx]}\'")
                # Unknown
                case other:
                    handle_unknown_switch(term[:2])
        else:
            if(input_files!=0):
                # ruh roh
                fatal_error('main', "More than 1 input file specified.")
            input_file=term
            input_files+=1
        idx += 1

    if(input_file==''):
        print_help()
        fatal_error('main', "No input files were specified.")

    # Load config
    load_config_out = load_config(config_file, verbosity)
    # Only write if it hasn't been overriden by parameters
    if(ROM_size == None):
        ROM_size = load_config_out[0][0]
        dbg_input_size = load_config_out[0][1]
        dbg_input_specifier = load_config_out[0][2]
    if(ROM_offset == None):
        ROM_offset = load_config_out[1]
    if(padding_word == None):
        padding_word = load_config_out[2]
    WORD_LENGTH = load_config_out[3]
    print("s %X\no 0x%X\np 0x%X"%(ROM_size, ROM_offset, padding_word))
    # Assemble
    if(ROM_size == None):
        fatal_error('main', "No ROM size specified, cannot continue.\nPlease specify a ROM size as a parameter or in the config file.")
    if(ROM_offset == None):
        fatal_error('main', "No ROM offset specified, cannot continue.\nPlease specify a ROM offset as a parameter or in the config file.")
    if(padding_word == None):
        fatal_error('main', "No padding word specified, cannot continue.\nPlease specify a padding word as a parameter or in the config file.")
    if(verbosity >= 1):
        print(f"main: ROM size is {str(ROM_size)} words", end='')
        if(not dbg_input_specifier.isdecimal()):
            print(f" or {dbg_input_size} {SIZE_PREFIX_FULL[dbg_input_specifier]}words", end='')
        print('.')
        print(f"main: ROM offset is 0x%X"%(ROM_offset))
    if(verbosity >= 1):
        print("main: Padding word is \'0x%0*X\'"%((WORD_LENGTH + 3) >> 2, padding_word))
    exit()
    if(verbosity >= 2):
        print("main: Baking constants..")
    bake_constants(matt_mode)
    machine_code_output = assemble(input_file, ROM_size, ROM_offset, verbosity - 1, debug_flags, matt_mode)
    formatter(machine_code_output, output_file, ROM_size, ROM_offset, padding_word, format_style, verbosity)

    # Success message
    print("main: Assembly successful.")
    # simulate('output.mc')

if __name__ == '__main__':
    main()
