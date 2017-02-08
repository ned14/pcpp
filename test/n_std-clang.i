# 1 "test/test-c/n_std.c"
# 1 "<built-in>" 1
# 1 "<built-in>" 3
# 312 "<built-in>" 3
# 1 "<command line>" 1
# 1 "<built-in>" 2
# 1 "test/test-c/n_std.c" 2
# 18 "test/test-c/n_std.c"
# 1 "test/test-c/defs.h" 1


# 1 "/usr/include/stdio.h" 1 3 4
# 27 "/usr/include/stdio.h" 3 4
# 1 "/usr/include/features.h" 1 3 4
# 352 "/usr/include/features.h" 3 4
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 353 "/usr/include/features.h" 2 3 4
# 374 "/usr/include/features.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/sys/cdefs.h" 1 3 4
# 385 "/usr/include/x86_64-linux-gnu/sys/cdefs.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/bits/wordsize.h" 1 3 4
# 386 "/usr/include/x86_64-linux-gnu/sys/cdefs.h" 2 3 4
# 375 "/usr/include/features.h" 2 3 4
# 398 "/usr/include/features.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/gnu/stubs.h" 1 3 4
# 10 "/usr/include/x86_64-linux-gnu/gnu/stubs.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/gnu/stubs-64.h" 1 3 4
# 11 "/usr/include/x86_64-linux-gnu/gnu/stubs.h" 2 3 4
# 399 "/usr/include/features.h" 2 3 4
# 28 "/usr/include/stdio.h" 2 3 4





# 1 "/usr/lib/llvm-3.5/bin/../lib/clang/3.5.0/include/stddef.h" 1 3 4
# 58 "/usr/lib/llvm-3.5/bin/../lib/clang/3.5.0/include/stddef.h" 3 4
typedef long unsigned int size_t;
# 34 "/usr/include/stdio.h" 2 3 4

# 1 "/usr/include/x86_64-linux-gnu/bits/types.h" 1 3 4
# 27 "/usr/include/x86_64-linux-gnu/bits/types.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/bits/wordsize.h" 1 3 4
# 28 "/usr/include/x86_64-linux-gnu/bits/types.h" 2 3 4


typedef unsigned char __u_char;
typedef unsigned short int __u_short;
typedef unsigned int __u_int;
typedef unsigned long int __u_long;


typedef signed char __int8_t;
typedef unsigned char __uint8_t;
typedef signed short int __int16_t;
typedef unsigned short int __uint16_t;
typedef signed int __int32_t;
typedef unsigned int __uint32_t;

typedef signed long int __int64_t;
typedef unsigned long int __uint64_t;







typedef long int __quad_t;
typedef unsigned long int __u_quad_t;
# 121 "/usr/include/x86_64-linux-gnu/bits/types.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/bits/typesizes.h" 1 3 4
# 122 "/usr/include/x86_64-linux-gnu/bits/types.h" 2 3 4


typedef unsigned long int __dev_t;
typedef unsigned int __uid_t;
typedef unsigned int __gid_t;
typedef unsigned long int __ino_t;
typedef unsigned long int __ino64_t;
typedef unsigned int __mode_t;
typedef unsigned long int __nlink_t;
typedef long int __off_t;
typedef long int __off64_t;
typedef int __pid_t;
typedef struct { int __val[2]; } __fsid_t;
typedef long int __clock_t;
typedef unsigned long int __rlim_t;
typedef unsigned long int __rlim64_t;
typedef unsigned int __id_t;
typedef long int __time_t;
typedef unsigned int __useconds_t;
typedef long int __suseconds_t;

typedef int __daddr_t;
typedef int __key_t;


typedef int __clockid_t;


typedef void * __timer_t;


typedef long int __blksize_t;




typedef long int __blkcnt_t;
typedef long int __blkcnt64_t;


typedef unsigned long int __fsblkcnt_t;
typedef unsigned long int __fsblkcnt64_t;


typedef unsigned long int __fsfilcnt_t;
typedef unsigned long int __fsfilcnt64_t;


typedef long int __fsword_t;

typedef long int __ssize_t;


typedef long int __syscall_slong_t;

typedef unsigned long int __syscall_ulong_t;



typedef __off64_t __loff_t;
typedef __quad_t *__qaddr_t;
typedef char *__caddr_t;


typedef long int __intptr_t;


typedef unsigned int __socklen_t;
# 36 "/usr/include/stdio.h" 2 3 4








struct _IO_FILE;



typedef struct _IO_FILE FILE;
# 64 "/usr/include/stdio.h" 3 4
typedef struct _IO_FILE __FILE;
# 74 "/usr/include/stdio.h" 3 4
# 1 "/usr/include/libio.h" 1 3 4
# 31 "/usr/include/libio.h" 3 4
# 1 "/usr/include/_G_config.h" 1 3 4
# 15 "/usr/include/_G_config.h" 3 4
# 1 "/usr/lib/llvm-3.5/bin/../lib/clang/3.5.0/include/stddef.h" 1 3 4
# 16 "/usr/include/_G_config.h" 2 3 4




# 1 "/usr/include/wchar.h" 1 3 4
# 82 "/usr/include/wchar.h" 3 4
typedef struct
{
  int __count;
  union
  {

    unsigned int __wch;



    char __wchb[4];
  } __value;
} __mbstate_t;
# 21 "/usr/include/_G_config.h" 2 3 4
typedef struct
{
  __off_t __pos;
  __mbstate_t __state;
} _G_fpos_t;
typedef struct
{
  __off64_t __pos;
  __mbstate_t __state;
} _G_fpos64_t;
# 32 "/usr/include/libio.h" 2 3 4
# 49 "/usr/include/libio.h" 3 4
# 1 "/usr/lib/llvm-3.5/bin/../lib/clang/3.5.0/include/stdarg.h" 1 3 4
# 30 "/usr/lib/llvm-3.5/bin/../lib/clang/3.5.0/include/stdarg.h" 3 4
typedef __builtin_va_list va_list;
# 50 "/usr/lib/llvm-3.5/bin/../lib/clang/3.5.0/include/stdarg.h" 3 4
typedef __builtin_va_list __gnuc_va_list;
# 50 "/usr/include/libio.h" 2 3 4
# 144 "/usr/include/libio.h" 3 4
struct _IO_jump_t; struct _IO_FILE;
# 154 "/usr/include/libio.h" 3 4
typedef void _IO_lock_t;





struct _IO_marker {
  struct _IO_marker *_next;
  struct _IO_FILE *_sbuf;



  int _pos;
# 177 "/usr/include/libio.h" 3 4
};


enum __codecvt_result
{
  __codecvt_ok,
  __codecvt_partial,
  __codecvt_error,
  __codecvt_noconv
};
# 245 "/usr/include/libio.h" 3 4
struct _IO_FILE {
  int _flags;




  char* _IO_read_ptr;
  char* _IO_read_end;
  char* _IO_read_base;
  char* _IO_write_base;
  char* _IO_write_ptr;
  char* _IO_write_end;
  char* _IO_buf_base;
  char* _IO_buf_end;

  char *_IO_save_base;
  char *_IO_backup_base;
  char *_IO_save_end;

  struct _IO_marker *_markers;

  struct _IO_FILE *_chain;

  int _fileno;



  int _flags2;

  __off_t _old_offset;



  unsigned short _cur_column;
  signed char _vtable_offset;
  char _shortbuf[1];



  _IO_lock_t *_lock;
# 293 "/usr/include/libio.h" 3 4
  __off64_t _offset;
# 302 "/usr/include/libio.h" 3 4
  void *__pad1;
  void *__pad2;
  void *__pad3;
  void *__pad4;
  size_t __pad5;

  int _mode;

  char _unused2[15 * sizeof (int) - 4 * sizeof (void *) - sizeof (size_t)];

};


typedef struct _IO_FILE _IO_FILE;


struct _IO_FILE_plus;

extern struct _IO_FILE_plus _IO_2_1_stdin_;
extern struct _IO_FILE_plus _IO_2_1_stdout_;
extern struct _IO_FILE_plus _IO_2_1_stderr_;
# 338 "/usr/include/libio.h" 3 4
typedef __ssize_t __io_read_fn (void *__cookie, char *__buf, size_t __nbytes);







typedef __ssize_t __io_write_fn (void *__cookie, const char *__buf,
     size_t __n);







typedef int __io_seek_fn (void *__cookie, __off64_t *__pos, int __w);


typedef int __io_close_fn (void *__cookie);
# 390 "/usr/include/libio.h" 3 4
extern int __underflow (_IO_FILE *);
extern int __uflow (_IO_FILE *);
extern int __overflow (_IO_FILE *, int);
# 434 "/usr/include/libio.h" 3 4
extern int _IO_getc (_IO_FILE *__fp);
extern int _IO_putc (int __c, _IO_FILE *__fp);
extern int _IO_feof (_IO_FILE *__fp) __attribute__ ((__nothrow__ ));
extern int _IO_ferror (_IO_FILE *__fp) __attribute__ ((__nothrow__ ));

extern int _IO_peekc_locked (_IO_FILE *__fp);





extern void _IO_flockfile (_IO_FILE *) __attribute__ ((__nothrow__ ));
extern void _IO_funlockfile (_IO_FILE *) __attribute__ ((__nothrow__ ));
extern int _IO_ftrylockfile (_IO_FILE *) __attribute__ ((__nothrow__ ));
# 464 "/usr/include/libio.h" 3 4
extern int _IO_vfscanf (_IO_FILE * __restrict, const char * __restrict,
   __gnuc_va_list, int *__restrict);
extern int _IO_vfprintf (_IO_FILE *__restrict, const char *__restrict,
    __gnuc_va_list);
extern __ssize_t _IO_padn (_IO_FILE *, int, __ssize_t);
extern size_t _IO_sgetn (_IO_FILE *, void *, size_t);

extern __off64_t _IO_seekoff (_IO_FILE *, __off64_t, int, int);
extern __off64_t _IO_seekpos (_IO_FILE *, __off64_t, int);

extern void _IO_free_backup_area (_IO_FILE *) __attribute__ ((__nothrow__ ));
# 75 "/usr/include/stdio.h" 2 3 4




typedef __gnuc_va_list va_list;
# 90 "/usr/include/stdio.h" 3 4
typedef __off_t off_t;
# 102 "/usr/include/stdio.h" 3 4
typedef __ssize_t ssize_t;







typedef _G_fpos_t fpos_t;
# 164 "/usr/include/stdio.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/bits/stdio_lim.h" 1 3 4
# 165 "/usr/include/stdio.h" 2 3 4



extern struct _IO_FILE *stdin;
extern struct _IO_FILE *stdout;
extern struct _IO_FILE *stderr;







extern int remove (const char *__filename) __attribute__ ((__nothrow__ ));

extern int rename (const char *__old, const char *__new) __attribute__ ((__nothrow__ ));




extern int renameat (int __oldfd, const char *__old, int __newfd,
       const char *__new) __attribute__ ((__nothrow__ ));
# 195 "/usr/include/stdio.h" 3 4
extern FILE *tmpfile (void) ;
# 209 "/usr/include/stdio.h" 3 4
extern char *tmpnam (char *__s) __attribute__ ((__nothrow__ )) ;





extern char *tmpnam_r (char *__s) __attribute__ ((__nothrow__ )) ;
# 227 "/usr/include/stdio.h" 3 4
extern char *tempnam (const char *__dir, const char *__pfx)
     __attribute__ ((__nothrow__ )) __attribute__ ((__malloc__)) ;
# 237 "/usr/include/stdio.h" 3 4
extern int fclose (FILE *__stream);




extern int fflush (FILE *__stream);
# 252 "/usr/include/stdio.h" 3 4
extern int fflush_unlocked (FILE *__stream);
# 272 "/usr/include/stdio.h" 3 4
extern FILE *fopen (const char *__restrict __filename,
      const char *__restrict __modes) ;




extern FILE *freopen (const char *__restrict __filename,
        const char *__restrict __modes,
        FILE *__restrict __stream) ;
# 306 "/usr/include/stdio.h" 3 4
extern FILE *fdopen (int __fd, const char *__modes) __attribute__ ((__nothrow__ )) ;
# 319 "/usr/include/stdio.h" 3 4
extern FILE *fmemopen (void *__s, size_t __len, const char *__modes)
  __attribute__ ((__nothrow__ )) ;




extern FILE *open_memstream (char **__bufloc, size_t *__sizeloc) __attribute__ ((__nothrow__ )) ;






extern void setbuf (FILE *__restrict __stream, char *__restrict __buf) __attribute__ ((__nothrow__ ));



extern int setvbuf (FILE *__restrict __stream, char *__restrict __buf,
      int __modes, size_t __n) __attribute__ ((__nothrow__ ));





extern void setbuffer (FILE *__restrict __stream, char *__restrict __buf,
         size_t __size) __attribute__ ((__nothrow__ ));


extern void setlinebuf (FILE *__stream) __attribute__ ((__nothrow__ ));
# 356 "/usr/include/stdio.h" 3 4
extern int fprintf (FILE *__restrict __stream,
      const char *__restrict __format, ...);




extern int printf (const char *__restrict __format, ...);

extern int sprintf (char *__restrict __s,
      const char *__restrict __format, ...) __attribute__ ((__nothrow__));





extern int vfprintf (FILE *__restrict __s, const char *__restrict __format,
       __gnuc_va_list __arg);




extern int vprintf (const char *__restrict __format, __gnuc_va_list __arg);

extern int vsprintf (char *__restrict __s, const char *__restrict __format,
       __gnuc_va_list __arg) __attribute__ ((__nothrow__));





extern int snprintf (char *__restrict __s, size_t __maxlen,
       const char *__restrict __format, ...)
     __attribute__ ((__nothrow__)) __attribute__ ((__format__ (__printf__, 3, 4)));

extern int vsnprintf (char *__restrict __s, size_t __maxlen,
        const char *__restrict __format, __gnuc_va_list __arg)
     __attribute__ ((__nothrow__)) __attribute__ ((__format__ (__printf__, 3, 0)));
# 412 "/usr/include/stdio.h" 3 4
extern int vdprintf (int __fd, const char *__restrict __fmt,
       __gnuc_va_list __arg)
     __attribute__ ((__format__ (__printf__, 2, 0)));
extern int dprintf (int __fd, const char *__restrict __fmt, ...)
     __attribute__ ((__format__ (__printf__, 2, 3)));
# 425 "/usr/include/stdio.h" 3 4
extern int fscanf (FILE *__restrict __stream,
     const char *__restrict __format, ...) ;




extern int scanf (const char *__restrict __format, ...) ;

extern int sscanf (const char *__restrict __s,
     const char *__restrict __format, ...) __attribute__ ((__nothrow__ ));
# 443 "/usr/include/stdio.h" 3 4
extern int fscanf (FILE *__restrict __stream, const char *__restrict __format, ...) __asm__ ("" "__isoc99_fscanf") ;


extern int scanf (const char *__restrict __format, ...) __asm__ ("" "__isoc99_scanf") ;

extern int sscanf (const char *__restrict __s, const char *__restrict __format, ...) __asm__ ("" "__isoc99_sscanf") __attribute__ ((__nothrow__ ));
# 471 "/usr/include/stdio.h" 3 4
extern int vfscanf (FILE *__restrict __s, const char *__restrict __format,
      __gnuc_va_list __arg)
     __attribute__ ((__format__ (__scanf__, 2, 0))) ;





extern int vscanf (const char *__restrict __format, __gnuc_va_list __arg)
     __attribute__ ((__format__ (__scanf__, 1, 0))) ;


extern int vsscanf (const char *__restrict __s,
      const char *__restrict __format, __gnuc_va_list __arg)
     __attribute__ ((__nothrow__ )) __attribute__ ((__format__ (__scanf__, 2, 0)));
# 494 "/usr/include/stdio.h" 3 4
extern int vfscanf (FILE *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg) __asm__ ("" "__isoc99_vfscanf")



     __attribute__ ((__format__ (__scanf__, 2, 0))) ;
extern int vscanf (const char *__restrict __format, __gnuc_va_list __arg) __asm__ ("" "__isoc99_vscanf")

     __attribute__ ((__format__ (__scanf__, 1, 0))) ;
extern int vsscanf (const char *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg) __asm__ ("" "__isoc99_vsscanf") __attribute__ ((__nothrow__ ))



     __attribute__ ((__format__ (__scanf__, 2, 0)));
# 531 "/usr/include/stdio.h" 3 4
extern int fgetc (FILE *__stream);
extern int getc (FILE *__stream);





extern int getchar (void);
# 550 "/usr/include/stdio.h" 3 4
extern int getc_unlocked (FILE *__stream);
extern int getchar_unlocked (void);
# 561 "/usr/include/stdio.h" 3 4
extern int fgetc_unlocked (FILE *__stream);
# 573 "/usr/include/stdio.h" 3 4
extern int fputc (int __c, FILE *__stream);
extern int putc (int __c, FILE *__stream);





extern int putchar (int __c);
# 594 "/usr/include/stdio.h" 3 4
extern int fputc_unlocked (int __c, FILE *__stream);







extern int putc_unlocked (int __c, FILE *__stream);
extern int putchar_unlocked (int __c);






extern int getw (FILE *__stream);


extern int putw (int __w, FILE *__stream);
# 622 "/usr/include/stdio.h" 3 4
extern char *fgets (char *__restrict __s, int __n, FILE *__restrict __stream)
          ;
# 638 "/usr/include/stdio.h" 3 4
extern char *gets (char *__s) __attribute__ ((__deprecated__));
# 665 "/usr/include/stdio.h" 3 4
extern __ssize_t __getdelim (char **__restrict __lineptr,
          size_t *__restrict __n, int __delimiter,
          FILE *__restrict __stream) ;
extern __ssize_t getdelim (char **__restrict __lineptr,
        size_t *__restrict __n, int __delimiter,
        FILE *__restrict __stream) ;







extern __ssize_t getline (char **__restrict __lineptr,
       size_t *__restrict __n,
       FILE *__restrict __stream) ;
# 689 "/usr/include/stdio.h" 3 4
extern int fputs (const char *__restrict __s, FILE *__restrict __stream);





extern int puts (const char *__s);






extern int ungetc (int __c, FILE *__stream);






extern size_t fread (void *__restrict __ptr, size_t __size,
       size_t __n, FILE *__restrict __stream) ;




extern size_t fwrite (const void *__restrict __ptr, size_t __size,
        size_t __n, FILE *__restrict __s);
# 737 "/usr/include/stdio.h" 3 4
extern size_t fread_unlocked (void *__restrict __ptr, size_t __size,
         size_t __n, FILE *__restrict __stream) ;
extern size_t fwrite_unlocked (const void *__restrict __ptr, size_t __size,
          size_t __n, FILE *__restrict __stream);
# 749 "/usr/include/stdio.h" 3 4
extern int fseek (FILE *__stream, long int __off, int __whence);




extern long int ftell (FILE *__stream) ;




extern void rewind (FILE *__stream);
# 773 "/usr/include/stdio.h" 3 4
extern int fseeko (FILE *__stream, __off_t __off, int __whence);




extern __off_t ftello (FILE *__stream) ;
# 798 "/usr/include/stdio.h" 3 4
extern int fgetpos (FILE *__restrict __stream, fpos_t *__restrict __pos);




extern int fsetpos (FILE *__stream, const fpos_t *__pos);
# 826 "/usr/include/stdio.h" 3 4
extern void clearerr (FILE *__stream) __attribute__ ((__nothrow__ ));

extern int feof (FILE *__stream) __attribute__ ((__nothrow__ )) ;

extern int ferror (FILE *__stream) __attribute__ ((__nothrow__ )) ;




extern void clearerr_unlocked (FILE *__stream) __attribute__ ((__nothrow__ ));
extern int feof_unlocked (FILE *__stream) __attribute__ ((__nothrow__ )) ;
extern int ferror_unlocked (FILE *__stream) __attribute__ ((__nothrow__ )) ;
# 846 "/usr/include/stdio.h" 3 4
extern void perror (const char *__s);







# 1 "/usr/include/x86_64-linux-gnu/bits/sys_errlist.h" 1 3 4
# 26 "/usr/include/x86_64-linux-gnu/bits/sys_errlist.h" 3 4
extern int sys_nerr;
extern const char *const sys_errlist[];
# 854 "/usr/include/stdio.h" 2 3 4




extern int fileno (FILE *__stream) __attribute__ ((__nothrow__ )) ;




extern int fileno_unlocked (FILE *__stream) __attribute__ ((__nothrow__ )) ;
# 873 "/usr/include/stdio.h" 3 4
extern FILE *popen (const char *__command, const char *__modes) ;





extern int pclose (FILE *__stream);





extern char *ctermid (char *__s) __attribute__ ((__nothrow__ ));
# 913 "/usr/include/stdio.h" 3 4
extern void flockfile (FILE *__stream) __attribute__ ((__nothrow__ ));



extern int ftrylockfile (FILE *__stream) __attribute__ ((__nothrow__ )) ;


extern void funlockfile (FILE *__stream) __attribute__ ((__nothrow__ ));
# 4 "test/test-c/defs.h" 2





# 1 "/usr/include/assert.h" 1 3 4
# 69 "/usr/include/assert.h" 3 4
extern void __assert_fail (const char *__assertion, const char *__file,
      unsigned int __line, const char *__function)
     __attribute__ ((__nothrow__ )) __attribute__ ((__noreturn__));


extern void __assert_perror_fail (int __errnum, const char *__file,
      unsigned int __line, const char *__function)
     __attribute__ ((__nothrow__ )) __attribute__ ((__noreturn__));




extern void __assert (const char *__assertion, const char *__file, int __line)
     __attribute__ ((__nothrow__ )) __attribute__ ((__noreturn__));
# 10 "test/test-c/defs.h" 2








extern int strcmp( const char *, const char *);
extern size_t strlen( const char *);
extern void exit( int);
# 19 "test/test-c/n_std.c" 2
# 30 "test/test-c/n_std.c"
void n_1( void);
void n_2( void);
void n_3( void);
void n_4( void);
void n_5( void);
void n_6( void);
void n_7( void);
void n_9( void);
void n_10( void);
void n_11( void);
void n_12( void);
void n_13( void);
void n_13_5( void);
void n_13_7( void);
void n_13_8( void);
void n_13_13( void);
void n_15( void);
void n_18( void);
void n_19( void);
void n_20( void);
void n_21( void);
void n_22( void);
void n_23( void);
void n_24( void);
void n_25( void);
void n_26( void);
void n_27( void);
void n_28( void);
void n_29( void);
void n_30( void);
void n_32( void);
void n_37( void);

int main( void)
{

    n_2();
    n_3();
    n_4();
    n_5();
    n_6();
    n_7();
    n_9();
    n_10();
    n_11();
    n_12();
    n_13();
    n_13_5();
    n_13_7();
    n_13_8();
    n_13_13();
    n_15();
    n_18();
    n_19();
    n_20();
    n_21();
    n_22();
    n_23();
    n_24();
    n_25();
    n_26();
    n_27();
    n_28();
    n_29();
    n_30();
    n_32();
    n_37();
    puts( "<End of \"n_std.c\">");
    return 0;
}

char quasi_trigraph[] = { '?', '?', ' ', '?', '?', '?', ' '
            , '?', '?', '%', ' ', '?', '?', '^', ' ', '?', '#', '\0' };

void n_2( void)

{
    int ab = 1, cd = 2, ef = 3, abcde = 5;





    ((ab + cd + ef == 6) ? (void) (0) : __assert_fail ("ab + cd + ef == 6", "test/test-c/n_std.c", 113, __PRETTY_FUNCTION__));
# 122 "test/test-c/n_std.c"
    ((ab + cd + ef == 6) ? (void) (0) : __assert_fail ("ab + cd + ef == 6", "test/test-c/n_std.c", 122, __PRETTY_FUNCTION__));


    ((strcmp( "abcde", "abcde") == 0) ? (void) (0) : __assert_fail ("strcmp( \"abcde\", \"abcde\") == 0", "test/test-c/n_std.c", 126, __PRETTY_FUNCTION__));



    ((abcde == 5) ? (void) (0) : __assert_fail ("abcde == 5", "test/test-c/n_std.c", 130, __PRETTY_FUNCTION__));


}

void n_3( void)

{
    int abcd = 4;


    ((strcmp( "abc de", "abc de") == 0) ? (void) (0) : __assert_fail ("strcmp( \"abc de\", \"abc de\") == 0", "test/test-c/n_std.c", 140, __PRETTY_FUNCTION__));
# 156 "test/test-c/n_std.c"
    ((abcd == 4) ? (void) (0) : __assert_fail ("abcd == 4", "test/test-c/n_std.c", 156, __PRETTY_FUNCTION__));
}

void n_4( void)

{



    ((strcmp( "abc", "abc") == 0) ? (void) (0) : __assert_fail ("strcmp( \"abc\", \"abc\") == 0", "test/test-c/n_std.c", 165, __PRETTY_FUNCTION__));


    ((strcmp( "<:", "<" ":") == 0) ? (void) (0) : __assert_fail ("strcmp( \"<:\", \"<\" \":\") == 0", "test/test-c/n_std.c", 168, __PRETTY_FUNCTION__));
}

void n_5( void)



{
    int abcde = 5;


    ((abcde == 5) ? (void) (0) : __assert_fail ("abcde == 5", "test/test-c/n_std.c", 179, __PRETTY_FUNCTION__));
}





# 1 "/usr/include/ctype.h" 1 3 4
# 39 "/usr/include/ctype.h" 3 4
# 1 "/usr/include/endian.h" 1 3 4
# 36 "/usr/include/endian.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/bits/endian.h" 1 3 4
# 37 "/usr/include/endian.h" 2 3 4
# 60 "/usr/include/endian.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/bits/byteswap.h" 1 3 4
# 28 "/usr/include/x86_64-linux-gnu/bits/byteswap.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/bits/wordsize.h" 1 3 4
# 29 "/usr/include/x86_64-linux-gnu/bits/byteswap.h" 2 3 4






# 1 "/usr/include/x86_64-linux-gnu/bits/byteswap-16.h" 1 3 4
# 36 "/usr/include/x86_64-linux-gnu/bits/byteswap.h" 2 3 4
# 61 "/usr/include/endian.h" 2 3 4
# 40 "/usr/include/ctype.h" 2 3 4






enum
{
  _ISupper = ((0) < 8 ? ((1 << (0)) << 8) : ((1 << (0)) >> 8)),
  _ISlower = ((1) < 8 ? ((1 << (1)) << 8) : ((1 << (1)) >> 8)),
  _ISalpha = ((2) < 8 ? ((1 << (2)) << 8) : ((1 << (2)) >> 8)),
  _ISdigit = ((3) < 8 ? ((1 << (3)) << 8) : ((1 << (3)) >> 8)),
  _ISxdigit = ((4) < 8 ? ((1 << (4)) << 8) : ((1 << (4)) >> 8)),
  _ISspace = ((5) < 8 ? ((1 << (5)) << 8) : ((1 << (5)) >> 8)),
  _ISprint = ((6) < 8 ? ((1 << (6)) << 8) : ((1 << (6)) >> 8)),
  _ISgraph = ((7) < 8 ? ((1 << (7)) << 8) : ((1 << (7)) >> 8)),
  _ISblank = ((8) < 8 ? ((1 << (8)) << 8) : ((1 << (8)) >> 8)),
  _IScntrl = ((9) < 8 ? ((1 << (9)) << 8) : ((1 << (9)) >> 8)),
  _ISpunct = ((10) < 8 ? ((1 << (10)) << 8) : ((1 << (10)) >> 8)),
  _ISalnum = ((11) < 8 ? ((1 << (11)) << 8) : ((1 << (11)) >> 8))
};
# 79 "/usr/include/ctype.h" 3 4
extern const unsigned short int **__ctype_b_loc (void)
     __attribute__ ((__nothrow__ )) __attribute__ ((__const__));
extern const __int32_t **__ctype_tolower_loc (void)
     __attribute__ ((__nothrow__ )) __attribute__ ((__const__));
extern const __int32_t **__ctype_toupper_loc (void)
     __attribute__ ((__nothrow__ )) __attribute__ ((__const__));
# 110 "/usr/include/ctype.h" 3 4
extern int isalnum (int) __attribute__ ((__nothrow__ ));
extern int isalpha (int) __attribute__ ((__nothrow__ ));
extern int iscntrl (int) __attribute__ ((__nothrow__ ));
extern int isdigit (int) __attribute__ ((__nothrow__ ));
extern int islower (int) __attribute__ ((__nothrow__ ));
extern int isgraph (int) __attribute__ ((__nothrow__ ));
extern int isprint (int) __attribute__ ((__nothrow__ ));
extern int ispunct (int) __attribute__ ((__nothrow__ ));
extern int isspace (int) __attribute__ ((__nothrow__ ));
extern int isupper (int) __attribute__ ((__nothrow__ ));
extern int isxdigit (int) __attribute__ ((__nothrow__ ));



extern int tolower (int __c) __attribute__ ((__nothrow__ ));


extern int toupper (int __c) __attribute__ ((__nothrow__ ));
# 136 "/usr/include/ctype.h" 3 4
extern int isblank (int) __attribute__ ((__nothrow__ ));
# 150 "/usr/include/ctype.h" 3 4
extern int isascii (int __c) __attribute__ ((__nothrow__ ));



extern int toascii (int __c) __attribute__ ((__nothrow__ ));



extern int _toupper (int) __attribute__ ((__nothrow__ ));
extern int _tolower (int) __attribute__ ((__nothrow__ ));
# 257 "/usr/include/ctype.h" 3 4
# 1 "/usr/include/xlocale.h" 1 3 4
# 27 "/usr/include/xlocale.h" 3 4
typedef struct __locale_struct
{

  struct __locale_data *__locales[13];


  const unsigned short int *__ctype_b;
  const int *__ctype_tolower;
  const int *__ctype_toupper;


  const char *__names[13];
} *__locale_t;


typedef __locale_t locale_t;
# 258 "/usr/include/ctype.h" 2 3 4
# 271 "/usr/include/ctype.h" 3 4
extern int isalnum_l (int, __locale_t) __attribute__ ((__nothrow__ ));
extern int isalpha_l (int, __locale_t) __attribute__ ((__nothrow__ ));
extern int iscntrl_l (int, __locale_t) __attribute__ ((__nothrow__ ));
extern int isdigit_l (int, __locale_t) __attribute__ ((__nothrow__ ));
extern int islower_l (int, __locale_t) __attribute__ ((__nothrow__ ));
extern int isgraph_l (int, __locale_t) __attribute__ ((__nothrow__ ));
extern int isprint_l (int, __locale_t) __attribute__ ((__nothrow__ ));
extern int ispunct_l (int, __locale_t) __attribute__ ((__nothrow__ ));
extern int isspace_l (int, __locale_t) __attribute__ ((__nothrow__ ));
extern int isupper_l (int, __locale_t) __attribute__ ((__nothrow__ ));
extern int isxdigit_l (int, __locale_t) __attribute__ ((__nothrow__ ));

extern int isblank_l (int, __locale_t) __attribute__ ((__nothrow__ ));



extern int __tolower_l (int __c, __locale_t __l) __attribute__ ((__nothrow__ ));
extern int tolower_l (int __c, __locale_t __l) __attribute__ ((__nothrow__ ));


extern int __toupper_l (int __c, __locale_t __l) __attribute__ ((__nothrow__ ));
extern int toupper_l (int __c, __locale_t __l) __attribute__ ((__nothrow__ ));
# 186 "test/test-c/n_std.c" 2


void n_6( void)

{
    int abc = 3;

    ((((*__ctype_b_loc ())[(int) (('a'))] & (unsigned short int) _ISalpha)) ? (void) (0) : __assert_fail ("((*__ctype_b_loc ())[(int) (('a'))] & (unsigned short int) _ISalpha)", "test/test-c/n_std.c", 193, __PRETTY_FUNCTION__));




# 1 "test/test-c/header.h" 1
# 198 "test/test-c/n_std.c" 2
 ((abc == 3) ? (void) (0) : __assert_fail ("abc == 3", "test/test-c/n_std.c", 198, __PRETTY_FUNCTION__));




# 1 "test/test-c/header.h" 1
# 203 "test/test-c/n_std.c" 2
 ((abc == 3) ? (void) (0) : __assert_fail ("abc == 3", "test/test-c/n_std.c", 203, __PRETTY_FUNCTION__));
}

void n_7( void)

{
# 1234 "cpp"
 ((1234 == 1234) ? (void) (0) : __assert_fail ("1234 == 1234", "cpp", 1234, __PRETTY_FUNCTION__));
    ((strcmp( "cpp", "cpp") == 0) ? (void) (0) : __assert_fail ("strcmp( \"cpp\", \"cpp\") == 0", "cpp", 1235, __PRETTY_FUNCTION__));
# 2345 "cpp"
 ((2345 == 2345) ? (void) (0) : __assert_fail ("2345 == 2345", "cpp", 2345, __PRETTY_FUNCTION__));
    ((strcmp( "cpp", "cpp") == 0) ? (void) (0) : __assert_fail ("strcmp( \"cpp\", \"cpp\") == 0", "cpp", 2346, __PRETTY_FUNCTION__));
# 1234 "n_7.c"
 ((1234 == 1234) ? (void) (0) : __assert_fail ("1234 == 1234", "n_7.c", 1234, __PRETTY_FUNCTION__));
    ((strcmp( "n_7.c", "n_7.c") == 0) ? (void) (0) : __assert_fail ("strcmp( \"n_7.c\", \"n_7.c\") == 0", "n_7.c", 1235, __PRETTY_FUNCTION__));
}
# 248 "n_std.c"

void n_9( void)

{



#pragma who knows ?
}

void n_10( void)

{







    ((1) ? (void) (0) : __assert_fail ("1", "n_std.c", 268, __PRETTY_FUNCTION__));
# 281 "n_std.c"
}

void n_11( void)

{
    int abc = 1, a = 0;







    ((abc) ? (void) (0) : __assert_fail ("abc", "n_std.c", 294, __PRETTY_FUNCTION__));


    ((abc) ? (void) (0) : __assert_fail ("abc", "n_std.c", 297, __PRETTY_FUNCTION__));
# 309 "n_std.c"
}


# 1 "/usr/lib/llvm-3.5/bin/../lib/clang/3.5.0/include/limits.h" 1 3
# 37 "/usr/lib/llvm-3.5/bin/../lib/clang/3.5.0/include/limits.h" 3
# 1 "/usr/include/limits.h" 1 3 4
# 143 "/usr/include/limits.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/bits/posix1_lim.h" 1 3 4
# 160 "/usr/include/x86_64-linux-gnu/bits/posix1_lim.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/bits/local_lim.h" 1 3 4
# 38 "/usr/include/x86_64-linux-gnu/bits/local_lim.h" 3 4
# 1 "/usr/include/linux/limits.h" 1 3 4
# 39 "/usr/include/x86_64-linux-gnu/bits/local_lim.h" 2 3 4
# 161 "/usr/include/x86_64-linux-gnu/bits/posix1_lim.h" 2 3 4
# 144 "/usr/include/limits.h" 2 3 4



# 1 "/usr/include/x86_64-linux-gnu/bits/posix2_lim.h" 1 3 4
# 148 "/usr/include/limits.h" 2 3 4
# 38 "/usr/lib/llvm-3.5/bin/../lib/clang/3.5.0/include/limits.h" 2 3
# 312 "n_std.c" 2

void n_12( void)

{
# 353 "n_std.c"
}

void n_13( void)
# 371 "n_std.c"
{
# 391 "n_std.c"
}

void n_13_5( void)

{
# 415 "n_std.c"
}

void n_13_7( void)

{
# 434 "n_std.c"
}

void n_13_8( void)

{
# 467 "n_std.c"
}

void n_13_13( void)

{
# 494 "n_std.c"
}

void n_15( void)

{



    ((1) ? (void) (0) : __assert_fail ("1", "n_std.c", 502, __PRETTY_FUNCTION__));
# 511 "n_std.c"
    ((1) ? (void) (0) : __assert_fail ("1", "n_std.c", 511, __PRETTY_FUNCTION__));

}

void n_18( void)




{
    int c = 3;


    (((1-1) == 0) ? (void) (0) : __assert_fail ("(1-1) == 0", "n_std.c", 524, __PRETTY_FUNCTION__));





    ((( c ) == 3) ? (void) (0) : __assert_fail ("( c ) == 3", "n_std.c", 530, __PRETTY_FUNCTION__));



    ((strcmp( "n1:n2", "n1:n2") == 0) ? (void) (0) : __assert_fail ("strcmp( \"n1:n2\", \"n1:n2\") == 0", "n_std.c", 534, __PRETTY_FUNCTION__));
}

void n_19( void)

{
    int c = 1;
# 549 "n_std.c"
    ((( c ) == 1) ? (void) (0) : __assert_fail ("( c ) == 1", "n_std.c", 549, __PRETTY_FUNCTION__));
}

void n_20( void)

{


    double fl;
    ((sizeof fl == sizeof (double)) ? (void) (0) : __assert_fail ("sizeof fl == sizeof (double)", "n_std.c", 558, __PRETTY_FUNCTION__));
}

void n_21( void)

{
    int a = 1, x = 2, y = -3;



    ((- - -a == -1) ? (void) (0) : __assert_fail ("---a == -1", "n_std.c", 568, __PRETTY_FUNCTION__));






    ((x- -y == -1) ? (void) (0) : __assert_fail ("x--y == -1", "n_std.c", 575, __PRETTY_FUNCTION__));
}

void n_22( void)

{



    ((strcmp( "12E+EXP", "12E+EXP") == 0) ? (void) (0) : __assert_fail ("strcmp( \"12E+EXP\", \"12E+EXP\") == 0", "n_std.c", 584, __PRETTY_FUNCTION__));


    ((strcmp( ".2e-EXP", ".2e-EXP") == 0) ? (void) (0) : __assert_fail ("strcmp( \".2e-EXP\", \".2e-EXP\") == 0", "n_std.c", 587, __PRETTY_FUNCTION__));



    ((strcmp( "12+1", "12+1") == 0) ? (void) (0) : __assert_fail ("strcmp( \"12+1\", \"12+1\") == 0", "n_std.c", 591, __PRETTY_FUNCTION__));
}

void n_23( void)

{
    int xy = 1;


    ((xy == 1) ? (void) (0) : __assert_fail ("xy == 1", "n_std.c", 600, __PRETTY_FUNCTION__));




    ((.12e+2 == 12.0) ? (void) (0) : __assert_fail (".12e+2 == 12.0", "n_std.c", 605, __PRETTY_FUNCTION__));
}

void n_24( void)

{

    ((strcmp( "a+b", "a+b") == 0) ? (void) (0) : __assert_fail ("strcmp( \"a+b\", \"a+b\") == 0", "n_std.c", 612, __PRETTY_FUNCTION__));



    ((strcmp( "ab + cd", "ab + cd") == 0) ? (void) (0) : __assert_fail ("strcmp( \"ab + cd\", \"ab + cd\") == 0", "n_std.c", 617, __PRETTY_FUNCTION__));




    ((strcmp( "'\"' + \"' \\\"\"", "'\"' + \"' \\\"\"") == 0) ? (void) (0) : __assert_fail ("strcmp( \"'\\\"' + \\\"' \\\\\\\"\\\"\", \"'\\\"' + \\\"' \\\\\\\"\\\"\") == 0", "n_std.c", 621, __PRETTY_FUNCTION__));



    ((strcmp( "\"abc\"", "\"abc\"") == 0) ? (void) (0) : __assert_fail ("strcmp( \"\\\"abc\\\"\", \"\\\"abc\\\"\") == 0", "n_std.c", 626, __PRETTY_FUNCTION__));





    ((strcmp( "x-y", "x-y") == 0) ? (void) (0) : __assert_fail ("strcmp( \"x-y\", \"x-y\") == 0", "n_std.c", 631, __PRETTY_FUNCTION__));
}

void n_25( void)



{
    int a = 1, b = 2, abc = 3, MACRO_0MACRO_1 = 2;






    (((a,b - 1) == 1) ? (void) (0) : __assert_fail ("(a,b - 1) == 1", "n_std.c", 646, __PRETTY_FUNCTION__));


    ((( - a) == -1) ? (void) (0) : __assert_fail ("( - a) == -1", "n_std.c", 649, __PRETTY_FUNCTION__));


    ((abc == 3) ? (void) (0) : __assert_fail ("abc == 3", "n_std.c", 652, __PRETTY_FUNCTION__));


    ((MACRO_0MACRO_1 == 2) ? (void) (0) : __assert_fail ("MACRO_0MACRO_1 == 2", "n_std.c", 655, __PRETTY_FUNCTION__));


    ((strcmp( "ZERO_TOKEN", "ZERO_TOKEN") == 0) ? (void) (0) : __assert_fail ("strcmp( \"ZERO_TOKEN\", \"ZERO_TOKEN\") == 0", "n_std.c", 658, __PRETTY_FUNCTION__));
}
# 676 "n_std.c"
int f( int a)
{
    return a;
}

int g( int a)
{
    return a * 2;
}


void n_26( void)

{
    int x = 1;
    int AB = 1;
    int Z[1];
    Z[0] = 1;




    ((Z[0] == 1) ? (void) (0) : __assert_fail ("Z[0] == 1", "n_std.c", 698, __PRETTY_FUNCTION__));





    ((AB == 1) ? (void) (0) : __assert_fail ("AB == 1", "n_std.c", 704, __PRETTY_FUNCTION__));




    ((x + f(x) == 2) ? (void) (0) : __assert_fail ("x + f(x) == 2", "n_std.c", 709, __PRETTY_FUNCTION__));





    ((x + x + g( x) == 4) ? (void) (0) : __assert_fail ("x + x + g( x) == 4", "n_std.c", 715, __PRETTY_FUNCTION__));



    ((Z[0] + f(Z[0]) == 2) ? (void) (0) : __assert_fail ("Z[0] + f(Z[0]) == 2", "n_std.c", 719, __PRETTY_FUNCTION__));
}

void n_27( void)




{
    int a = 1, b = 2, c, m = 1, n = 2;
# 739 "n_std.c"
    ((1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 == 36) ? (void) (0) : __assert_fail ("1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 == 36", "n_std.c", 739, __PRETTY_FUNCTION__));






    (((1) + (1 + 2) + 1 + 2 + 1 + 2 + 3 + 1 + 2 + 3 + 4 == 23) ? (void) (0) : __assert_fail ("(1) + (1 + 2) + 1 + 2 + 1 + 2 + 3 + 1 + 2 + 3 + 4 == 23", "n_std.c", 746, __PRETTY_FUNCTION__));


    ((1 == 1) ? (void) (0) : __assert_fail ("1 == 1", "n_std.c", 749, __PRETTY_FUNCTION__));






    ((((a) - (b)) == -1) ? (void) (0) : __assert_fail ("((a) - (b)) == -1", "n_std.c", 756, __PRETTY_FUNCTION__));


    c = (a - b);
    ((c == -1) ? (void) (0) : __assert_fail ("c == -1", "n_std.c", 760, __PRETTY_FUNCTION__));





    ((n == 2) ? (void) (0) : __assert_fail ("n == 2", "n_std.c", 766, __PRETTY_FUNCTION__));
}

void n_28( void)


{
    char * date = "Feb  7 2017";


    ((strcmp( "n_std.c", "n_std.c") == 0) ? (void) (0) : __assert_fail ("strcmp( \"n_std.c\", \"n_std.c\") == 0", "n_std.c", 776, __PRETTY_FUNCTION__));


    ((779 == 779) ? (void) (0) : __assert_fail ("779 == 779", "n_std.c", 779, __PRETTY_FUNCTION__));


    ((strlen( "Feb  7 2017") == 11) ? (void) (0) : __assert_fail ("strlen( \"Feb  7 2017\") == 11", "n_std.c", 782, __PRETTY_FUNCTION__));
    ((date[ 4] != '0') ? (void) (0) : __assert_fail ("date[ 4] != '0'", "n_std.c", 783, __PRETTY_FUNCTION__));


    ((strlen( "16:10:26") == 8) ? (void) (0) : __assert_fail ("strlen( \"16:10:26\") == 8", "n_std.c", 786, __PRETTY_FUNCTION__));


    ((1) ? (void) (0) : __assert_fail ("1", "n_std.c", 789, __PRETTY_FUNCTION__));


    ((199901L >= 199409L) ? (void) (0) : __assert_fail ("199901L >= 199409L", "n_std.c", 792, __PRETTY_FUNCTION__));



# 1 "test/test-c/line.h" 1


{
    char * file = "test/test-c/line.h";
    file += strlen( file) - 6;
    ((6 == 6 && strcmp( file, "line.h") == 0) ? (void) (0) : __assert_fail ("6 == 6 && strcmp( file, \"line.h\") == 0", "test/test-c/line.h", 6, __PRETTY_FUNCTION__));
}
# 796 "n_std.c" 2
}

void n_29( void)

{
    int DEFINED = 1;




    ((DEFINED == 1) ? (void) (0) : __assert_fail ("DEFINED == 1", "n_std.c", 806, __PRETTY_FUNCTION__));



}

void n_30( void)






{



    int a = 1, b = 2, c = 3;


    ((a + b + c == 6) ? (void) (0) : __assert_fail ("a + b + c == 6", "n_std.c", 835, __PRETTY_FUNCTION__));
# 836 "n_std.c"
}

void n_32( void)

{
# 850 "n_std.c"
}

void n_37( void)

{






    int ABCDEFGHIJKLMNOPQRSTUVWXYZabcde = 31;
    int ABCDEFGHIJKLMNOPQRSTUVWXYZabcd_ = 30;
    int nest = 0;


    ((ABCDEFGHIJKLMNOPQRSTUVWXYZabcde == 31) ? (void) (0) : __assert_fail ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcde == 31", "n_std.c", 869, __PRETTY_FUNCTION__));






    ((ABCDEFGHIJKLMNOPQRSTUVWXYZabcd_ == 30) ? (void) (0) : __assert_fail ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcd_ == 30", "n_std.c", 873, __PRETTY_FUNCTION__));


    nest = 0;
# 893 "n_std.c"
                                nest = 8;
# 902 "n_std.c"
    ((nest == 8) ? (void) (0) : __assert_fail ("nest == 8", "n_std.c", 902, __PRETTY_FUNCTION__));


    nest = 0;

# 1 "test/test-c/nest1.h" 1


    nest = 1;


# 1 "test/test-c/nest2.h" 1


    nest = 2;


# 1 "test/test-c/nest3.h" 1


    nest = 3;


# 1 "test/test-c/nest4.h" 1


    nest = 4;


# 1 "test/test-c/nest5.h" 1


    nest = 5;


# 1 "test/test-c/nest6.h" 1


    nest = 6;


# 1 "test/test-c/nest7.h" 1


    nest = 7;


# 1 "test/test-c/nest8.h" 1



    nest = 8;
# 6 "test/test-c/nest7.h" 2
# 6 "test/test-c/nest6.h" 2
# 6 "test/test-c/nest5.h" 2
# 6 "test/test-c/nest4.h" 2
# 6 "test/test-c/nest3.h" 2
# 6 "test/test-c/nest2.h" 2
# 6 "test/test-c/nest1.h" 2
# 907 "n_std.c" 2
 ((nest == 8) ? (void) (0) : __assert_fail ("nest == 8", "n_std.c", 907, __PRETTY_FUNCTION__));






    nest = 32;

    ((nest == 32) ? (void) (0) : __assert_fail ("nest == 32", "n_std.c", 916, __PRETTY_FUNCTION__));


    {
        char * extremely_long_string =
"123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567"







        ;
        ((strlen( extremely_long_string) == 507) ? (void) (0) : __assert_fail ("strlen( extremely_long_string) == 507", "n_std.c", 930, __PRETTY_FUNCTION__));
    }


    {
    int a123456789012345678901234567890 = 123450; int b123456789012345678901234567890 = 123451; int c123456789012345678901234567890 = 123452; int d123456789012345678901234567890 = 123453; int e123456789012345678901234567890 = 123454; int f123456789012345678901234567890 = 123455; int A123456789012345678901234567890 = 123456; int B123456789012345678901234567890 = 123457; int C123456789012345678901234567890 = 123458; int D1234567890123456789012 = 123459;
# 945 "n_std.c"
        ((a123456789012345678901234567890 == 123450 && D1234567890123456789012 == 123459) ? (void) (0) : __assert_fail ("a123456789012345678901234567890 == 123450 && D1234567890123456789012 == 123459", "n_std.c", 946, __PRETTY_FUNCTION__));

    }







# 1 "test/test-c/m1024.h" 1
# 955 "n_std.c" 2
 ((1) ? (void) (0) : __assert_fail ("1", "n_std.c", 955, __PRETTY_FUNCTION__));
}
