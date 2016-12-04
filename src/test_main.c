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


/**
 * A simple utility function which extracts the value out of a key-value config pair.
 * It does so by copying the data into a payload string, without modifying the original
 * data provided.
 *
 * @param src
 * @param payload
 * @param payload_len
 * @param key
 */
void pk_string_parse(const char *src, char *payload, size_t payload_len, const char *key)
{
    /* First make sure memory is nice and clean */
    memset(payload, 0, payload_len);

    /* Ignore the <key> in the beginning of our string */
    strcpy(payload, src + strlen(key));
}


void print_host_struct(pk_parse_hst *host)
{
    printf("=== Host: %s ===\n", host->host_id);
    printf("\tHostName: %s\n", host->hostname);
    printf("\tUser: %s\n", host->username);
    printf("\tPort: %s\n", host->port);
    printf("\tID Only: %s\n", host->id_only);
    printf("\tID File: %s\n", host->id_file);

    size_t host_len = strlen(host->host_id) + 9 /* Beginning */ + 4 /* End */;
    int i;
    for(i = 0; i <= host_len; i++) {
        printf("=");
    }

    /* Then just add new lines */
    printf("\n\n");

}


int main(void)
{
    char str[] ="Host lonelyrobot\n"
                "#poke pk_updated 2382094332\n"
                "    User        spacekookie\n"
                "    HostName    5.45.106.146\n"
                "    IdentitiesOnly  no\n"
                "    IdentityFile    ~/.ssh/p_rsa\n"
                "    Port        22";

    char * pch;
    int ctr = 0;

    printf ("Splitting origin string into token stream...\n\n");

    int host_ctr = 0;
    pk_parse_hst hosts[2];
    memset(hosts, 0, sizeof(pk_parse_hst) * 2);

#define HOST_NAME   "HostName"
#define HOST_ID     "Host"
#define PORT        "Port"
#define USER        "User"
#define ID_ONLY     "IdentitiesOnly"
#define ID_FILE     "IdentityFile"

#define PK_DATA_WRITER(data, target, pattern) \
    { \
    if(STR_STARTS(data, pattern) == 0) { \
        pk_string_parse(data, target, 128, pattern); \
        /* printf("'%s' now: %s\n", #pattern, target); */ \
        goto end_value_write; \
    } }

    pch = strtok (str,"\n");
    while (pch != NULL) {
        // printf ("%d > %s\n", ctr++, pch);

        char trimmed[strlen(pch) + 1];
        pk_string_trim(pch, trimmed);

        /* These two need to be in this order to avoid "Host" vs "HostName" conflicts */
        PK_DATA_WRITER(trimmed, hosts[host_ctr].hostname, HOST_NAME)
        PK_DATA_WRITER(trimmed, hosts[host_ctr].host_id, HOST_ID)

        PK_DATA_WRITER(trimmed, hosts[host_ctr].id_only, ID_ONLY)
        PK_DATA_WRITER(trimmed, hosts[host_ctr].id_file, ID_FILE)
        PK_DATA_WRITER(trimmed, hosts[host_ctr].username, USER)
        PK_DATA_WRITER(trimmed, hosts[host_ctr].port, PORT)

        end_value_write:

        pch = strtok (NULL, "\n");
    }

    printf("Finishing up...looking at data\n");

    print_host_struct(&hosts[0]);

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