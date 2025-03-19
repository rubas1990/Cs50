#include <cs50.h>
#include <stdio.h>
#include <string.h>


typedef struct
{
    string name;
    string number;
}
person;

int main(void)
{
    person people[3];
    people[0].name = "Ruben";
    people[0].number = "8442286100";

    people[1].name = "David";
    people[1].number = "8442044624";

    people[2].name = "Juan";
    people[2].number = "8441602895";


    string name = get_string("Name: ");
    for (int i = 0; i < 3; i++)
    {
        if (strcmp (people[i].name, name) == 0)
        {
            printf("Found: %s\n", people[i].number);
            return 0;
        }
    }
    printf("Not Found\n");
    return 1;
}
