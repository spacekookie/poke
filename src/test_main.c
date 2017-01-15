#include <poke/pk.h>
#include <poke/pk_parse.h>

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#define TEST_PATH "/home/spacekookie/.ssh/config"


int main(void)
{
    printf("=== Welcome to poke ===\n");

    /* Create a context for a test path */
    // pk_dm_ctx ctx;
    pk_parse_ctx parser;

    // pk_dm_init(&ctx, TEST_PATH);

    /* Parse the ssh config */
    pk_parse_init(&parser, TEST_PATH);

    pk_parse_load(&parser);

    pk_parse_print(&parser);

    /* Clean up and quit */
    // pk_dm_free(&ctx);
    return 0;
}