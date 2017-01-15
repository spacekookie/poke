#include <poke.h>
#include <stdio.h>

#define TEST_PATH "/home/spacekookie/.ssh/config"

int main(void)
{
    printf("=== Welcome to poke ===\n");

    /* Create a context for a test path */
    pk_parse_ctx parser;

    /* Parse the ssh config */
    pk_parse_init(&parser, TEST_PATH);

    pk_parse_load(&parser);

    pk_parse_hst *host;
    int err = pk_parse_query(&parser, &host, "agamemnon");

    if(err == 0) {
        printf("'%s': %s@%s\n", host->host_id, host->username, host->hostname);

        /* Initialise a new session to work with */
        pk_sm_ctx ctx;
        pk_sm_init(&ctx, host);

        pk_sm_start(&ctx);

        /* Free memory correctly */
        pk_sm_free(&ctx);
    }

    pk_parse_free(&parser);
    return 0;
}