#include <poke/pk.h>

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#define TEST_PATH "/home/spacekookie/.ssh/config"

int main(void)
{
    clock_t t1, t2;
    t1 = clock();

    pk_parse_ctx parser;
    pk_parse_init(&parser, TEST_PATH);

    /* Parse the config into context */
    pk_config *cfg;
    pk_parse_load(&parser, &cfg);

    /* Query parser set for hosts */
    pk_client *client;
    pk_parse_query(&parser, &client, "lonelyrobot");
    pk_parse_printhst(client);

    /* Free memory */
    pk_parse_free(&parser);

    t2 = clock();
    float diff = ((float)(t2 - t1) / 1000000.0F ) * 1000;
    printf("Program execution took %f milliseconds\n",diff);

    return 0;

}