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
from common import *

###- CONSTANTS -###
# Comment symbols
COMMENT_SYMBOLS = ['#', ';', '//']
# Operand separators
OPERAND_SEPARATORS = ', \t'
# Space characters for inbetween operands and instruction
INSTRUCTION_SPACING = ' \t'
# Opcode position in first word; how much to shift opcode relative to the first word (in bits, left)
#OPCODE_POSITION = 4
OPCODE_POSITION = None
# Word length in bits
#WORD_LENGTH = 8
WORD_LENGTH = None
# Max length an instruction can have (in words)
#INSTRUCTION_MAX_LENGTH = 4
INSTRUCTION_MAX_LENGTH = None

###- ALL POSSIBLE OPERANDS -###
# Operands
# Format : '<1 char label>':[<position in word>, <word position>, <bit length>, <1: signed, 0: unsigned>, <type flags>, "<full name>"]
# Type flags :
## Bit 0 is allow immediates
## Bit 1 is allow registers
## Bit 2 is allow mem locations
## Bit 3 is reserved for the merge flag
## Bit 4 is reserved for indicating that a mem location parameter is at the beginning of the list
## Bit 5 is reserved for indicating that a mem location parameter is at the end of the list
## Bit 6 is reserved for the "ANY" flag, which overrides type-checking if the type is "immediate" (or no type information)
## For the first word in every line, bits 0-2 all have to be 0, and bits 3-5 represent the type of the line (Label, Definition, ORG, DB, Instruction)
## The rest are up to you
OPERANDS= {
#            'a':[0, 3, 20, 0, 0b0110101, "Full address immediate"], # An address by itself ; [addr]
#            'd':[0, 3, 20, 0, 0b0010101, "Address"],                # An address meant to be next to something else ; [addr, 
#            'D':[4, 1, 4,  0, 0b0000010, "Destination register"],   # Destination register for operations ; %dest
#            'S':[4, 1, 4,  0, 0b0000010, "Source register"],        # Source register for operations ; %src
#            'A':[0, 1, 4,  0, 0b0000010, "Register A"],             # Register A parameter in operations ; %A
#            'B':[4, 2, 4,  0, 0b0000010, "Register B"],             # Register B parameter in operations ; %B
#            'I':[0, 3, 16, 1, 0b0000001, "Immediate"],              # A 2 byte immediate for operations ; imm
#            'F':[4, 1, 4,  0, 0b0000001, "Flag"],                   # The flag in SF/CF ; flag
#            'X':[0, 0, 0,  0, 0xA6,      "Register BX"],            # Detects when register BX is specifically used, accompanies an address to offset it ; %BX]
#            'Y':[0, 1, 4,  0, 0b0010101, "Page"],                   # Immediate used to select the page ; [page,
#            'P':[4, 2, 4,  0, 0b0010110, "Page register"],          # Register used to select the page ; [%page,
#            'O':[0, 1, 4,  0, 0b0100110, "Offset register"],        # Register used to select the offset ; %offset]
          }

###- NATIVE INSTRUCTIONS -###
# Format: '<mnemonic>':[<opcode>, '<operand flags in order of use in opcode>', <opcode specific mask>, <size in user-defined words>]
# [A=0] means operand A is optional and defaults to 0
# - parameter type requirements are derived from operand flag type flags
OPCODES = {
#           'nop' :[[0x0, '',     0x00000000, 4],], # Do nothing club
#
#           'brk' :[[0x1, '',     0x00000000, 4],], # Hey, listen!
#
#           'add' :[[0x2, 'DAB',  0x00000000, 4],   # Arithmetic
#                   [0x3, 'DAI',  0x00000000, 4],],
#           'adc' :[[0x2, 'DAB',  0x01000000, 4],
#                   [0x3, 'DAI',  0x01000000, 4],],
#           'sub' :[[0x2, 'DAB',  0x02000000, 4],
#                   [0x3, 'DAI',  0x02000000, 4],],
#           'sbb' :[[0x2, 'DAB',  0x03000000, 4],
#                   [0x3, 'DAI',  0x03000000, 4],],
#           'and' :[[0x2, 'DAB',  0x04000000, 4],
#                   [0x3, 'DAI',  0x04000000, 4],],
#           'or'  :[[0x2, 'DAB',  0x05000000, 4],
#                   [0x3, 'DAI',  0x05000000, 4],],
#           'xor' :[[0x2, 'DAB',  0x06000000, 4],
#                   [0x3, 'DAI',  0x06000000, 4],],
#           'shr' :[[0x2, 'DA',   0x07000000, 4],],
#           'src' :[[0x2, 'DA',   0x08000000, 4],],
#           'asr' :[[0x2, 'DA',   0x09000000, 4],],
#           'ror' :[[0x2, 'DA',   0x0A000000, 4],],
#           'rol' :[[0x2, 'DA',   0x0B000000, 4],],
#           'neg' :[[0x2, 'DA',   0x0C000000, 4],],
#
#           'str' :[[0x4, 'Sa',   0x00000000, 4],   # Data control
#                   [0x4, 'SdX',  0x01000000, 4],
#                   [0x4, 'SYO',  0x02000000, 4],
#                   [0x4, 'SPO',  0x03000000, 4],],
#           'lod' :[[0x5, 'Da',   0x00000000, 4],
#                   [0x5, 'DdX',  0x01000000, 4],
#                   [0x5, 'DYO',  0x02000000, 4],
#                   [0x5, 'DPO',  0x03000000, 4],],
#           'psh' :[[0x6, 'Sa',   0x00000000, 4],
#                   [0x6, 'SdX',  0x01000000, 4],
#                   [0x6, 'SYO',  0x02000000, 4],
#                   [0x6, 'SPO',  0x03000000, 4],],
#           'pop' :[[0x7, 'Da',   0x00000000, 4],
#                   [0x7, 'DdX',  0x01000000, 4],
#                   [0x7, 'DYO',  0x02000000, 4],
#                   [0x7, 'DPO',  0x03000000, 4],],
#
#           'jmp' :[[0x8, 'a',    0x00000000, 4],   # Branching
#                   [0x8, 'dX',   0x01000000, 4],
#                   [0x8, 'YO',   0x02000000, 4],
#                   [0x8, 'PO',   0x03000000, 4],],
#           'jz'  :[[0x9, 'a',    0x00000000, 4],
#                   [0x9, 'dX',   0x01000000, 4],
#                   [0x9, 'YO',   0x02000000, 4],
#                   [0x9, 'PO',   0x03000000, 4],],
#           'jc'  :[[0x9, 'a',    0x00100000, 4],
#                   [0x9, 'dX',   0x01100000, 4],
#                   [0x9, 'YO',   0x02100000, 4],
#                   [0x9, 'PO',   0x03100000, 4],],
#           'jo'  :[[0x9, 'a',    0x00200000, 4],
#                   [0x9, 'dX',   0x01200000, 4],
#                   [0x9, 'YO',   0x02200000, 4],
#                   [0x9, 'PO',   0x03200000, 4],],
#           'js'  :[[0x9, 'a',    0x00300000, 4],
#                   [0x9, 'dX',   0x01300000, 4],
#                   [0x9, 'YO',   0x02300000, 4],
#                   [0x9, 'PO',   0x03300000, 4],],
#           'jg'  :[[0x9, 'a',    0x00400000, 4],
#                   [0x9, 'dX',   0x01400000, 4],
#                   [0x9, 'YO',   0x02400000, 4],
#                   [0x9, 'PO',   0x03400000, 4],],
#           'jl'  :[[0x9, 'a',    0x00500000, 4],
#                   [0x9, 'dX',   0x01500000, 4],
#                   [0x9, 'YO',   0x02500000, 4],
#                   [0x9, 'PO',   0x03500000, 4],],
#           'jb'  :[[0x9, 'a',    0x00600000, 4],
#                   [0x9, 'dX',   0x01600000, 4],
#                   [0x9, 'YO',   0x02600000, 4],
#                   [0x9, 'PO',   0x03600000, 4],],
#           'ji'  :[[0x9, 'a',    0x00700000, 4],
#                   [0x9, 'dX',   0x01700000, 4],
#                   [0x9, 'YO',   0x02700000, 4],
#                   [0x9, 'PO',   0x03700000, 4],],
#           'jnz' :[[0x9, 'a',    0x00800000, 4],
#                   [0x9, 'dX',   0x01800000, 4],
#                   [0x9, 'YO',   0x02800000, 4],
#                   [0x9, 'PO',   0x03800000, 4],],
#           'jnc' :[[0x9, 'a',    0x00900000, 4],
#                   [0x9, 'dX',   0x01900000, 4],
#                   [0x9, 'YO',   0x02900000, 4],
#                   [0x9, 'PO',   0x03900000, 4],],
#           'jno' :[[0x9, 'a',    0x00A00000, 4],
#                   [0x9, 'dX',   0x01A00000, 4],
#                   [0x9, 'YO',   0x02A00000, 4],
#                   [0x9, 'PO',   0x03A00000, 4],],
#           'jns' :[[0x9, 'a',    0x00B00000, 4],
#                   [0x9, 'dX',   0x01B00000, 4],
#                   [0x9, 'YO',   0x02B00000, 4],
#                   [0x9, 'PO',   0x03B00000, 4],],
#           'jle' :[[0x9, 'a',    0x00C00000, 4],
#                   [0x9, 'dX',   0x01C00000, 4],
#                   [0x9, 'YO',   0x02C00000, 4],
#                   [0x9, 'PO',   0x03C00000, 4],],
#           'jge' :[[0x9, 'a',    0x00D00000, 4],
#                   [0x9, 'dX',   0x01D00000, 4],
#                   [0x9, 'YO',   0x02D00000, 4],
#                   [0x9, 'PO',   0x03D00000, 4],],
#           'jnb' :[[0x9, 'a',    0x00E00000, 4],
#                   [0x9, 'dX',   0x01E00000, 4],
#                   [0x9, 'YO',   0x02E00000, 4],
#                   [0x9, 'PO',   0x03E00000, 4],],
#           'jni' :[[0x9, 'a',    0x00F00000, 4],
#                   [0x9, 'dX',   0x01F00000, 4],
#                   [0x9, 'YO',   0x02F00000, 4],
#                   [0x9, 'PO',   0x03F00000, 4],],
#           'cal' :[[0xA, 'a',    0x00000000, 4],
#                   [0xA, 'dX',   0x01000000, 4],
#                   [0xA, 'YO',   0x02000000, 4],
#                   [0xA, 'PO',   0x03000000, 4],],
#           'ret' :[[0xB, '',     0x00000000, 4],],
#           'rti' :[[0xE, '',     0x00000000, 4],],
#
#           'sf'  :[[0xC, 'F',    0x00000000, 4],], # Data control
#           'cf'  :[[0xD, 'F',    0x00000000, 4],],
          } # Opcodes

###- PSEUDO-INSTRUCTIONS -###
# Pseudo-instructions
# Format : 'label':['<resolution as formatted string>', '<operand flags in order>']
# - instructions must be separated by newlines ('\n')
# - parameter type requirements are derived from operand flag type flags
PSEUDO_INSTRUCTIONS = {
#           'mvi' :[['add %{0}, %ZX, {1}',   'DI'],],
#           'mov' :[['add %{0}, %ZX, %{1}',  'DA'],],
#           'cmp' :[['sub %ZX, %{0}, %{1}',  'AB'],
#                   ['sub %ZX, %{0}, {1}',   'AI'],],
#           'inc' :[['add %{0}, %{0}, 1',    'D' ],],
#           'dec' :[['sub %{0}, %{0}, 1',    'D' ],],
#           'shl' :[['add %{0}, %{1}, %{1}', 'DA'],],
         }
###- STARTING SYMBOLS -###
# Dictionary that the assembler starts with
# [<resolution value>, <custom type flags>]
# - in most situations custom type flags aren't needed, unless you need custom behavior with the type system.
STARTING_SYMBOLS = {
#                    'zx' :[0,  0,], 'ax' :[1,  0,], 'bx' :[2,  0x80,], 'cx' :[3,  0,], # Registers
#                    'dx' :[4,  0,], 'ex' :[5,  0,], 'fx' :[6,  0,   ], 'sx' :[7,  0,],
#                    'sy' :[8,  0,], 'al' :[9,  0,], 'bl' :[10, 0,   ], 'cl' :[11, 0,],
#                    'dl' :[12, 0,], 'el' :[13, 0,], 'fl' :[14, 0,   ], 'sl' :[15, 0,],
#                    'reset_vector':[0xFFFF4, 0,], 'interrupt_vector':[0xFFFF8, 0,], 'nmi_vector':[0xFFFFC, 0,], # vectors
                   }

###- UTILITY -###
# Define check
def is_define(word: str):
    if(len(word) == 0):
        return 0
    return word == 'define'
# Label check
def is_label(word: str):
    if(type(word) == int):
        return 0
    if(len(word) == 0):
        return 0
    return (word[0] == '.') | ((word[-1] == ':') << 1)
# Symbol check
def is_symbol(word: list, symbols: dict):
    if(type(word[0]) == int):
        return False
    if(len(word[0]) == 0):
        return False
    return (word[0].lower() in symbols)
# Definition check
def is_definition(word: list, symbols: dict):
    if(type(word[0]) == int):
        return False
    if(len(word[0]) == 0):
        return False
    return (word[0] in symbols)
# Merge offset parameters
def merge_offset_parameters(line: list, is_resolved: bool = False):
    idx = 1
    params = line[0]
    while(idx != len(params)):
        A = params[idx - 1]
        B = params[idx]
        if(B[1] & 0x8):
            if(not ((A[1] & 0x1) and (B[1] & 0x1))):
                fatal_error('assembler', f"merge_offset_parameters: on line {line[1]}, cannot merge \'{display_type(A, True)}\' and \'{display_type(B, True)}\'")
            if((type(A[0]) == int) and (type(B[0]) == int)):
                A[0] = A[0] + B[0]
            elif(is_resolved):
                fatal_error('assembler', f"merge_offset_parameters: line {line[1]} has unresolved parameters, couldn\'t merge.\n{rec_dump_array(line, 1)}\n{recompose_line(line)}")
            else:
                A[0] = f"{display_word([A[0], A[1] & (~0x30)])}, {display_word([B[0], B[1] & (~0x30)])}"
            A[1] |= B[1] & 0x30
            line[0].pop(idx)
            continue
        idx += 1
# Merge offset parameters, but output as a copy and only with the types
def merge_offset_types(line:list) -> list:
    line_copy = deep_copy(line)
    merge_offset_parameters(line_copy, False)
    params = []

    for param in line_copy[0]:
        params.append(param[1])

    return params
# Pseudo-instruction check
def is_pseudo(line: list):
    if(len(line[0]) == 0):
        fatal_error('assembler', f"is_pseudo: line {line[1]} is empty..? it should\'ve been filtered out by the assembler..\n{rec_dump_array(line, 1)}\n{resolve_line(line)}")
    label = line[0][0][0]
    if(label in PSEUDO_INSTRUCTIONS):
        variations = PSEUDO_INSTRUCTIONS[label]
        merged_param_types = merge_offset_types(line)[1:]

        variant = -1
        for variant_index in range(len(variations)):
            if(variant > -1):
                break
            variation = variations[variant_index]
            # Number of operands check
            if(len(merged_param_types) != variation[0]):
                continue
            # Operand type check
            offset = 0
            for idx in range(len(merged_param_types)):
                type_flags = variation[2][idx - offset]
                # override check
                if((merged_param_types[idx] & 1) and (type_flags & 0o100)):
                    continue
                type_flags &= (~0o100)
                if((merged_param_types[idx] & type_flags) != type_flags):
                    break
            else:
                variant = variant_index
        # Might be a native-instruction with the same label
        if((variant == -1) and (label in OPCODES)):
            return (False, variant)
        # Is a pseudo-instruction, but types might not match
        return (True, variant)
    # Is not a pseudo-instruction
    return (False, -1)
# Instruction check
def is_instruction(line: list):
    if(len(line[0]) == 0):
        fatal_error('assembler', f"is_instruction: line {line[1]} is empty..? it should\'ve been filtered out by the assembler..\n{rec_dump_array(line, 1)}\n{resolve_line(line)}")
    label = line[0][0][0]
    if(label in OPCODES):
        variations = OPCODES[label]
        merged_param_types = merge_offset_types(line)[1:]

        variant = -1
        for idx in range(len(variations)):
            if(variant > -1):
                break
            variation = variations[idx]
            # Number of operands check
            if((len(merged_param_types) < variation[1][1]) or (len(merged_param_types) > variation[1][2])):
                continue
            # Operand type check
            for idx2 in range(len(merged_param_types)):
                type_flags = variation[1][0][idx2][0][4]
                # override check
                if((merged_param_types[idx2] & 1) and (type_flags & 0o100)):
                    continue
                type_flags &= (~0o100)
                if((merged_param_types[idx2] & type_flags) != type_flags):
                    break
            else:
                variant = idx
        return (True, variant)
    return (False, -1)
# Turn label as it appears in code into how it'll be used in instructions ('Done:' -> '.Done')
def to_label(word: list, filename: str, line: int, caller: str):
    if(len(word[0]) == 0):
        return 0
    result = is_label(word[0])
    if(result != 0):
        if(result == 1):
            return word
        elif(result == 2):
            return ['.' + word[0][:-1], word[1]]
        elif(result == 3):
            return [word[0][:-1], word[1]]
    else:
        fatal_error('assembler', f"{caller}: {filename}:{line}: Could not interpret label \'{word}\' ({display_type(word, True)})")
# Convert label from many syntaxes into 1 syntax
def convert_label(word: list):
    result = is_label(word[0])
    if(result != 0):
        if(result == 1):
            return [word[0][1:] + ':', word[1]]
        elif(result == 2):
            return word
        elif(result == 3):
            return [word[0][1:], word[1]]
    else:
        fatal_error('assembler debug', f"convert_label: Could not interpret label \'{word[0]}\' ({display_type(word, True)})")
# Helper function for displaying the type of a word
def display_type(word: list, a_or_an: bool = False):
    if(word[1] & 0b111):
        sentence = " ".join(["immediate"]*(word[1] & 1) + ["register"]*((word[1] >> 1) & 1))
    elif(word[1] & (~0b111)):
        t = (word[1] >> 3) & 0b111
        sentence = ["no type", "label", "definition", "ORG directive", "DB directive", "instruction"][t]
    else:
        sentence = "no type"
    if(a_or_an):
        if(sentence[0].lower() in "aeiou"):
            return "an " + sentence
        return "a " + sentence
    return sentence
# Helper function for displaying the types of an entire line
def display_types_line(line: list, cleaned_input: bool = False):
    if(cleaned_input):
        return f"{line[0].upper()} {', '.join(display_word([display_type([0, x[0] & (~0b100)]), x[0]], x[1] if(len(x) > 1) else None) for x in line[1:])}"
    else:
        return f"{display_word(line[0][0])} {', '.join(display_word([display_type([0, x[1] & (~0b100)]), x[1]]) for x in line[0][1:])}"
# Helper function for displaying the word based off of its flags
def display_word(word: list, optional_substitute: int = None):
    disp_word = str(word[0])
    if(optional_substitute != None):
        # word=default
        disp_word = disp_word + '=' + str(optional_substitute)
    if(word[1] & 0b111):
        # [+%*word+]
        if(word[1] & 0o100):
            # * = any
            disp_word = '*' + disp_word
        if(word[1] & 0b010):
            disp_word = '%' + disp_word
        if(word[1] & 0b1000):
            # merge
            disp_word = '+' + disp_word
        if(word[1] & 0b010000):
            disp_word = '[' + disp_word
        if(word[1] & (~0x7F)):
            # + after = special behavior
            disp_word = disp_word + '+'
        if(word[1] & 0b100000):
            disp_word = disp_word + ']'
    elif((word[1] & 0x38) != 0):
        # WORD
        return disp_word.upper()
    else:
        # word+
        if(word[1] & (~0x7F)):
            # + after = special behavior
            disp_word = disp_word + '+'
    return disp_word
# Resolve integers, ignores everything else
def resolve_integer(word: list, filename: str, line: int, caller: str):
    # Return unmodified if is an int, or empty
    if((type(word[0]) == int) or (len(word[0]) == 0)):
        return word
    # Auto-detect format
    if(word[0][0] in '-0123456789'):
        try:
            offset = 0
            if(word[0][0] == '-'):
                offset = 1
            if(word[0][offset:offset + 2] == '0x'):
                return [int(word[0][:offset] + word[0][offset + 2:], 16), word[1]]
            elif(word[0][offset:offset + 2] == '0o'):
                return [int(word[0][:offset] + word[0][offset + 2:], 8), word[1]]
            elif(word[0][offset:offset + 2] == '0b'):
                return [int(word[0][:offset] + word[0][offset + 2:], 2), word[1]]
            else:
                return [int(word[0], 10), word[1]]
        except ValueError as _ERR:
            fatal_error('assembler', f"{caller}: {filename}:{line}: Could not resolve number \'{word[0]}\' which is {display_type(word, True)}\n{_ERR}")
    # $ prefixed hexadecimal
    elif(word[0][0] == '$'):
        try:
            return [int(word[0][1:], 16), word[1]]
        except ValueError as _ERR:
            fatal_error('assembler', f"{caller}: {filename}:{line}: Could not resolve hexadecimal \'{word[0]}\' which is {display_type(word, True)}\n{_ERR}")
    # Return unmodified if not an integer
    return word
# Handle character constant
def char_constant(string: str, idx: int, filename: str, line: int, caller: str, resolve_strings: bool = True, default_flags: int = 0b001):
    idx_end = strfind_escape(string, '\'', idx + 1)
    if(idx_end == -1):
        fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Missing terminating \' character.\n{string}\n{' ' * idx}^{'~' * (len(string) - idx - 1)}")
    idx_end += 1
    if(not resolve_strings):
        return (idx, idx_end, [[string[idx:idx_end], default_flags]])
    try:
        evaluated = eval(string[idx:idx_end])
    except Exception as _ERR:
        fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Could not evaluate character constant.\n{string}\n{' ' * idx}^{'~' * (idx_end - idx - 1)}\n{_ERR}")
    if(len(evaluated) > 1):
        fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Too many characters in character constant.\n{string}\n{' ' * idx}^{'~' * (idx_end - idx - 1)}")
    elif(len(evaluated) == 0):
        fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Empty character constant.\n{string}\n{' ' * idx}^~")
    return (idx, idx_end, [[ord(evaluated) & ((1 << WORD_LENGTH) - 1), default_flags]])
# Handle string constant
def string_constant(string: str, idx: int, filename: str, line: int, caller: str, resolve_strings: bool = True, default_flags: int = 0b001):
    idx_end = strfind_escape(string, '\"', idx + 1)
    if(idx_end == -1):
        fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Missing terminating \" character.\n{string}\n{' ' * idx}^{'~' * (len(string) - idx - 1)}")
    idx_end += 1
    if(not resolve_strings):
        return (idx, idx_end, [[string[idx:idx_end], default_flags]])
    try:
        evaluated = eval(string[idx:idx_end])
    except Exception as _ERR:
        fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Could not evaluate string constant.\n{string}\n{' ' * idx}^{'~' * (idx_end - idx - 1)}\n{_ERR}")
    if(len(evaluated) == 0):
        fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Empty string constant.\n{string}\n{' ' * idx}^~")
    return (idx, idx_end, [[(ord(char) & ((1 << WORD_LENGTH) - 1)), default_flags] for char in evaluated])
# Decompose instruction params (+ character literals with both ' and ")
def decompose_instruction_params(string: str, filename: str, line: int, caller: str, resolve_strings: bool = True, default_flags: int = 0b001):
    idx = 0
    output = []
    while(idx < len(string)):
        flags = default_flags
        idx = inverted_strfind(string, OPERAND_SEPARATORS, idx)
        if(idx == -1):
            break
        if(string[idx] == '['):
            idx += 1
            idx_end = strfind_escape(string, ']', idx)
            if(idx_end == -1):
                fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Missing closing bracket for memory location type indicator.\n{string}\n{' ' * (idx - 1)}^{'~' * (len(string) - idx)}")
            params = decompose_instruction_params(string[idx:idx_end].strip(), filename, line, caller + " handling memloc:", resolve_strings, default_flags | 0b100)
            if(len(params) == 0):
                fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Empty memory location type indicator.\n{string}\n{' ' * (idx - 1)}^{'~' * (idx_end - idx + 1)}")
            params[0][1]  |= 0b010000
            params[-1][1] |= 0b100000
            output = output + params
            idx_end += 1
        else:
            if(string[idx] == '+'): # Parameter that should be merged
                idx += 1
                # If only a '+', add it to the output instead
                try:
                    if(string[idx] in OPERAND_SEPARATORS):
                        output.append(['+', flags])
                        idx_end = idx
                        continue
                except IndexError:
                    output.append(['+', flags])
                    break
                # Check if not the first parameter
                if(len(output) > 0):
                    # Add merge flag
                    flags = flags | 0b1000
            if(string[idx] == '%'): # Register type
                idx += 1
                # If only a '%', add it to the output instead
                try:
                    if(string[idx] in OPERAND_SEPARATORS):
                        output.append(['%', flags])
                        idx_end = idx
                        continue
                except IndexError:
                    output.append(['%', flags])
                    break
                flags = (flags & (~0b001)) | 0b010 # Swap immediate flag for register flag
            if(string[idx] == '\''): # Character literal
                idx, idx_end, constant = char_constant(string, idx, filename, line, caller, resolve_strings, flags)
                output = output + constant
            elif(string[idx] == '\"'): # Character literal (alias)
                idx, idx_end, constants = string_constant(string, idx, filename, line, caller, resolve_strings, flags)
                if(len(constants) != 1):
                    fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: There must be exactly 1 character in string constant. (for instruction operands)\n{string}\n{' ' * idx}^{'~' * (idx_end - idx - 1)}")
                output = output + constants
            else: # Don't know (label or definition)
                idx_end = strfind(string, OPERAND_SEPARATORS, idx)
                if(idx_end == -1):
                    output.append([string[idx:], flags])
                    break
                output.append([string[idx:idx_end], flags])
        idx = idx_end
    if(resolve_strings):
        return [resolve_integer(x, filename, line, caller) for x in output]
    return output
# Decompose DB params (+ character literals + string constants)
def decompose_DB_params(string: str, filename: str, line: int, caller: str, resolve_strings: bool = True, default_flags: int = 0b001):
    idx = 0
    output = []
    while(idx < len(string)):
        flags = default_flags
        idx = inverted_strfind(string, OPERAND_SEPARATORS, idx)
        if(idx == -1):
            break
        if(string[idx] == '\''): # Character literal
            idx, idx_end, constant = char_constant(string, idx, filename, line, caller, resolve_strings, flags)
            output = output + constant
        elif(string[idx] == '\"'): # String constant (specific for DB)
            idx, idx_end, constants = string_constant(string, idx, filename, line, caller, resolve_strings, flags)
            output = output + constants
        else: # Don't know (label or definition)
            idx_end = strfind(string, OPERAND_SEPARATORS, idx)
            if(idx_end == -1):
                output.append([string[idx:], flags])
                break
            output.append([string[idx:idx_end], flags])
        idx = idx_end
    if(resolve_strings):
        return [resolve_integer(x, filename, line, caller) for x in output]
    return output
# Parse line
def parse_line(line: list, filename: str, caller: str, resolve_strings: bool = True):
    decomposed_lines = []
    decomposed_definitions = []
    split_A = 0
    split_B = 0
    instruction = ''
    # Labels and finding instruction
    while(is_label(instruction) or (split_A == 0)):
        split_B = strfind(line[0], INSTRUCTION_SPACING, split_A)
        if(split_B == -1):
            instruction = line[0][split_A:]
        else:
            instruction = line[0][split_A:split_B]
        if(is_label(instruction)):
            decomposed_lines.append([[[instruction, 0o10]], line[1]])
        if(split_B == -1):
            break
        split_A = inverted_strfind(line[0], INSTRUCTION_SPACING, split_B)
    if(split_B != -1):
        parameters  = line[0][split_A:]
    else:
        parameters = ""
    if(is_label(instruction)):
        return decomposed_lines, decomposed_definitions
    instruction = instruction.lower()
    # Definition
    if(is_define(instruction)):
        decomposed_definitions.append([[[instruction, 0o20]] + decompose_instruction_params(parameters, filename, line[1], caller, resolve_strings), line[1]])
    # ORG
    elif(instruction == 'org'):
        decomposed_lines.append([[[instruction, 0o30]] + decompose_instruction_params(parameters, filename, line[1], caller, resolve_strings), line[1]])
    # DB
    elif(instruction == 'db'):
        decomposed_lines.append([[[instruction, 0o40]] + decompose_DB_params(parameters, filename, line[1], caller, resolve_strings), line[1]])
    # Assume it's an instruction
    else:
        decomposed_lines.append([[[instruction, 0o50]] + decompose_instruction_params(parameters, filename, line[1], caller, resolve_strings), line[1]])
    return (decomposed_lines, decomposed_definitions)
# Recompose line
def recompose_line(line: list):
    first_word = line[0][0]

    # Label
    if(first_word[1] == 0o10):
        return convert_label(first_word)[0]
    # Everything else
    else:
        return display_word(first_word) + (' '*(len(line[0]) > 1)) + ', '.join(display_word(x) for x in line[0][1:])
# Display multiple lines of Assembly
def print_assembly(lines: list, last_was: dict, line_width: int):
    last_line = 0
    special_case = False
    for line in lines:
        if(last_line == line[1]):
            print("%s: "%(' ' * line_width), end='')
        else:
            print("%0*d: "%(line_width, line[1]), end='')
        # Check if instruction
#        if((line[0][0][0] not in ['org', 'db', 'define']) and (is_label(line[0][0][0]) == 0)):
        if(line[0][0][1] == 0o50):
            print("  ", end='')
        print(recompose_line(line), end='')
        # Display instruction variation
        if((line[0][0][1] == 0o50) and (len(line[0][0]) > 2)):
            print(" ; variation %d"%(line[0][0][2]), end='')
        # I don't even know
        if(((line[1] in last_was) and (last_line != line[1])) or special_case):
            # Check if label
#            if(is_label(line[0][0][0]) != 0):
            if(line[0][0][1] == 0o10):
                special_case = True
            else:
                print(" ; resolved from ; %s"%(recompose_line(last_was[line[1]])), end='')
                special_case = False
        last_line = line[1]
        print()
# Display multiple lines of Assembly with machine code positions
def print_assembly_wordpos(lines: list, last_was: dict, line_width: int, hex_width: int):
    last_line = 0
    special_case = False
    for line in lines:
        if(last_line == line[1]):
            print("%s:%0*X: "%(' ' * line_width, hex_width, line[2]), end='')
        else:
            print("%0*d:%0*X: "%(line_width, line[1], hex_width, line[2]), end='')
        # Check if instruction
#        if((line[0][0][0] not in ['org', 'db', 'define']) and (is_label(line[0][0][0]) == 0)):
        if(line[0][0][1] == 0o50):
            print("  ", end='')
        print(recompose_line(line), end='')
        if((line[0][0][1] == 0o50) and (len(line[0][0]) > 2)):
            print(" ; variation %d"%(line[0][0][2]), end='')
        # I don't even know
        if(((line[1] in last_was) and (last_line != line[1])) or special_case):
            # Check if label
#            if(is_label(line[0][0][0]) != 0):
            if(line[0][0][1] == 0o10):
                special_case = True
            else:
                print(" ; resolved from ; %s"%(recompose_line(last_was[line[1]])), end='')
                special_case = False
        # Check if ORG directive
#        elif(line[0][0][0] == 'org'):
        elif(line[0][0][1] == 0o30):
            print(" ; jump to 0x%0*X"%(hex_width, line[2]), end='')
        last_line = line[1]
        print()
# Strip line of comments
def remove_comment(comment_symbols: list, line: str):
    idx = [line.find(symbol) for symbol in comment_symbols]
    idx = [x for x in idx if(x != -1)]
    if(len(idx) == 0):
        return line
    return line[:min(idx)]
# Bake a cake!
def bake_constants(matt_mode):
    # Calculate number of operands and add to macro element
    pop_keys = [pop for pop in PSEUDO_INSTRUCTIONS]
    for pop in pop_keys:
        popinfo=PSEUDO_INSTRUCTIONS[pop]
        for idx in range(len(popinfo)):
            popinfo[idx].insert(0, len(popinfo[idx][1]))
            # Deal with multi-line pseudo-instructions in Matt mode later on

            # Make requirement list
            requirements = []
            for c in popinfo[idx][2]:
                requirements.append(OPERANDS[c][4])
            popinfo[idx][2] = requirements

    # Check operands
    for operand in OPERANDS:
        if(OPERANDS[operand][1] >= INSTRUCTION_MAX_LENGTH):
            fatal_error('assembler', f"baking stage: wtf: Operand \'{OPERANDS[operand][5]}\' defined in a word outside set maximum length, are you sure it\'s correct?")
        if(OPERANDS[operand][0] >= WORD_LENGTH):
            fatal_error('assembler', f"baking stage: wtf: Operand \'{OPERANDS[operand][5]}\' shift amount is bigger than a word, are you sure it\'s correct?")
        if((((OPERANDS[operand][1] + 1) * WORD_LENGTH) - OPERANDS[operand][0] - OPERANDS[operand][2]) < 0):
            fatal_error('assembler', f"baking stage: wtf: Operand \'{OPERANDS[operand][5]}\' is defined outside the instruction, are you sure it\'s correct?")

    # Make instructions more machine-friendly and check instruction lengths
    for opcode in OPCODES:
        variations = OPCODES[opcode]
        for variation_index in range(len(variations)):
            variation = variations[variation_index]
            # Error and prompt user if instruction's length exceeds max length
            if((variation[3] * WORD_LENGTH) > (INSTRUCTION_MAX_LENGTH * WORD_LENGTH)):
                fatal_error('assembler', f"baking stage: wtf: Instruction \'{opcode.upper()}\' variation {variation_index} exceeds set maximum length, are you sure it\'s correct?")

            processed_opcode=[]
            operands=variation[1]

            idx=0
            minimum_operands=0
            while(idx<len(operands)):
                # Process optional operand
                if(operands[idx]=='['):
                    idx_end=operands.find(']', idx)
                    if(idx_end==-1):
                        fatal_error('assembler', f"baking stage: syntax error: No closing brace for operand \'{operands[idx+1]}\' in instruction \'{opcode.upper()}\' variation {variation_index}.")
                    substr=operands[idx+1:idx_end]
                    if(substr[2:]==''):
                        fatal_error('assembler', f"baking stage: wtf: No default defined for operand \'{substr[0]}\' for instruction \'{opcode.upper()}\' variation {variation_index}.")
                    processed_opcode.append([OPERANDS[substr[0]], int(substr[2:])])
                    idx=idx_end+1
                    minimum_operands-=1
                # Process sequence of mandatory operands
                else:
                    idx_end=operands.find('[', idx)
                    if(idx_end==-1):
                        idx_end += len(operands) + 1
                    substr=operands[idx:idx_end]
                    processed_opcode = processed_opcode + [[OPERANDS[x]] for x in substr]
                    idx=idx_end

            # Check operands used in instruction; make sure operands don't go outside the instruction
            for index in range(len(processed_opcode)):
                operand = processed_opcode[index][0]
                if(operand[1] >= variation[3]):
                    fatal_error('assembler', f"baking stage: wtf: Operand \'{operand[5]}\' in instruction \'{opcode.upper()}\' variation {variation_index} is defined in a word outside the instruction\'s length, are you sure it\'s correct?")

            maximum_operands=len(processed_opcode)
            minimum_operands=minimum_operands+maximum_operands
            processed_opcode=[processed_opcode, minimum_operands, maximum_operands]
            variation[1]=processed_opcode

    # Validity check
    for opcode in OPCODES:
        variations = OPCODES[opcode]
        for variation_index in range(len(variations)):
            variation = variations[variation_index]
            operands=variation[1][0]
            maxim=1
            for idx, operand in enumerate(operands):
                if(maxim <= len(operand)):
                    maxim=len(operand)
                else:
                    fatal_error('assembler', f"baking stage: wtf: Optional operand \'{operands[idx-1][0][5]}\' declared inbetween mandatory ones in instruction \'{opcode.upper()}\' variation {variation_index}! (Will cause problems later)")
# Decompose instruction params (+ character literals with both ' and ")
def decompose_config_params(string: str, filename: str, line: int, caller: str):
    idx = 0
    output = []
    while(idx < len(string)):
        idx = inverted_strfind(string, OPERAND_SEPARATORS, idx)
        if(idx == -1):
            break
        if(string[idx] == '['):
            idx += 1
            idx_end = strfind_escape(string, ']', idx)
            if(idx_end == -1):
                fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Missing closing bracket.\n{string}\n{' ' * (idx - 1)}^{'~' * (len(string) - idx)}")
            params = decompose_config_params(string[idx:idx_end].strip(), filename, line, caller + " handling list:")
            if(len(params) == 0):
                fatal_error('assembler', f"{caller}: {filename}:{line}:{idx + 1}: Empty list.\n{string}\n{' ' * (idx - 1)}^{'~' * (idx_end - idx + 1)}")
            output.append(params)
            idx_end += 1
        else:
            if(string[idx] == '\"'): # String
                idx, idx_end, constants = string_constant(string, idx, filename, line, caller, False, 0)
                output.append(constants[0][0])
            else: # Normal
                idx_end = strfind(string, OPERAND_SEPARATORS, idx)
                if(idx_end == -1):
                    output.append(string[idx:])
                    break
                output.append(string[idx:idx_end])
        idx = idx_end
    return output
# returns ROM size then ROM offset then padding word
def load_config(config_filename: str, verbose_level: int):
    ROM_size = dbg_input_size = dbg_input_specifier = ROM_offset = padding_word = None
    if(verbose_level >= 1):
        print(f"load_config: Reading from \'{config_filename}\'")
    try:
        config_file = open(config_filename, 'r')
    except FileNotFoundError as _ERR:
        fatal_error('assembler', f"load_config: {config_filename}: File not found.\n{_ERR}")
    lines = [line.strip() for line in config_file]
    config_file.close()

    # Remove comments and blanklines, and add line number
    lines = [[remove_comment(COMMENT_SYMBOLS, line).strip(), idx+1] for idx, line in enumerate(lines)]

    # Remove empty lines & add line numbers
    lines = [line for line in lines if(len(line[0]) != 0)]

    # Decompose and process
    fields = ['options', 'operands', 'instructions', 'macros', 'symbols']
    mode = 0
    line_index = 0
    while(line_index < len(lines)):
        line = lines[line_index]
        line_number = line[1]
        if(line[0][0] == '['): # Field
            new_field = line[0][1:line[0].find(']')].strip().lower()
            mode = fields.index(new_field)
            print("New field \'%s\', mode %d"%(new_field, mode))
            line_index += 1
            continue
        idx = strfind(line[0], ' ')
        idx2 = inverted_strfind(line[0], ' ', idx)
        first_word = []
        if(idx != -1):
            first_word.append(line[0][0:idx])
        else:
            first_word.append(line[0])
        if((mode == 1) and (first_word[0] != 'opcode')):
            idx = inverted_strfind(line[0], ' ', idx)
            idx2 = strfind(line[0], ' ', idx)
            first_word.append(line[0][idx:idx2])
        params = []
        if(idx2 != -1):
            params = decompose_config_params(line[0][idx2:], config_filename, line_number, 'load_config')

        if(mode == 1):
            params[0] += params[0][1].split(':')
            params[0].pop(1)

        print(' '.join(first_word) + ' ' + ', '.join(str(param) for param in params))

        if(mode == 0):
            match(first_word[0].lower()):
                case 'word_size':
                    WORD_LENGTH = int(params[0], 0)
                case 'instruction_max_length':
                    INSTRUCTION_MAX_LENGTH = int(params[0], 0)
                case 'rom_size':
                    ROM_size, dbg_input_size, dbg_input_specifier = calculate_size(params[0], 'load_config')
                case 'rom_offset':
                    ROM_offset = int(params[0], 0)
                case 'padding_word':
                    padding_word = int(params[0], 0)
                case other:
                    fatal_error('assembler', f"load_config: {config_filename}:{line_number}: [{fields[mode]}]: Unknown option \'{first_word[0]}\'")
        # TODO: the rest lol

        line_index += 1
    return ([ROM_size, dbg_input_size, dbg_input_specifier], ROM_offset, padding_word, WORD_LENGTH)

###- MAIN THING -###
# Assemble function
def assemble(assembly_filename: str, ROM_size: int, ROM_offset: int, verbose_level: int, debug_flags: int, matt_mode: bool):
    if(debug_flags & 0b1100):
        if(debug_flags & 0x8):
            print("ISA-defined symbols:")
            for symbol in STARTING_SYMBOLS:
                symbolinfo = STARTING_SYMBOLS[symbol]
                print('- \'%s\' = %d (%s)'%(symbol, symbolinfo[0], display_word([display_type([symbolinfo[0], symbolinfo[1] & (~0b100)]), symbolinfo[1]])))
        if(debug_flags & 0x4):
            total = 0
            print("Native-instructions: (%d)"%(len(OPCODES)))
            for opcode in OPCODES:
                variations=OPCODES[opcode]
                print(f"{opcode}: ({len(variations)})")
                for variation_index in range(len(variations)):
                    variation = variations[variation_index]
                    params = [display_word([display_type([0, x[0][4] & (~0b100)]), x[0][4]], x[1] if(len(x) != 1) else None) for x in variation[1][0]]

                    print(f'- {variation_index}: ' + opcode.upper() + ' ' + ', '.join(params))
                    total += 1
            print("(Total: %d)"%(total))
            total = 0
            print("\nPseudo-instructions: (%d)"%(len(PSEUDO_INSTRUCTIONS)))
            for label in PSEUDO_INSTRUCTIONS:
                variations=PSEUDO_INSTRUCTIONS[label]
                print(f"{label}: ({len(variations)})")
                for variation_index in range(len(variations)):
                    variation = variations[variation_index]
                    params = [display_word([display_type([0, x & (~0b100)]), x], None) for x in variation[2]]

                    print(f'- {variation_index}: ' + label.upper() + ' ' + ', '.join(params) + ' -> ' + variation[1])
                    total += 1
            print("(Total: %d)"%(total))
        exit()

    try:
        assembly_file = open(assembly_filename, 'r')
    except FileNotFoundError as _ERR:
        fatal_error('assembler', f"{assembly_filename}: File not found.\n{_ERR}")
    if(verbose_level >= 0):
        print(f"assembler: Reading from \'{assembly_filename}\'")
        if(matt_mode):
            # Matt mode engaged.
            print(f"assembler: Matt mode active. ORG, DB, & multi-line pseudo-instructions are disabled.")
    lines = [line.strip() for line in assembly_file]
    assembly_file.close()

    # DEBUG: ROM address size constant
    ROM_address_size = int(log2(ROM_size) + 3) >> 2
    line_address_size = int(log(len(lines), 10) + 1)
    word_display_size = int(WORD_LENGTH + 3) >> 2
    if(verbose_level >= 2):
        print("Address hex width: %d (%s)"%(ROM_address_size, ''.join(hex(x%16).upper()[2] for x in range(ROM_address_size))))
        print("Line address width: %d (%s)"%(line_address_size, ''.join(chr(0x30 + (x%10)) for x in range(line_address_size))))
        print("Word display width: %d (%s)"%(word_display_size, ''.join(hex(x%16).upper()[2] for x in range(word_display_size))))

    # Remove comments and blanklines, and add line number
    lines = [[remove_comment(COMMENT_SYMBOLS, line).strip(), idx+1] for idx, line in enumerate(lines)]

    # Remove empty lines & add line numbers
    lines = [line for line in lines if(len(line[0]) != 0)]

    if(len(lines) == 0):
        fatal_error('assembler', f"{assembly_filename}: File empty.")

    # Populatesymbol table
    symbols = STARTING_SYMBOLS
    # Definitions table
    definitions = {}
    # Labels table
    labels = {}

    # Decompose instructions and separate labels
    # DEBUG: show current job
    if(verbose_level >= 1):
        print("\nPARSING LINES..")
    decomposed = []
    decomposed_definitions = []
    original_lines = {}
    for line in lines:
        new_lines, new_definitions = parse_line(line, assembly_filename, 'parser')
        decomposed = decomposed + new_lines
        decomposed_definitions = decomposed_definitions + new_definitions
        new_lines, new_definitions = parse_line(line, assembly_filename, 'parser', False)
        original_lines[line[1]] = new_lines + new_definitions

    # DEBUG: display Assembly right now
    if(verbose_level >= 3):
        print("ASSEMBLY:")
        print_assembly(decomposed, {}, line_address_size)

    # DEBUG: display definitions
    if(verbose_level >= 3):
        print("\nDEFINITIONS:")
        print_assembly(decomposed_definitions, {}, line_address_size)

    # Resolve symbols
    # DEBUG: show current job
    if(verbose_level >= 1):
        print("\nRESOLVING DEFINITIONS.. (ISA-DEFINED)")
    for index in range(len(decomposed)):
        line = decomposed[index]
        line_number = line[1]
        params = line[0]

        line_before_change = deep_copy(line)
        changed = False
        for index2 in range(1, len(params)):
            param = params[index2]
            if(is_symbol(param, symbols)):
                changed = True
                symbolinfo = symbols[param[0].lower()]
                params[index2] = [symbolinfo[0], param[1] | symbolinfo[1]]

        # DEBUG: show resolved line
        if(verbose_level >= 2):
            if(changed):
                print("%0*d: %s -> %s"%(line_address_size, line_number, recompose_line(line_before_change), recompose_line(line)))

    # DEBUG: display Assembly right now
    if(verbose_level >= 3):
        print("ASSEMBLY:")
        print_assembly(decomposed, {}, line_address_size)

    # Memorize definitions (and resolve their parameters if needed)
    # DEBUG: show current job
    if(verbose_level >= 1):
        print("\nMEMORIZING USER-DEFINED DEFINITIONS, PRE-LABELS..")
    # Q: "why not tasks = decomposed_definitions?"
    # A: "because I only want a list of pointers to the lines so I don't modify the original"
    tasks = [x for x in decomposed_definitions]

    if((verbose_level >= 1) and (len(tasks) == 0)):
       print("Nothing to do.")

    # Parameter check
    for definition in tasks:
        merged_types = merge_offset_types(definition)
        # Once, there were 4 little definitions
        if(len(merged_types) > 3): # One had too many parameters
            fatal_error('assembler', f"definition parameter check: {assembly_filename}:{definition[1]}: Too many parameters for definition.")
        elif(len(merged_types) == 2): # One had only a name
            fatal_error('assembler', f"definition parameter check: {assembly_filename}:{definition[1]}: Only name given for definition.")
        elif(len(merged_types) == 1): # One had no parameters
            fatal_error('assembler', f"definition parameter check: {assembly_filename}:{definition[1]}: No parameters given for definition.")
        # But one was juuust right

    # Memorize or resolve
    while(len(tasks) != 0):
        progress = False
        idx = 0
        while(idx < len(tasks)):
            definition = tasks[idx]

            # Check if resolved
            if((len(definition[0]) == 3) and (type(definition[0][2][0]) == int)):
                progress = True
                definitions[definition[0][1][0]] = definition[0][2][0]
                if(verbose_level >= 2):
                    print(f"%0*d: \'%s\' = %d"%(line_address_size, definition[1], definition[0][1][0], definition[0][2][0]))
                tasks.pop(idx)
                continue
            # Otherwise, try to resolve operands
            else:
                fully_resolved = True

                line_before_change = deep_copy(definition)
                changed = False
                for idx2 in range(2, len(definition[0])):
                    if(is_definition(definition[0][idx2], definitions)):
                        progress = True
                        changed = True
                        definition[0][idx2][0] = definitions[definition[0][idx2][0]]
                    if(type(definition[0][idx2][0]) != int):
                        fully_resolved = False

                if(changed and (verbose_level >= 2)):
                    print('%0*d: %s -> %s ; resolution'%(line_address_size, definition[1], recompose_line(line_before_change), recompose_line(definition)))
                if(fully_resolved):
                    line_before_change = deep_copy(definition)
                    merge_offset_parameters(definition, True)
                    if((definition != line_before_change) and (verbose_level >= 2)):
                        print('%0*d: %s -> %s ; merge'%(line_address_size, definition[1], recompose_line(line_before_change), recompose_line(definition)))
            idx += 1
        if(not progress):
            if(len(tasks) != 0):
                if(verbose_level >= 2):
                    print("definition resolver (pre-labels): Couldn\'t resolve everything, likely only labels left, leaving the rest for after labels.")
            break
        if(verbose_level >= 2):
            print("  > Loop <")

    # Resolve definitions
    # DEBUG: show current job
    if(verbose_level >= 1):
        print("\nRESOLVING USER-DEFINED DEFINITIONS, PRE-LABELS..")
    for index in range(len(decomposed)):
        line = decomposed[index]
        line_number = line[1]

        line_before_change = deep_copy(line)
        changed = False
        all_resolved = True
        for index2 in range(1, len(line[0])):
            if(is_definition(line[0][index2], definitions)):
                changed = True
                line[0][index2][0] = definitions[line[0][index2][0]]
            if(type(line[0][index2][0]) != int):
                all_resolved = False
        # DEBUG: show resolved line
        if(verbose_level >= 2):
            if(changed):
                print("%0*d: %s -> %s ; resolution"%(line_address_size, line_number, recompose_line(line_before_change), recompose_line(line)))
        if(all_resolved):
            line_before_change = deep_copy(line)
            merge_offset_parameters(line, True)
            if((verbose_level >= 2) and (line_before_change != line)):
                print("%0*d: %s -> %s ; merge"%(line_address_size, line_number, recompose_line(line_before_change), recompose_line(line)))

    # DEBUG: display Assembly after resolving definitions
    if(verbose_level >= 3):
        print("\nASSEMBLY NOW:")
        print_assembly(decomposed, {}, line_address_size)

    # Resolve pseudo-instructions
    # DEBUG: show current job
    if(verbose_level >= 1):
        print("\nRESOLVING PSEUDO-INSTRUCTIONS..")
    last_was = {}
    cont=True
    while(cont):
        cont=False
        index = 0

        while(index < len(decomposed)):
            line = decomposed[index]
            line_number=line[1]
            words=line[0]
            res = is_pseudo(line)

            # label exists
            if(res[0]):
                label = words[0][0]
                # a variant exists
                if(res[1] != -1):
                    merge_offset_parameters(line)
                    variant_index = res[1]
                    if(line_number not in last_was):
                        last_was[line_number] = original_lines[line[1]][-1]
                    cont=True
                    popinfo=PSEUDO_INSTRUCTIONS[label][variant_index]

                    gen_lines = popinfo[1].format(*[x[0] for x in words[1:]]).split('\n')

                    parsed = []
                    for gline in gen_lines:
                        new_lines, new_definitions = parse_line([gline, line_number], assembly_filename, 'pseudo-instruction resolver')

                        for line in new_lines:
                            line_number = line[1]
                            params = line[0]
                            for index2 in range(1, len(params)):
                                param = params[index2]
                                if(is_symbol(param, symbols)):
                                    symbolinfo = symbols[param[0].lower()]
                                    params[index2] = [symbolinfo[0], param[1] | symbolinfo[1]]

                        parsed = parsed + new_lines

                    # DEBUG: display resolved line
                    if(verbose_level >= 2):
                        print('%0*d: %s -> %s ; variation %d'%(line_address_size, line_number, recompose_line(line), '\\n'.join(recompose_line(gline) for gline in parsed), res[1]))
                    decomposed = decomposed[:index] + parsed + decomposed[index + 1:]
                # no variant found
                else:
                    fatal_error('assembler', f"pseudo-instruction resolver: {assembly_filename}:{line_number}: No pseudo-instruction variation for \'{label.upper()}\' matches\n  {display_types_line(line)}\nVariations:\n  {'\n  '.join(display_types_line([label] + [[y] for y in x[2]], True) for x in PSEUDO_INSTRUCTIONS[label])}")
            else:
                index += 1

    # DEBUG: display Assembly after resolving pseudo-instructions
    if(verbose_level >= 3):
        print("\nASSEMBLY NOW:")
        print_assembly(decomposed, last_was, line_address_size)

    # Find variants of instructions and find bad instructions
    # DEBUG: show current job
    if(verbose_level >= 1):
        print("\nRESOLVING INSTRUCTION TYPES..")

    for index in range(len(decomposed)):
        line = decomposed[index]
        line_number = line[1]
        # Check if instruction type
        if(line[0][0][1] == 0o50):
            res = is_instruction(line)
            # label exists
            if(res[0]):
                label = line[0][0][0]
                # a variant exists
                if(res[1] != -1):
                    line[0][0].append(res[1])
                    if(verbose_level >= 2):
                        print("%*d: %s -> \'%s\' variation %d"%(line_address_size, line_number, recompose_line(line), label.upper(), res[1]))
                # no variant found
                else:
                    fatal_error('assembler', f"instruction type resolver: {assembly_filename}:{line_number}: No native-instruction variation for \'{label.upper()}\' matches\n  {display_types_line(line)}\nVariations:\n  {'\n  '.join(display_types_line([label] + [[y[0][4], y[1] if(len(y) > 1) else None] for y in x[1][0]], True) for x in OPCODES[label])}")
            # fuck
            else:
                fatal_error('assembler', f"instruction type resolver: {assembly_filename}:{line_number}: No native-instruction with the mnemonic \'{line[0][0][0].upper()}\' known.\n" + "%0*d:   %s ; %s"%(line_address_size, line[1], recompose_line(original_lines[line[1]][-1]), display_types_line(line)))
    # New format: [[['<label>', type, variant], ['<param>', type], ...], <line number>]
    # (the variant is appended to the label)

    # DEBUG: display Assembly after resolving native-instruction types
    if(verbose_level >= 3):
        print("\nASSEMBLY NOW:")
        print_assembly(decomposed, last_was, line_address_size)

    # Calculate positions of lines in the machine code file, using the user-defined instruction lengths
    # Resolves & removes ORG directives too
    # DEBUG: show current job
    if(verbose_level >= 1):
        print("\nCALCULATING POSITIONS IN MACHINE CODE..")
    position = 0 # Default is position 0
    for index in range(len(decomposed)):
        line = decomposed[index]
        words = line[0]
        line_number = line[1]
        # DEBUG: display current line
        if(verbose_level >= 2):
            spacing = ' ' * line_address_size
            print("%0*d: %s"%(line_address_size, line_number, recompose_line(line)))

        # Handle ORG directive
        if(words[0][1] == 0o30):
            # Error on ORG directive if in Matt mode
            if(matt_mode):
                fatal_error('assembler', f"position resolver: {assembly_filename}:{line_number}: Encountered ORG directive, but they are disabled in Matt mode.")
            if(len(words) == 1):
                fatal_error('assembler', f"position resolver: {assembly_filename}:{line_number}: No parameters given for ORG directive.")
            elif(len(words) > 2):
                fatal_error('assembler', f"position resolver: {assembly_filename}:{line_number}: Too many parameters given for ORG directive.")
            if(type(words[1][0]) != int):
                fatal_error('assembler', f"position resolver: {assembly_filename}:{line_number}: ORG parameter wasn\'t resolved. remember labels cannot be used here, and definitions that are based off of labels are resolved later down the line.")
            position = words[1][0]
            # DEBUG: show position jump
            if(verbose_level >= 2):
                print("%s: Encountered ORG directive, changing position to 0x%0*X"%(spacing, ROM_address_size, position))

        # Check if position is in ROM bounds
        if(position >= ROM_size):
            fatal_error('assembler', f"position resolver: {assembly_filename}:{line_number}: Position {'0x%X'%position} is out of bounds of the ROM. (ROM size = {ROM_size})")
        elif(position < 0):
            fatal_error('assembler', f"position resolver: {assembly_filename}:{line_number}: Position went negative ({'0x%X'%position}). What the fuck are you doing?")

        # Add current position to line
        decomposed[index].append(position)
        # DEBUG: show what position current line is in the machine code
        if(verbose_level >= 2):
            print("%s: is at 0x%0*X"%(spacing, ROM_address_size, position))

        # Handle known instruction
        if(words[0][1] == 0o50):
            position += OPCODES[words[0][0]][words[0][2]][3]
            # DEBUG: show how many words 'position' is incremented by
            if(verbose_level >= 2):
                print("%s: This \'%s\' is a known instruction (variation %d), and is %d words.\n%s: Incrementing position by %d words."%(spacing, words[0][0].upper(), words[0][2], OPCODES[words[0][0]][words[0][2]][3], spacing, OPCODES[words[0][0]][words[0][2]][3]))
        # Handle DB directive
        elif(words[0][1] == 0o40):
            # Error on DB directive if in Matt mode
            if(matt_mode):
                fatal_error('assembler', f"position resolver: {assembly_filename}:{line_number}: Encountered DB directive, but they are disabled in Matt mode.")
            if(len(words) == 1):
                fatal_error('assembler', f"position resolver: {assembly_filename}:{line_number}: No parameters given for DB directive.")
            position += len(words) - 1
            # DEBUG: show how many words 'position' is incremented by
            if(verbose_level >= 2):
                print("%s: Encountered DB directive, that defines %d words.\n%s: Incrementing position by %d words."%(spacing, len(words) - 1, spacing, len(words) - 1))

    # DEBUG: show assembly after calculating positions
    if(verbose_level >= 3):
        print("\nASSEMBLY NOW:")
        print_assembly_wordpos(decomposed, last_was, line_address_size, ROM_address_size)

    # Memorize labels
    # DEBUG: show current job
    if(verbose_level >= 1):
        print("\nMEMORIZING LABELS..")
    for index in range(len(decomposed)):
        line = decomposed[index]
        words = line[0]
        line_number = line[1]
        line_word_pos = line[2]

        # if label
        if(words[0][1] == 0o10):
            label = to_label(words[0], assembly_filename, line_number, 'label resolver')
            labels[label[0]] = line_word_pos
            # DEBUG: show what position label is at
            if(verbose_level >= 2):
                print("%0*d: \'%s\' (\'%s\') is at 0x%0*X"%(line_address_size, line[1], label[0], words[0][0], ROM_address_size, line_word_pos))

    # DEBUG: show label table
    if(verbose_level >= 3):
        print("\nLABEL TABLE:")
        print(dump_dict(labels))

    # Resolve labels
    # DEBUG: show current job
    if(verbose_level >= 1):
        print("\nRESOLVING LABELS..")
    for index in range(len(decomposed)):
        line = decomposed[index]
        line_number = line[1]
        params = line[0]

        line_before_change = deep_copy(line)
        changed = False
        all_resolved = True
        for index2 in range(1, len(params)):
            if(type(params[index2][0]) == int):
                continue
            if(is_label(params[index2][0]) == 1):
                changed = True
                index = -1
                if('[' in params[index2][0]):
                    start = params[index2][0].find('[')
                    end   = params[index2][0].find(']')
                    if(end == -1):
                        fatal_error('assembler', f"label resolver: {assembly_filename}:{line_number}: Unterminated label index.\n{params[index2][0]}\n{' '*start}^{'~'*(len(params[index2][0]) - start - 1)}")
                    try:
                        index = int(params[index2][0][start+1:end])
                    except ValueError:
                        fatal_error('assembler', f"label resolver: {assembly_filename}:{line_number}: Label index couldn\'t be resolved.\n{params[index2][0]}\n{' '*(start + 1)}^{'~'*(end - start - 2)}")
                    params[index2][0] = params[index2][0][:start]
                try:
                    if(index != -1):
                        params[index2][0] = (labels[params[index2][0]] >> (WORD_LENGTH * index)) & ((1 << WORD_LENGTH) - 1)
                    else:
                        params[index2][0] = labels[params[index2][0]]
                except KeyError as _ERR:
                    fatal_error('assembler', f"label resolver: {assembly_filename}:{line_number}: Couldn\'t resolve label \'{params[index2][0]}\'\nLabel table dump:\n{dump_dict(labels)}")
            if(type(params[index2][0]) != int):
                all_resolved = False
        # DEBUG: show resolved line
        if(verbose_level >= 2):
            if(changed):
                print("%0*d:%0*X: %s -> %s ; resolution"%(line_address_size, line_number, ROM_address_size, line[2], recompose_line(line_before_change), recompose_line(line)))
        if(all_resolved):
            line_before_change = deep_copy(line)
            merge_offset_parameters(line, True)
            if((verbose_level >= 2) and (line != line_before_change)):
                print("%0*d:%0*X: %s -> %s ; merge"%(line_address_size, line_number, ROM_address_size, line[2], recompose_line(line_before_change), recompose_line(line)))

    # DEBUG: display Assembly after resolving labels
    if(verbose_level >= 3):
        print("\nASSEMBLY NOW:")
        print_assembly_wordpos(decomposed, last_was, line_address_size, ROM_address_size)

    # Memorize definitions (and resolve their parameters if needed)
    # DEBUG: show current job
    do_job = len(tasks) != 0
    if((verbose_level >= 1) and (tasks != 0)):
        print("\nMEMORIZING USER-DEFINED DEFINITIONS, POST-LABELS..")
        if(not do_job):
            print("Nothing left, skipping.")

    # Memorize or resolve
    while(len(tasks) != 0):
        progress = False
        idx = 0
        while(idx < len(tasks)):
            definition = tasks[idx]

            # Check if resolved
            if((len(definition[0]) == 3) and (type(definition[0][2][0]) == int)):
                progress = True
                definitions[definition[0][1][0]] = definition[0][2][0]
                if(verbose_level >= 2):
                    print(f"%0*d: \'%s\' = %d"%(line_address_size, definition[1], definition[0][1][0], definition[0][2][0]))
                tasks.pop(idx)
                continue
            # Otherwise, try to resolve operands
            else:
                fully_resolved = True

                line_before_change = deep_copy(definition)
                changed = False
                for idx2 in range(2, len(definition[0])):
                    if(type(definition[0][idx2][0]) == int):
                        continue
                    if(is_definition(definition[0][idx2], definitions)):
                        progress = True
                        changed = True
                        definition[0][idx2][0] = definitions[definition[0][idx2][0]]
                    if(is_label(definition[0][idx2][0]) == 1):
                        progress = True
                        changed = True
                        definition[0][idx2][0] = labels[definition[0][idx2][0]]
                    if(type(definition[0][idx2][0]) != int):
                        fully_resolved = False
                if(changed and (verbose_level >= 2)):
                    print('%0*d: %s -> %s ; resolution'%(line_address_size, definition[1], recompose_line(line_before_change), recompose_line(definition)))
                if(fully_resolved):
                    line_before_change = deep_copy(definition)
                    merge_offset_parameters(definition, True)
                    if((definition != line_before_change) and (verbose_level >= 2)):
                        print('%0*d: %s -> %s ; merge'%(line_address_size, definition[1], recompose_line(line_before_change), recompose_line(definition)))
            idx += 1
        if(not progress):
            if(len(tasks) != 0):
                fatal_error('assembler', f"definition resolver (post-labels): Couldn\'t resolve everything in definitions.")
            break
        if(verbose_level >= 2):
            print("  > Loop <")

    # Resolve definitions
    # DEBUG: show current job
    if(verbose_level >= 1):
        print("\nRESOLVING USER-DEFINED DEFINITIONS, POST-LABELS..")

    for index in range(len(decomposed)):
        line = decomposed[index]
        line_number = line[1]

        line_before_change = deep_copy(line)
        changed = False
        for index2 in range(1, len(line[0])):
            if(is_definition(line[0][index2], definitions)):
                changed = True
                line[0][index2][0] = definitions[line[0][index2][0]]
            if(type(line[0][index2][0]) != int):
                fatal_error('assembler', f"definition resolver (post-labels, final): {assembly_filename}:{line_number}: Couldn\'t resolve \'{line[0][index2][0]}\'")
        # DEBUG: show resolved line
        if(verbose_level >= 2):
            if(changed):
                print("%0*d: %s -> %s ; resolution"%(line_address_size, line_number, recompose_line(line_before_change), recompose_line(line)))
        line_before_change = deep_copy(line)
        merge_offset_parameters(line, True)
        if((verbose_level >= 2) and (line_before_change != line)):
            print("%0*d: %s -> %s ; merge"%(line_address_size, line_number, recompose_line(line_before_change), recompose_line(line)))

    # DEBUG: display Assembly after resolving definitions
    if(verbose_level >= 3):
        print("\nASSEMBLY NOW:")
        print_assembly_wordpos(decomposed, last_was, line_address_size, ROM_address_size)

    # Lines should be clean by now

    # Assembly stage
    # DEBUG: show current job
    if(verbose_level >= 1):
        print("\nSTARTING ASSEMBLY..")
    output_machine_code = []
    last_line = -1
    for i in range(len(decomposed)):
        # Decompose instruction
        line=decomposed[i]
        words=line[0]
        line_number=line[1]

        machine_code = 0
        current_instruction = words[0][0]
        current_type = words[0][1]
        words = words[1:]
        
        # Begin machine code translation
        # handle DB directive
        if(current_type == 0o40):
            if(verbose_level >= 2):
                print("%0*d:%0*X: %s"%(line_address_size, line_number, ROM_address_size, line[2], recompose_line(line)), end='')
                offset_display_size = max(int(log2(len(words)) + 3) >> 2, ROM_address_size - 1)
                head = 0
                while(head < len(words)):
                    if((head % 16) == 0):
                        print("\n%s:+%0*X: "%(' '*line_address_size, offset_display_size, head), end='')
                    print("%0*X "%(word_display_size, words[head][0]), end='')
                    head += 1
                    if(((head % 8) == 0) or (head >= len(words))):
                        print(' ', end='')
                    if(((head % 16) == 0) or (head >= len(words))):
                       print("%s|%-16s|"%(' '*((word_display_size + 1) * (15 - ((head - 1) % 16))), ''.join((chr(words[idx][0]) if(chr(words[idx][0]).isprintable()) else '.') for idx in range(head - ((head - 1) % 16) - 1, head))), end='')
                print()

            output_machine_code.append([sum(words[len(words) - index - 1][0] << (index * WORD_LENGTH) for index in range(len(words))), line_number, line[2], len(words), original_lines[line_number][-1]])
        # handle instructions
        elif(current_type == 0o50):
            variant = line[0][0][2]
            # Resolve mnemonic
            try:
                current_opinfo = OPCODES[current_instruction][variant]
            except KeyError as _ERR:
                fatal_error('assembler', f"assembly stage: {assembly_filename}:{line_number}: Unknown instruction mnemonic \'{current_instruction}\'\n{_ERR}")
            current_size = current_opinfo[3]

            if(verbose_level >= 2):
                if(line_number != last_line):
                    print("%0*d:%0*X: %s"%(line_address_size, line_number, ROM_address_size, line[2], recompose_line(line)))
                else:
                    print("%s:%0*X: %s"%(' '*line_address_size, ROM_address_size, line[2], recompose_line(line)))

            # Assemble opcode
            machine_code |= current_opinfo[0] << (OPCODE_POSITION + ((current_opinfo[3] - 1) * WORD_LENGTH))

            # Number of operands check
            # Should be good without it?
#            if(  current_opinfo[1][-2] > len(words)):
#                fatal_error('assembler', f"assembly stage: {assembly_filename}:{line_number}: Not enough operands for instruction \'{current_instruction}\' variation {variant}")
#            elif(current_opinfo[1][-1] < len(words)):
#                fatal_error('assembler', f"assembly stage: {assembly_filename}:{line_number}: Too many operands for instruction \'{current_instruction}\' variation {variant}")

            # Check operands and assemble them
            for idx, opcode in enumerate(current_opinfo[1][0]):
                if(len(words) <= idx):
                    words.append([opcode[1], opcode[0][4]])
                opinfo = opcode[0]

                # Check if bit width is 0
                if(opinfo[2] == 0):
                    # Skip assembling operand
                    continue

                mask   = (1 << opinfo[2]) - 1
                sign   = 1
                if(words[idx][0] < 0):
                    sign = -1
                if((not opinfo[3]) and (sign < 0)):
                    fatal_error('assembler', f"assembly stage: {assembly_filename}:{line_number}: {opinfo[5]} for instruction \'{current_instruction}\' variant {variant} is signed, but the operand doesn\'t support that.")
                unsignedver = words[idx][0] * sign
                if(unsignedver != (unsignedver & mask)):
                    fatal_error('assembler', f"assembly stage: {assembly_filename}:{line_number}: {opinfo[5]} for instruction \'{current_instruction}\' variant {variant} doesn\'t fit, it\'s too big. (bit width: {opinfo[2]})")

                machine_code |= (words[idx][0] & mask) << (opinfo[0] + ((current_opinfo[3] - opinfo[1] - 1) * WORD_LENGTH))
                # Just to be safe, it's ANDed with the mask

            # OR with opcode-specific mask
            machine_code |= current_opinfo[2]

            # Length check
            if((int(log2(machine_code if(machine_code != 0) else 1)) + 1) > (current_opinfo[3] * WORD_LENGTH)):
                fatal_error('assembler', f"assembly stage: {assembly_filename}:{line_number}: Uh-oh! the instruction at this line ended up bigger than expected, this should be investigated.. You should open an issue about this!\n" +
                "Relevant info:\n" +
                "  Version format: {1}\n  Version.......: {0}\n".format(*render_version(VERSION, VER_FMT)) +
                f"  {assembly_filename}:{line_number}: {lines[i][0]}\n" +
                "%*0d:%*0X: %s \n"%(line_address_size, line_number, ROM_address_size, line[2], recompose_line(line)) +
                f"{words}\n" +
                f"{current_opinfo}\n")

            # Output
            # Format is: [<INSTRUCTION>, <LINE IN ASSEMBLY FILE>, <POSITION IN WORDS>, <SIZE IN WORDS>, [<ORIGINAL OPERANDS>]]
            if(last_line != line_number):
                output_machine_code.append([machine_code, line_number, line[2], current_size, original_lines[line_number][-1]])
            else:
                output_machine_code.append([machine_code, line_number, line[2], current_size])
            if(verbose_level >= 2):
                print("%*s: %s"%(line_address_size + ROM_address_size + 1, '+', " ".join("%0*X"%(word_display_size, x) for x in word_dissect(machine_code, current_size, WORD_LENGTH))))
            last_line = line_number

    if(verbose_level >= 1):
        print("\nSORTING OUTPUT BY POSITION IN MACHINE CODE..")
    output_machine_code.sort(key = lambda x:x[2])

    # DEBUG: print machine code and their origins
    if(verbose_level >= 2):
        print("OUTPUT:\n%s\nDISAMBIGUATION:"%(dump_array(output_machine_code)))
        word_size = (WORD_LENGTH + 3) >> 2
        for machine_code in output_machine_code:
            print('%0*d:%0*X: %s'%(line_address_size, machine_code[1], ROM_address_size, machine_code[2], " ".join("%0*X"%(word_size, x) for x in word_dissect(machine_code[0], machine_code[3], WORD_LENGTH))), end='')
            if(len(machine_code) >= 5):
                print(' ; %s'%(recompose_line(machine_code[4])), end='')
            print()
    if(debug_flags & 1):
        print(f'Label table dump:\n{dump_dict(labels)}')
    if(debug_flags & 2):
        print(f'Definition table dump:\n{dump_dict(definitions)}')

    return output_machine_code

# Formats output of the assembler
def formatter(assembler_output: list, output_file: str, rom_size: int, rom_offset: int, padding_word: int, format_style: str, verbose_level: int):
    format_style = format_style.lower()
    ROM_address_size = int(log2(rom_size) + 3) >> 2
    word_size = (WORD_LENGTH + 3) >> 2
    if(format_style in ['raw', 'image']):
        output = open(output_file, 'wb')
    else:
        output = open(output_file, 'w')

    if(verbose_level >= 1):
        print(f"formatter: Outputting to \'{output_file}\'")
        print("formatter: Outputting as", end='')

    # Matt's assembler format
    ## Outputs binary as ASCII
    ## Output is as big as it needs to be
    ## Empty space is filled with provided padding_word
    if(format_style == 'matt'):
        if(verbose_level >= 1):
            print(" Matt\'s format.")
        head = 0
        for instruction in assembler_output:
            position = instruction[2]
            size = instruction[3]
            word = instruction[0]
            if(head != position):
                for _ in range(position - head):
                    output.write(bin(padding_word)[2:].zfill(WORD_LENGTH) + '\n')
                head = position
            output.write(bin(word)[2:].zfill(WORD_LENGTH * size) + '\n')
            head += size
    # Raw format
    ## Just raw binary, not human friendly
    ## Output is as big as it needs to be if raw format
    ## Output is fattened to be (rom_size * bytes_per_word) bytes with provided padding_word if image format
    ## Empty space is filled with provided padding_word
    elif(format_style in ['raw', 'image']):
        if(verbose_level >= 1):
            if(format_style == 'raw'):
                print(" raw format.")
            else:
                print(" ROM image format.")
        head = 0
        bytes_per_word = (WORD_LENGTH + 7) >> 3
        padding = bytes(word_dissect(padding_word, bytes_per_word, 8))

        if(format_style == 'image'):
            assembler_output.append([padding_word, -1, rom_size - 1, 1])

        for instruction in assembler_output:
            position = instruction[2]
            size = instruction[3]
            word = bytes(word_dissect(instruction[0], size * bytes_per_word, 8))
            if(head != position):
                for _ in range(position - head):
                    output.write(padding)
                head = position
            output.write(word)
            head += size
    # Hexdump formats
    ## Better human readability
    ## Output is fattened to be rom_size words (* Dependent on variation)
    ## Empty space is filled with provided padding_word (* Dependent on variation)
    ## Output is squeezed when a repeating line is detected to save space. (* Dependent on variation)
    elif(format_style[:7] == 'hexdump'):
        head = 0
        first_word = True
        # Disables squeezing
        no_squeeze = 'ns' in format_style
        # Disables squeezing for instructions
        squeeze_only_pad = 'sp' in format_style
        # Disables padding
        no_pad = 'np' in format_style
        # Disables fattening
        no_fat = ('nf' in format_style) or no_pad
        last_word = 0
        repeating = False
        address_length = int(log2(rom_size) + 3) >> 2

        if(verbose_level >= 1):
            print(" hexdump format", end='')

            if(no_squeeze):
                print(", without squeezing", end='')
            if(squeeze_only_pad):
                print(", squeezing only padding/fat", end='')
            if(no_pad):
                print(", without padding", end='')
            if(no_fat):
                print(", without file fattening", end='')
            print('.')

        if(not no_fat):
            assembler_output.append([padding_word, -1, rom_size - 1, 1])

        for instruction in assembler_output:
            position = instruction[2]
            size = instruction[3]
            word = instruction[0]
            if(head != position):
                for _ in range(position - head):
                    if(no_pad):
                        head = position
                        break
                    # if word isn't repeating, write
                    if((last_word != padding_word) or first_word or no_squeeze):
                        repeating = False
                        output.write('%0*X: %0*X\n'%(ROM_address_size, head, word_size, padding_word))
                        last_word = padding_word
                    # squeeze if haven't squeezed already
                    elif(not repeating):
                        output.write('*\n')
                        repeating = True
                        head = position
                        break
                    head += 1
            # if word isn't repeating, write
            if((last_word != word) or first_word or no_squeeze or squeeze_only_pad):
                repeating = False
                output.write('%0*X: %s\n'%(ROM_address_size, head, " ".join("%0*X"%(word_size, x) for x in word_dissect(word, size, WORD_LENGTH))))
                last_word = word
            # squeeze if haven't squeezed already
            elif(not repeating):
                output.write('*\n')
                repeating = True
            head += size
            first_word = False
        if(repeating):
            output.write('%0*X:\n'%(ROM_address_size, head))
    # Logisim3 format
    elif(format_style[:8] == 'logisim3'):
        current_line = [0] * 16
        last_line = [-1] * 16
        current_line_index = 0
        head = 0
        index = 0
        repeating = False
        do_squeeze = ('ys' in format_style[8:])
        no_fat = ('nf' in format_style[8:])
        if(verbose_level >= 1):
            print(" logisim v3.0 format", end='')
            if(do_squeeze):
                print(", with squeezing", end='')
            if(no_fat):
                print(", with no file fattening", end='')
            print('.')
        if(not no_fat):
            assembler_output.append([padding_word, -1, rom_size - 1, 1])
        output.write("v3.0 hex words addressed\n")
        while(index != len(assembler_output)):
            current = assembler_output[index]
            size = current[3]
            words = word_dissect(current[0], size, WORD_LENGTH)
            position = current[2]
            while((head + current_line_index) != position):
                if(current_line_index == 16):
                    if((current_line != last_line) or (not do_squeeze)):
                        output.write('%0*X: %s\n'%(ROM_address_size, head, " ".join("%0*X"%(word_size, x) for x in current_line)))
                        last_line = current_line.copy()
                        repeating = False
                    elif(not repeating):
                        output.write('*\n')
                        repeating = True
                    current_line_index = 0
                    head += 16
                current_line[current_line_index] = padding_word
                current_line_index += 1
            for word in words:
                if(current_line_index == 16):
                    if((current_line != last_line) or (not do_squeeze)):
                        output.write('%0*X: %s\n'%(ROM_address_size, head, " ".join("%0*X"%(word_size, x) for x in current_line)))
                        last_line = current_line.copy()
                        repeating = False
                    elif(not repeating):
                        output.write('*\n')
                        repeating = True
                    current_line_index = 0
                    head += 16
                current_line[current_line_index] = word
                current_line_index += 1
            index += 1
        if(current_line_index != 0):
            output.write('%0*X: %s\n'%(ROM_address_size, head, " ".join("%0*X"%(word_size, current_line[x]) for x in range(current_line_index))))
    # Logisim2 RLE format
    elif(format_style == 'logisim2'):
        index = 0
        head  = 0
        line_index   = 0
        current_word = -1
        repetition   = 0
        if(verbose_level >= 1):
            print(" logisim v2.0 RLE format.")
        output.write("v2.0 raw\n")
        while(index != len(assembler_output)):
            current = assembler_output[index]
            size = current[3]
            words = word_dissect(current[0], size, WORD_LENGTH)
            position = current[2]
            while(head != position):
                if(current_word == -1):
                    current_word = padding_word
                    head += 1
                    continue
                if(current_word == padding_word):
                    repetition += 1
                else:
                    if(repetition >= 3):
                        if(line_index == 8):
                            output.write('\n')
                            line_index = 0
                        if(line_index == 7):
                            output.write('%d*%X'%(repetition + 1, current_word))
                        else:
                            output.write('%d*%X '%(repetition + 1, current_word))
                        line_index += 1
                    else:
                        for _ in range(repetition + 1):
                            if(line_index == 8):
                                output.write('\n')
                                line_index = 0
                            if(line_index == 7):
                                output.write('%X'%(current_word))
                            else:
                                output.write('%X '%(current_word))
                            line_index += 1
                    repetition = 0
                    current_word = padding_word
                head += 1
            for word in words:
                if(current_word == -1):
                    current_word = word
                    head += 1
                    continue
                if(current_word == word):
                    repetition += 1
                else:
                    if(repetition >= 3):
                        if(line_index == 8):
                            output.write('\n')
                            line_index = 0
                        if(line_index == 7):
                            output.write('%d*%X'%(repetition + 1, current_word))
                        else:
                            output.write('%d*%X '%(repetition + 1, current_word))
                        line_index += 1
                    else:
                        for _ in range(repetition + 1):
                            if(line_index == 8):
                                output.write('\n')
                                line_index = 0
                            if(line_index == 7):
                                output.write('%X'%(current_word))
                            else:
                                output.write('%X '%(current_word))
                            line_index += 1
                    repetition = 0
                    current_word = word
                head += 1
            index += 1
        if(repetition >= 3):
            if(line_index == 8):
                output.write('\n')
                line_index = 0
            if(line_index == 7):
                output.write('%d*%X'%(repetition + 1, current_word))
            else:
                output.write('%d*%X '%(repetition + 1, current_word))
            line_index += 1
        else:
            for _ in range(repetition + 1):
                if(line_index == 8):
                    output.write('\n')
                    line_index = 0
                if(line_index == 7):
                    output.write('%X'%(current_word))
                else:
                    output.write('%X '%(current_word))
                line_index += 1
        output.write('\n')
    # DEBUG format
    ## Most human readability
    ## Not for normal use
    elif(format_style == 'debug'):
        if(verbose_level >= 1):
            print(" DEBUG format.")
        line_address_size = int(log(find_max(assembler_output, key = lambda x:x[1]), 10) + 1)
        for machine_code in assembler_output:
            output.write('%0*d:%0*X: %s'%(line_address_size, machine_code[1], ROM_address_size, machine_code[2], " ".join("%0*X"%(word_size, x) for x in word_dissect(machine_code[0], machine_code[3], WORD_LENGTH))))
            if(len(machine_code) >= 5):
                output.write(' ; %s'%(recompose_line(machine_code[4])))
            output.write('\n')
    else:
        fatal_error('formatter', f"Don\'t know format \'{format_style}\'")

    output.close()
