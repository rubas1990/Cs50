#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int only_digits(string s);

int rotate(char c, int n);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    if (!only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    int key = atoi(argv[1]);

    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");

    for (int i = 0; i < strlen(plaintext); i++)
    {
        printf("%c", rotate(plaintext[i], key));
    }

    printf("\n");

    return 0;
}

int rotate(char c, int n)
{
    if (isalpha(c))
    {
        if (isupper(c))
        {
            return (c - 'A' + n) % 26 + 'A';
        }
        else
        {
            return (c - 'a' + n) % 26 + 'a';
        }
    }
    else
    {
        return c;
    }
}

int only_digits(string s)
{
    for (int i = 0; i < strlen(s); i++)
    {
        if (!isdigit(s[i]))
        {
            return 0;
        }
    }

    return 1;
}
