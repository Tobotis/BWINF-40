#include <stdio.h>

int main()
{
    long long a = 100234555;
    long long b = 22333335;
    long long c = 341500;
    for (long long i = 1; i <= 90000000000; i++)
    {
        if (i % 100000000 == 0)
        {
            printf("%lld\n", i);
        }
        a = a - (b % 2);
        b = b - (c % 2);
    }
    printf("Sum is %lld\n", a + b);
    return 0;
}