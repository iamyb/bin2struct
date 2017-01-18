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
import sys

sys.path[0:0] = ['.', '../lib/pyelftools']
from collections import namedtuple, OrderedDict
from elftools.common.py3compat import iterkeys
from elftools.elf.elffile import ELFFile

class bts_die_cache(object):
    def __init__(self, elffile):
        self.die_collections = {}
        self.cu_boundary_map = OrderedDict()
        self._load_dwarf(elffile)

    # -------------------------------- PUBLIC ---------------------------------#
    def get(self, offset):
        if self.die_collections.has_key(offset):
            return self.die_collections[offset]
        else:
            self._collec_cu_die(self._find_cu(offset))
            return self.die_collections[offset]
    # -------------------------------- PRIVATE --------------------------------#
    def _load_dwarf(self, elffile):
        dwarfinfo = elffile.get_dwarf_info()
        for CU in dwarfinfo.iter_CUs():
            self.cu_boundary_map[CU.get_boundary()] = CU

    def _collect_die(self, die):
        for child in die.iter_children():
            self.die_collections[child.get_offset()] = child;
            self._collect_die(child)

    def _collec_cu_die(self, cu):
        top_DIE = cu.get_top_DIE()
        self.die_collections[top_DIE.get_offset()] = top_DIE
        self._collect_die(top_DIE)

    def _find_cu(self, offset):
        boundary_list = iterkeys(self.cu_boundary_map)
        prev = 0
        for boundary in boundary_list:
            if (prev < offset < boundary):
                return self.cu_boundary_map[boundary]
            prev = boundary
        return None
