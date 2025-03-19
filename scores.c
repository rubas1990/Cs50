#include <cs50.h>
#include <stdio.h>

const int n =3;

float average(int length, int array[]);

int main (void)
{
    int score [n];
    for (int i = 0; i < n; i ++)
    {
        score[i] = get_int("Score: ");
    }
    printf("Average: %f\n", average(n, score));
}



float average(int length, int array[])
{
    int sum = 0;
    for (int i = 0; i < length; i++)
     {
        sum += array[i];
     }
      return sum / (float) length;
}
