## What is bin2struct
bin2struct is a utility to convert the binary memory dump of c data structure to the readable text, with the annotated structure field's name for every line of data. 

It use pyelftools to parse the elf target file and extract the structure member information from the dwarf. therefore, you must specify necessary compiler flag to build your target to have the dwarf contained in your target, like '-g' in the gcc.

#### Usage example
Compile below c source code and execute the target, you will get one target file "test.out" and one dump file "test.bin". 
 
	// compile: $gcc -g test.c -o test.out
    // execute: $./test.out
	#include<stdio.h>

	typedef struct sdef
	{
		unsigned char      a;
		unsigned short     b;
		unsigned int       c;
		unsigned long long d;
	}sdef;

	int main(void)
	{
		sdef data;
		data.a = 1;
		data.b = 2;
		data.c = 3;
		data.d = 4;
		
		FILE *f = fopen("test.bin", "wb");
		if(!f)
			fwrite(&data, sizeof(data), 1, f);
		fclose(f);

		return 0;
	}

with those two files, you can use below command 
> $python bts.py -t test.out -s sdef -b test.bin -o test.txt  

to convert the dump into a readable text as below:

	              0x01  |  sdef.a(1)
	            0x0002  |  sdef.b(2)
	        0x00000003  |  sdef.c(4)
	0x0000000000000004  |  sdef.d(8)



## Supports and Limitaions
- Support DWARF2, DWARF3, DWARF4 format, only test on amd64 with gcc
- Support base types, pointer types, enum, arrays, volatile type and nest of those.
- Other types like bit fields not added yet. 
- Other platform may need additional effort as pyelftools limitation.

## License
>This program is free software; you can redistribute it and/or modify it under
> the terms of the GNU Lesser General Public License as published by the Free
> Software Foundation; either version 3 of the License, or (at your option) any
> later version.

> This program is distributed in the hope that it will be useful,but WITHOUT ANY
> WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
> FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

> You should have received a copy of the GNU Lesser General Public License along
> with this program. If not, see <http://www.gnu.org/licenses/>.