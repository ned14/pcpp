# 19 "test/test-c/n_std.c"





#define sub( x, y)      (x - y)
#define str( a)         # a
#define xstr( a)        str( a)
#define glue( a, b)     a ## b
#define xglue( a, b)    glue( a, b)

void    n_1( void);
void    n_2( void);
void    n_3( void);
void    n_4( void);
void    n_5( void);
void    n_6( void);
void    n_7( void);
void    n_9( void);
void    n_10( void);
void    n_11( void);
void    n_12( void);
void    n_13( void);
void    n_13_5( void);
void    n_13_7( void);
void    n_13_8( void);
void    n_13_13( void);
void    n_15( void);
void    n_18( void);
void    n_19( void);
void    n_20( void);
void    n_21( void);
void    n_22( void);
void    n_23( void);
void    n_24( void);
void    n_25( void);
void    n_26( void);
void    n_27( void);
void    n_28( void);
void    n_29( void);
void    n_30( void);
void    n_32( void);
void    n_37( void);

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
    return  0;
}

char    quasi_trigraph[] = { '?', '?', ' ', '?', '?', '?', ' '
            , '?', '?', '%', ' ', '?', '?', '^', ' ', '?', '#', '\0' };

void    n_2( void)

{
    int     ab = 1, cd = 2, ef = 3, abcde = 5;



#define FUNC( a, b, c)          a + b + c

    assert( FUNC( ab, cd, ef) == 6);




#define FUNC( a, b      , c)                a + b               + c



    assert (FUNC( ab, cd, ef) == 6);


    assert (strcmp( "abcde", "abcde") == 0);



    assert( abcde == 5);


}

void    n_3( void)

{
    int     abcd = 4;


assert( strcmp( str( abc de), "abc de") == 0);
# 156 "test/test-c/n_std.c"
    assert( abcd == 4);
}

void    n_4( void)

{

%: define  stringize( a)    %: a

    assert( strcmp( stringize( abc), "abc") == 0);


    assert( strcmp( stringize( <:), "<" ":") == 0);
}

void    n_5( void)



{
    int     abcde = 5;


    assert( abcde == 5);
}
# 190 "test/test-c/n_std.c"
void    n_6( void)

{
    int     abc = 3;

    assert( isalpha( 'a'));
# 200 "test/test-c/n_std.c"
    assert( abc == 3);
# 205 "test/test-c/n_std.c"
    assert( abc == 3);
}

void    n_7( void)

{

# 1234 "cpp"
    assert( 1234 == 1234);
    assert( strcmp( "cpp", "cpp") == 0);


# 2345 "cpp"
    assert( 2345 == 2345);
    assert( strcmp( "cpp", "cpp") == 0);



# 1234 "n_7.c"
    assert( 1234 == 1234);
    assert( strcmp( "n_7.c", "n_7.c") == 0);
}


# 230 "n_std.c"

void    n_9( void)

{


#pragma once
#pragma who knows ?
}

void    n_10( void)

{
# 250 "test/test-c/n_std.c"
    assert( 1);
# 263 "test/test-c/n_std.c"
}

void    n_11( void)

{
    int     abc = 1, a = 0;
# 276 "test/test-c/n_std.c"
    assert( abc);


    assert( abc);
# 291 "test/test-c/n_std.c"
}





void    n_12( void)

{


    fputs( "Bad evaluation of long.\n", stderr);


    fputs( "Bad evaluation of long.\n", stderr);
# 337 "test/test-c/n_std.c"
}

void    n_13( void)
# 355 "test/test-c/n_std.c"
{
# 368 "test/test-c/n_std.c"
    fputs( "Bad arithmetic of ||, && operators.\n", stderr);






}

void    n_13_5( void)

{







    fputs( "Bad arithmetic conversion.\n", stderr);



    fputs( "Bad arithmetic conversion.\n", stderr);





    fputs( "Bad arithmetic conversion.\n", stderr);

}

void    n_13_7( void)

{
# 418 "test/test-c/n_std.c"
}

void    n_13_8( void)

{
# 451 "test/test-c/n_std.c"
}

void    n_13_13( void)

{
# 478 "test/test-c/n_std.c"
}

void    n_15( void)

{



    assert( 1);
# 495 "test/test-c/n_std.c"
    assert( 1);

}

void    n_18( void)



#define FTN_LIKE(a)     ( a )
{
    int     c = 3;


    assert( (1-1) == 0);





    assert( FTN_LIKE( c) == 3);


#define STR( n1, n2)    "n1:n2"
    assert( strcmp( STR( 1, 2), "n1:n2") == 0);
}

void    n_19( void)

{
    int     c = 1;





#define FTN_LIKE( a     )(                             a )


    assert( FTN_LIKE( c) == 1);
}

void    n_20( void)

{


    double   fl;
    assert( sizeof fl == sizeof (double));
}

void    n_21( void)

{
    int     a = 1, x = 2, y = -3;



    assert( ---a == -1);



#define sub( a, b)  a-b


    assert( sub( x, -y) == -1);
}

void    n_22( void)

{



    assert( strcmp( xstr( 12E+1), "12E+EXP") == 0);


    assert( strcmp( xstr( .2e-1), ".2e-EXP") == 0);



    assert( strcmp( xstr( 12+1), "12+1") == 0);
}

void    n_23( void)

{
    int     xy = 1;


    assert( glue( x, y) == 1);




    assert( xglue( .12e+, 2) == 12.0);
}

void    n_24( void)

{

    assert( strcmp( str( a+b), "a+b") == 0);



assert( strcmp( str(    ab      +
        cd  ), "ab + cd") == 0);



    assert( strcmp( str( '"' + "' \""), "'\"' + \"' \\\"\"") == 0);



    assert( strcmp( str( "abc"), "\"abc\"") == 0);




#define f(a)        a
    assert( strcmp( xstr( x-f(y)), "x-y") == 0);
}

void    n_25( void)



{
    int     a = 1, b = 2, abc = 3, MACRO_0MACRO_1 = 2;


#define sub( x, y)      (x - y)



    assert( sub( a,b, 1) == 1);


    assert( sub( , a) == -1);


    assert( xglue( glue( a, b), c) == 3);


    assert( glue( 0, 1) == 2);


    assert( strcmp( str( ), "ZERO_TOKEN") == 0);
}
# 660 "test/test-c/n_std.c"
int     f( int a)
{
    return  a;
}

int     g( int a)
{
    return  a * 2;
}


void    n_26( void)

{
    int     x = 1;
    int     AB = 1;
    int     Z[1];
    Z[0] = 1;




    assert( Z[0] == 1);





    assert( AB == 1);



#define f(a)    a + f(a)
    assert( f( x) == 2);



#define g(a)    a + h( a)
#define h(a)    a + g( a)
    assert( g( x) == 4);



    assert( f( Z[0]) == 2);
}

void    n_27( void)




{
    int     a = 1, b = 2, c, m = 1, n = 2;
# 723 "test/test-c/n_std.c"
    assert( 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 == 36);


#define FUNC4( a, b)    FUNC3( a, b) + NEST4
#define FUNC3( a, b)    FUNC2( a, b) + NEST3
#define FUNC2( a, b)    FUNC1( a, b) + NEST2
#define FUNC1( a, b)    (a) + (b)
    assert( FUNC4( 1, NEST1 + 2) == 23);


    assert( glue( MACRO_, 1) == 1);


#define math( op, a, b) op( (a), (b))



    assert( math( sub, a, b) == -1);


    c = sub( a,b );
    assert( c == -1);




#define n( a)   a 
    assert( n( n) == 2);
}

void    n_28( void)


{
    char *  date = "Feb 10 2017";


    assert( strcmp( "n_std.c", "n_std.c") == 0);


    assert( 763 == 779);


    assert( strlen( "Feb 10 2017") == 11);
    assert( date[ 4] != '0');


    assert( strlen( "17:51:53") == 8);


    assert( 1);


    assert( 199901L >= 199409L);




{
    char *  file = "test/test-c/line.h";
    file += strlen( file) - 6;
    assert( 6 == 6 && strcmp( file, "line.h") == 0);
}
# 780 "test/test-c/n_std.c"
}

void    n_29( void)

{
    int     DEFINED = 1;




    assert( DEFINED == 1);



}

void    n_30( void)






{

#define FUNC( a, b, c)      a + b + c

    int     a = 1, b = 2, c = 3;


    assert
    (
        FUNC
        (
            a,
            b,
            c
        )
        == 6
    );
}

void    n_32( void)

{


    fputs( "Bad evaluation of octal escape sequence.\n", stderr);






}

void    n_37( void)

{



#define glue31(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,A,B,C,D,E)       a##b##c##d##e##f##g##h##i##j##k##l##m##n##o##p##q##r##s##t##u##v##w##x##y##z##A##B##C##D##E


    int     ABCDEFGHIJKLMNOPQRSTUVWXYZabcde = 31;
    int     ABCDEFGHIJKLMNOPQRSTUVWXYZabcd_ = 30;
    int     nest = 0;


    assert(
        glue31( A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R
            , S, T, U, V, W, X, -y, Z[0], a, b, c, d, e)
        == 31);



    assert( ABCDEFGHIJKLMNOPQRSTUVWXYZabcd_ == 30);


    nest = 0;
# 877 "test/test-c/n_std.c"
                                nest = 8;
# 886 "test/test-c/n_std.c"
    assert( nest == 8);


    nest = 0;


    nest = 1;



    nest = 2;



    nest = 3;



    nest = 4;



    nest = 5;



    nest = 6;



    nest = 7;




    nest = 8;
# 891 "test/test-c/n_std.c"
    assert( nest == 8);






    nest = 32;

    assert( nest == 32);


    {
        char *  extremely_long_string =
"123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567"
# 913 "test/test-c/n_std.c"
        ;
        assert( strlen( extremely_long_string) == 507);
    }


    {
    int a123456789012345678901234567890 = 123450;       int b123456789012345678901234567890 = 123451;       int c123456789012345678901234567890 = 123452;       int d123456789012345678901234567890 = 123453;       int e123456789012345678901234567890 = 123454;       int f123456789012345678901234567890 = 123455;       int A123456789012345678901234567890 = 123456;       int B123456789012345678901234567890 = 123457;       int C123456789012345678901234567890 = 123458;       int D1234567890123456789012 = 123459;
# 929 "test/test-c/n_std.c"
        assert( a123456789012345678901234567890 == 123450
            && D1234567890123456789012 == 123459);
    }
# 939 "test/test-c/n_std.c"
    assert( 1);
}

