#include <poke/pk.h>
#include <poke/pk_parse.h>

#include <stdlib.h>
#include <stdio.h>

#define TEST_PATH "/home/spacekookie/.ssh/config"

int main(void)
{
    printf("=== Welcome to poke ===\n");

    /* Create a context for a test path */
    pk_dm_ctx ctx;
    pk_dm_init(&ctx, TEST_PATH);

    /* Parse the ssh config */


    /* Clean up and quit */
    pk_dm_free(&ctx);
    return 0;
}