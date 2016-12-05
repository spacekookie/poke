#include <poke/pk.h>
#include <poke/pk_parse.h>

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

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
    printf("\n");
    printf("\tPK Updated: %s\n", host->pk_updated);
    printf("\tPK Blacklisted: %s\n", host->pk_blacklist);

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
    clock_t t1, t2;
    t1 = clock();

    FILE *f = fopen(TEST_PATH, "r");
    fseek(f, 0, SEEK_END);
    size_t cfg_size = (size_t) ftell(f);
    fseek(f, 0, SEEK_SET);  //same as rewind(f);

    char str[cfg_size + 1];
    memset(str, 0, cfg_size + 1);
    fread(str, cfg_size, 1, f);
    fclose(f);

    char *pch;
    int ctr = 0;
    printf ("Splitting origin string into token stream...\n\n");

    int host_ctr = -1;
    pk_parse_hst hosts[128];
    memset(hosts, 0, sizeof(pk_parse_hst) * 128);

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

        if(STR_STARTS(trimmed, HOST_ID) == 0) {
            host_ctr++;
            strcpy(hosts[host_ctr].pk_updated, "-1");
            strcpy(hosts[host_ctr].pk_blacklist, "no");
            strcpy(hosts[host_ctr].port, "22");
            strcpy(hosts[host_ctr].id_only, "no");
        }
        PK_DATA_WRITER(trimmed, hosts[host_ctr].host_id, HOST_ID)

        PK_DATA_WRITER(trimmed, hosts[host_ctr].id_only, ID_ONLY)
        PK_DATA_WRITER(trimmed, hosts[host_ctr].id_file, ID_FILE)
        PK_DATA_WRITER(trimmed, hosts[host_ctr].username, USER)
        PK_DATA_WRITER(trimmed, hosts[host_ctr].port, PORT)

        /** Check for our own #poke extentions */
        if(STR_STARTS(trimmed, PK_EXT) == 0) {

            char poke_extention[128];
            memset(poke_extention, 0, sizeof(char) * 128);
            strcpy(poke_extention, trimmed + strlen(PK_EXT));

            PK_DATA_WRITER(poke_extention, hosts[host_ctr].pk_updated, PK_UPDATED);
            PK_DATA_WRITER(poke_extention, hosts[host_ctr].pk_blacklist, PK_BLACKLIST);
        }

        /* A label at the end to avoid any re-assignments through double if statements */
        end_value_write:
        pch = strtok (NULL, "\n");
    }

    printf("Finishing up...looking at data\n");

    int i;
    for(i = 0; i < 128; i++) {
        if(strlen(hosts[i].hostname) == 0) continue;
        print_host_struct(&hosts[i]);
    }

    t2 = clock();
    float diff = ((float)(t2 - t1) / 1000000.0F ) * 1000;
    printf("Program execution took %f milliseconds\n",diff);

    return 0;

}