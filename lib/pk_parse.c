#include <poke/pk_parse.h>
#include <stdio.h>
#include <string.h>
#include <malloc.h>

#define CHECK_CTX if(ctx == NULL) return PK_ERR_INVALID_PARAMS;
#define BUFFER_SIZE 32768

#define PK_STR_STARTS(src, check) strncmp(src, check, strlen(check))
#define PK_DATA_WRITER(data, target, pattern) \
    { \
    if(PK_STR_STARTS(data, pattern) == 0) { \
        pk_string_parse(data, target, 128, pattern); \
        /* printf("'%s' now: %s\n", #pattern, target); */ \
        goto end_value_write; \
    } }

/** Forward declare function headers for easier to read file **/
void pk_string_trim(char *src, char *dst);
void pk_string_parse(const char *src, char *payload, size_t payload_len, const char *key);

/** Prepare a parser context for a config file */
int pk_parse_init(pk_parse_ctx *ctx, const char *path)
{
    CHECK_CTX

    memset(ctx, 0, sizeof(pk_parse_ctx));

    ctx->ssh_path = (char*) malloc(sizeof(char) * strlen(path));
    if(ctx->ssh_path == NULL) return PK_ERR_MALLOC_FAILED;
    strcpy(ctx->ssh_path, path);

    return PK_ERR_SUCCESS;
}

/** Load the config to RAM and store a series of tokens to work on */
int pk_parse_load(pk_parse_ctx *ctx)
{
    CHECK_CTX


    /* Open the file and seek through it for length */
    FILE *f = fopen(ctx->ssh_path, "r");
    fseek(f, 0, SEEK_END);
    size_t cfg_size = (size_t) ftell(f);
    fseek(f, 0, SEEK_SET);

    /* Create a buffer of the correct size */
    char buffer[cfg_size + 1];
    memset(buffer, 0, cfg_size + 1);
    fread(buffer, cfg_size, 1, f);
    fclose(f);

    /* Copy the raw data into a struct buffer for future reference */
    ctx->raw_data = (char*) malloc(sizeof(char) * cfg_size);
    if(ctx->raw_data == NULL) return PK_ERR_MALLOC_FAILED;
    strcpy(ctx->raw_data, buffer);

    /* Scan through the config first once to find host count */
    size_t host_n = 0;
    char *temp;

    /* Skim through the config once to count Host entries */
    temp = strtok (buffer, "\n");
    while(temp != NULL) {

        /* Trim string for later matching */
        char trimmed[strlen(temp) + 1];
        pk_string_trim(temp, trimmed);

        /* Explicitly match "HostName" to avoid collisions */
        if(PK_STR_STARTS(trimmed, HOST_NAME) == 0) {
        } else if(PK_STR_STARTS(trimmed, HOST_ID)) {
            host_n++;
        }

        temp = strtok(NULL, "\n");
    }

    /* Create some stack variables for future parsing */
    const char delims[] = "\n";
    pk_parse_hst hosts[host_n];
    unsigned int host_ctr = 0;
    char *pch;

    /* Start parsing - first token */
    pch = strtok (buffer, delims);

    /* Then iterate through the token list */
    while(pch != NULL) {

        /* Trim string for later matching */
        char trimmed[strlen(pch) + 1];
        pk_string_trim(pch, trimmed);

        /* Store a reference pointer to the host */
        pk_parse_hst *curr = &hosts[host_ctr];

        /* These two need to be in this order to avoid "Host" vs "HostName" conflicts */
        PK_DATA_WRITER(trimmed, hosts[host_ctr].hostname, HOST_NAME)

        /* For each new host fill in default data */
        if(PK_STR_STARTS(trimmed, HOST_ID) == 0) {

            /* Increment host buffer counter */
            host_ctr++;

            strcpy(hosts[host_ctr].pk_updated, PK_DEFAULT_UPDATED);
            strcpy(hosts[host_ctr].pk_blacklist, PK_DEFAULT_BLACKLIST);
            strcpy(hosts[host_ctr].port, PK_DEFAULT_PORT);
            strcpy(hosts[host_ctr].id_only, PK_DEFAULT_ID_ONLY);

            /* Finally write host name to new host */
            PK_DATA_WRITER(trimmed, hosts[host_ctr].host_id, HOST_ID)
        }

        /* Parse escape label to avoid assignment collisions */
        end_value_write:
        pch = strtok (NULL, "\n");
    }

    return PK_ERR_SUCCESS;
}

/** Remove the store token stream and list from memory */
int pk_parse_dump(pk_parse_ctx *ctx)
{
    CHECK_CTX

    if(ctx->raw_data) free(ctx->raw_data);

    return PK_ERR_SUCCESS;
}

/** Find information in the token stream for access */
int pk_parse_query(pk_parse_ctx *ctx, pk_parse_hst **data, const char *hostname)
{
    CHECK_CTX

    return PK_ERR_SUCCESS;
}

/** Free parser context from memory completely */
int pk_parse_free(pk_parse_ctx *ctx)
{
    CHECK_CTX

    if(ctx->raw_data) free(ctx->raw_data);

    int i;
    for(i = 0; i < ctx->hused; i++) {
        pk_parse_hst *hst = ctx->hosts[i];
        free(hst);
    }

    free(ctx->hosts);
    free(ctx);

    return PK_ERR_SUCCESS;
}

/************************************************************************************************/

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