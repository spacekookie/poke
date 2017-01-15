#include <poke.h>
#include <stdio.h>

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

    pk_parse_hst *host;
    int err = pk_parse_query(&parser, &host, "agamemnon");

    if(err == 0) {
        printf("'%s': %s@%s\n", host->host_id, host->username, host->hostname);
    }

    pk_parse_free(&parser);
    return 0;
}