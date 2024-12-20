#define MODIFY(x) x
#define FOO MODIFY(FOO)
#define DO_FOO FOO(42);

DO_FOO
