#include <poke/pk.h>
#include <poke/pk_parse.h>

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define TEST_PATH "/home/spacekookie/.ssh/config"
#define STR_STARTS(src, check) strncmp(src, check, strlen(check))

void pk_string_trim(char *src, char *dst)
{
    int s, d=0;
    for (s=0; src[s] != 0; s++)
        if (src[s] != ' ') {
            dst[d] = src[s];
            d++;
        }
    dst[d] = 0;
}


int main(void)
{
    char str[] ="Host lonelyrobot\n"
            "#poke pk_updated 2382094332\n"
            "    User        spacekookie\n"
            "    HostName    www.lonelyrobot.io\n"
            "    IdentitiesOnly  no\n"
            "    IdentityFile    ~/.ssh/p_rsa\n"
            "    Port        22";

    char * pch;
    int ctr = 0;

    printf ("Splitting origin string into token stream...\n\n");

    int host_ctr = 0;
    pk_parse_hst hosts[2];
    memset(hosts, 0, sizeof(pk_parse_hst) * 2);

    pch = strtok (str,"\n");
    while (pch != NULL) {
        char trimmed[strlen(pch) + 1];
        pk_string_trim(pch, trimmed);

        if(STR_STARTS(trimmed, "Host") == 0) {
            char hostname[strlen(trimmed)];
            memset(hostname, 0, strlen(trimmed));

            /* Ignore the "Host" in the beginning of our string */
            strcpy(hostname, trimmed + 4);

            strcpy(hosts[host_ctr].hostname, hostname);
            printf("Selected host name: '%s'\n\n", hosts[host_ctr].hostname);
        }

        printf ("%d > %s\n", ctr++, pch);
        pch = strtok (NULL, "\n");
    }
    return 0;

    printf("=== Welcome to poke ===\n");

    /* Create a context for a test path */
    pk_dm_ctx ctx;
    pk_parse_ctx parser;

    pk_dm_init(&ctx, TEST_PATH);

    /* Parse the ssh config */
    pk_parse_init(&parser, TEST_PATH);

    /* Clean up and quit */
    pk_dm_free(&ctx);
    return 0;
}