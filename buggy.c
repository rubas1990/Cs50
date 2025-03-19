#include <cs50.h>
#include <stdio.h>

void print_column (int height);

int main (void)
{
     int n = get_int("Height: ");
     print_column (n);
}

void print_column (int height)
{
    for (int i = 0 ; i <= height ; i++)
    {
         printf("#\n");
    }
}
