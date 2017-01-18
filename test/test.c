#include<stdio.h>

typedef unsigned char       u8;
typedef unsigned short      u16;
typedef unsigned int        u32;
typedef unsigned long long  u64;

typedef char                i8;
typedef short               i16;
typedef int                 i32;
typedef long long           i64;

typedef enum e_def
{
    e_def_1 = 1,
    e_def_2 = 2,
    e_def_3 = 3,
    e_def_4 = 4,
    e_def_5 = 5,
    e_def_6 = 6,
    e_def_7 = 7,
    e_def_8 = 8
}e_def;

//basic
typedef struct s_def_1
{
   u8               a;
   u16              b;
   u32              c;
   u64              d;
   i8               e;
   i16              f;
   i32              g;
   i64              h;
}s_def_1;

//volatile
typedef struct s_def_2
{
   volatile u8      a;
   volatile u16     b;
   volatile u32     c;
   volatile u64     d;
   volatile i8      e;
   volatile i16     f;
   volatile i32     g;
   volatile i64     h;
}s_def_2;

//array
#define SIZE 9
typedef struct s_def_3
{
   u8         a[SIZE];
   u16        b[SIZE];
   u32        c[SIZE];
   u64        d[SIZE];
   i8         e[SIZE];
   i16        f[SIZE];
   i32        g[SIZE];
   i64        h[SIZE];
}s_def_3;

//pointer
typedef struct s_def_4
{
   u8*              a;
   u16*             b;
   u32*             c;
   u64*             d;
   i8*              e;
   i16*             f;
   i32*             g;
   i64*             h;
}s_def_4;

//enum
typedef struct s_def_5
{
   e_def            a;
   e_def            b;
   e_def            c;
   e_def            d;
   e_def            e;
   e_def            f;
   e_def            g;
   e_def            h;
}s_def_5;

//function pointer
typedef void (*f_ptr)(void);

typedef struct s_def_6
{
   f_ptr            a;
   f_ptr            b;
   f_ptr            c;
   f_ptr            d;
   f_ptr            e;
   f_ptr            f;
   f_ptr            g;
   f_ptr            h;
}s_def_6;

typedef struct s_defs
{
    s_def_1      def1;
    s_def_2      def2;
    s_def_3      def3;
    s_def_4      def4;
    s_def_5      def5;
    s_def_6      def6;
}s_defs;

static s_defs data;

int main(void)
{
    u32 j = 0;
    u32 i = 1;
    data.def1.a = i++;
    data.def1.b = i++;
    data.def1.c = i++;
    data.def1.d = i++;
    data.def1.e = i++;
    data.def1.f = i++;
    data.def1.g = i++;
    data.def1.h = i++;

    data.def2.a = i++;
    data.def2.b = i++;
    data.def2.c = i++;
    data.def2.d = i++;
    data.def2.e = i++;
    data.def2.f = i++;
    data.def2.g = i++;
    data.def2.h = i++;

    for(j = 0; j < SIZE; j++)
        data.def3.a[j] = i++;
    for(j = 0; j < SIZE; j++)
        data.def3.b[j] = i++;
    for(j = 0; j < SIZE; j++)
        data.def3.c[j] = i++;
    for(j = 0; j < SIZE; j++)
        data.def3.d[j] = i++;
    for(j = 0; j < SIZE; j++)
        data.def3.e[j] = i++;
    for(j = 0; j < SIZE; j++)
        data.def3.f[j] = i++;
    for(j = 0; j < SIZE; j++)
        data.def3.g[j] = i++;
    for(j = 0; j < SIZE; j++)
        data.def3.h[j] = i++;

    
    data.def4.a = i++;
    data.def4.b = i++;
    data.def4.c = i++;
    data.def4.d = i++;
    data.def4.e = i++;
    data.def4.f = i++;
    data.def4.g = i++;
    data.def4.h = i++;
    
    data.def5.a = i++;
    data.def5.b = i++;
    data.def5.c = i++;
    data.def5.d = i++;
    data.def5.e = i++;
    data.def5.f = i++;
    data.def5.g = i++;
    data.def5.h = i++;
    
    data.def6.a = i++;
    data.def6.b = i++;
    data.def6.c = i++;
    data.def6.d = i++;
    data.def6.e = i++;
    data.def6.f = i++;
    data.def6.g = i++;
    data.def6.h = i++;

    FILE *ptr = fopen("test.bin", "wb");
    if(ptr != NULL)
        fwrite(&data, sizeof(data), 1, ptr);
    fclose(ptr);

    return 0;
}
