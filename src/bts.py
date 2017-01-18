################################################################################
# Copyright (C) 2016 b20yang
# ---
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful,but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
################################################################################
from __future__ import print_function
import os, sys, getopt, struct

sys.path[0:0] = ['.', '../lib/pyelftools']
from elftools.elf.elffile import ELFFile
from bts_die_cache import bts_die_cache




# ------------------------------------------------------------------------------
class bts_struct_info(object):
    def __init__(self, name, source):
        self.name = name
        self.source = source
        self.type_info = []

    def get_name(self):
        return self.name

    def get_source(self):
        return self.source

    def add_info(self, info):
        self.type_info.append(info)

    def get_info(self):
        return self.type_info

# Could be moved into bts_struct_info
# ------------------------------------------------------------------------------
def read_data(offset, size, f):
    f.seek(offset)
    value = f.read(size)
    if value == '':
        print("reach binary file end...please check!")
        sys.exit(2)
        #return 0xABABABAB

    if   size == 8:
        return struct.unpack('<Q', value)[0]
    elif size == 4:
        return struct.unpack('<I', value)[0]
    elif size == 2:
        return struct.unpack('<H', value)[0]
    elif size == 1:
        return struct.unpack('<B', value)[0]


def print_struct(struct, data, output="results.txt"):
    b = open(data, "rb")
    o = open(output, "w")

    fields = struct.get_info();
    for (location, size, name) in fields:
        value = read_data(location, size, b)
        o.write("0x%08x |  %s(%s)\n" % ((value), name, size))
    b.close()
    o.close()


# DIE Attributes Helper Functions
# ------------------------------------------------------------------------------
def get_DW_AT_name(die):
    if(die.attributes.has_key('DW_AT_name')):
        return die.attributes['DW_AT_name'].value
    else:
        #print ("Oops, there is no valid key. DW_AT_name")
     #   sys.exit(2)
        return None;


def get_DW_AT_type(die):
    if (die.attributes.has_key('DW_AT_type')):
        return die.attributes['DW_AT_type'].value
    else:
        #print ("Oops, there is no valid key. DW_AT_type")
      #  sys.exit(2)
        return None


def get_DW_AT_byte_size(die):
    if (die.attributes.has_key('DW_AT_byte_size')):
        return die.attributes['DW_AT_byte_size'].value
    else:
        #print("Oops, there is no valid key. DW_AT_byte_size")
       # sys.exit(2)
        return None


def get_DW_AT_upper_bound(die):
    if (die.attributes.has_key('DW_AT_upper_bound')):
        return die.attributes['DW_AT_upper_bound'].value
    else:
        #print("Oops, there is no valid key. DW_AT_upper_bound")
        #sys.exit(2)
        return None


def decode_leb128(values):
    result = 0;
    shift = 0;
    for data in values:
        result |= ((data & 0x7f) << shift);
        if ( (data & 0x80) == 0):
            break;
        shift += 7;
    return result


def get_DW_AT_data_member_location(die):
    if (die.attributes.has_key('DW_AT_data_member_location')):
        values = die.attributes['DW_AT_data_member_location'].value[1:]
        return decode_leb128(values)
    else:
        return None


# Type Parsing
# ------------------------------------------------------------------------------
def parse_struct_type(die, name, base, cache, struct):
    for child in die.iter_children():
        prefix = name + "." + get_DW_AT_name(child)
        offset = get_DW_AT_type(child)
        location = get_DW_AT_data_member_location(child)
        parse_member(offset, prefix, base+location, cache, struct)
    return get_DW_AT_byte_size(die);


# ------------------------------------------------------------------------------
def parse_array_type(die, name, location, cache, struct):
    offset = get_DW_AT_type(die)
    loop = 0;
    for child in die.iter_children():
        if child.tag == 'DW_TAG_subrange_type':
            loop = get_DW_AT_upper_bound(child) + 1
            break

    size = 0
    for i in range(loop):
        name_idx = (name + "[%s]") % (i)
        size += parse_member(offset, name_idx, location+size, cache, struct)
    return size


# ------------------------------------------------------------------------------
def parse_base_type(die, name, location, struct):
    size = get_DW_AT_byte_size(die)
    struct.add_info((location, size, name))
    #print (location ,size , name)
    return size

#-------------------------------------------------------------------------------
def parse_member(index, name, location, cache, struct):
    die = cache.get(index)
    if(die.tag == 'DW_TAG_base_type'):
        size = parse_base_type(die, name, location, struct)
    elif(die.tag == 'DW_TAG_enumeration_type'):
        size = parse_base_type(die, name, location, struct)
    elif(die.tag == 'DW_TAG_pointer_type'):
        size = parse_base_type(die, name, location, struct)
    elif(die.tag == 'DW_TAG_array_type'):
        size = parse_array_type(die, name, location, cache, struct)
    elif(die.tag == 'DW_TAG_structure_type'):
        size = parse_struct_type(die, name, location, cache, struct)
    elif(die.tag == 'DW_TAG_typedef'):
        offset = get_DW_AT_type(die)
        size = parse_member(offset, name, location, cache, struct)
    elif(die.tag == 'DW_TAG_volatile_type'):
        offset = get_DW_AT_type(die)
        size = parse_member(offset, name, location, cache, struct)
    elif(die.tag == 'DW_TAG_subroutine_type'):
        offset = get_DW_AT_type(die)
        size = parse_member(offset, name, location, cache, struct)
    else:
        print ("NOT supported %s" %  die.tag)
    return size;


# ------------------------------------------------------------------------------
def process_file(filename, struct_name, binary, output, source=""):
    with open(filename, 'rb') as f:
        elffile = ELFFile(f)

        if not elffile.has_dwarf_info():
            print('  file has no DWARF info')
            return

        cache = bts_die_cache(elffile)
        struct = bts_struct_info(struct_name, source)

        offset = find_struct(elffile, struct)
        if( offset == None):
            print (" can't find this struct %s" % struct)
            return

        struct_die = cache.get(offset)
        parse_struct_type(struct_die, struct.get_name(), 0, cache, struct)
        print_struct(struct, binary, output)


# ------------------------------------------------------------------------------
def find_struct(elffile, info):
    dwarfinfo = elffile.get_dwarf_info()
    for CU in dwarfinfo.iter_CUs():
        top_DIE = CU.get_top_DIE()
        if info.get_source() in str(get_DW_AT_name(top_DIE)):
            offset = iter_top_die(top_DIE, info.get_name(), CU)
            if (offset > 0):
                return offset
    return None

def iter_top_die(die, struct_name, CU):
    for child in die.iter_children():
        if child.tag == 'DW_TAG_structure_type' :
            if get_DW_AT_name(child) == struct_name:
                return child.get_offset()
    return None


# ------------------------------------------------------------------------------
def usage():
    print('bts.py -t <target> -s <struct> -b <binary> -o <output>')
    sys.exit(2)


def main(argv):
    opts, args = getopt.getopt(
        argv, "ht:b:s:o", ['target=', 'binary=', 'struct=', 'output='])

    if len(opts) < 3:
        usage()

    target_file, binary_file, struct_name, output_file = ('', '', '', '')

    for opt, arg in opts:
        if opt in ("-t", "--target"):
            target_file = arg
        elif opt in ("-b", "--binary"):
            binary_file = arg
        elif opt in ("-s", "--struct"):
            struct_name = arg
        elif opt in ("-o", "--output"):
            output_file = args[0]

    if(output_file == ''):
        output_file = os.path.splitext(binary_file)[0]+'.txt'

    process_file(target_file, struct_name, binary_file, output_file)


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    main(sys.argv[1:])

