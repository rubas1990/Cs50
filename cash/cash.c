#include <cs50.h>
#include <stdio.h>

int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);

int main(void)
{
    int cents;
    do
    {
        cents = get_int("change owed: ");
    }

    while (cents < 0);

    // Calculate how many quarters you should give customer
    int quarters = calculate_quarters(cents);
    cents -= quarters * 25;

    int dimes = calculate_dimes(cents);
    cents -= dimes * 10;

    int nickels = calculate_nickels(cents);
    cents -= nickels * 5;

    int pennies = cents;

    // printf("%d\n",quarters);
    // printf("%d\n",dimes);
    // printf("%d\n",nickels);
    // printf("%d\n",pennies);
    int total = quarters + dimes + nickels + pennies;
    printf("%d\n", total);
}

int calculate_quarters(int cents)
{
    // Calculate how many quarters you should give customer
    int quarters = 0;
    while (cents >= 25)
    {
        quarters++;
        cents = cents - 25;
    }
    return quarters;
}

int calculate_dimes(int cents)
{
    // Calculate how many quarters you should give customer
    int dimes = 0;
    while (cents >= 10)
    {
        dimes++;
        cents = cents - 10;
    }
    return dimes;
}
int calculate_nickels(int cents)
{
    // Calculate how many quarters you should give customer
    int nickels = 0;
    while (cents >= 5)
    {
        nickels++;
        cents = cents - 5;
    }
    return nickels;
}
