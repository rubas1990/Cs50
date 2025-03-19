#include <stdio.h>
#include <stdint.h>

typedef unit8_t BYTE;

int main (int argc, char *argv[])
{
    FILE *src = fopen(argv[1], "rb");
    FILE *dst = fopen(argv[2], "wb");
                l

    BYTE b;

    while (fread(&b, sizeof(b), 1, src))
}
