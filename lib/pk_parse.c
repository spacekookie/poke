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
    char skim_buf[cfg_size + 1];
    memset(skim_buf, 0, cfg_size + 1);
    memcpy(skim_buf, buffer, cfg_size + 1);

    size_t host_n = 0;
    char *temp;

    /* Skim through the config once to count Host entries */
    temp = strtok(skim_buf, "\n");
    while(temp != NULL) {

        /* Trim string for later matching */
        char trimmed[strlen(temp) + 1];
        pk_string_trim(temp, trimmed);

        /* Explicitly match "HostName" to avoid collisions */
        if(PK_STR_STARTS(trimmed, HOST_NAME) == 0) {
        } else if(PK_STR_STARTS(trimmed, HOST_ID) == 0) {
            host_n++;
        }

        temp = strtok(NULL, "\n");
    }

    /* Create some stack variables for future parsing */
    const char delims[] = "\n";
    pk_parse_hst hosts[host_n];
    int host_ctr = -1;
    char *pch;

    /* Start parsing - first token */
    pch = strtok (buffer, delims);

    /* Then iterate through the token list */
    while(pch != NULL) {

        /* Trim string for later matching */
        char trimmed[strlen(pch) + 1];
        pk_string_trim(pch, trimmed);

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

        PK_DATA_WRITER(trimmed, hosts[host_ctr].id_only, ID_ONLY)
        PK_DATA_WRITER(trimmed, hosts[host_ctr].id_file, ID_FILE)
        PK_DATA_WRITER(trimmed, hosts[host_ctr].username, USER)
        PK_DATA_WRITER(trimmed, hosts[host_ctr].port, PORT)


        /* Parse escape label to avoid assignment collisions */
        end_value_write:
        pch = strtok (NULL, delims);
    }

    /* Allocate enough space for host storage and copy data */
    ctx->hosts = (pk_parse_hst**) malloc(sizeof(pk_parse_hst*) * (host_n + 6));
    if(ctx->hosts == NULL) return PK_ERR_MALLOC_FAILED;
    memset(ctx->hosts, 0, sizeof(pk_parse_hst*) * (host_n + 6));
    ctx->hsize = (int) host_n + 6;

    /* Allocate each host on heap */
    int i;
    for(i = 0; i < host_n; i++) {

        /* Allocate heap memory and clean it */
        pk_parse_hst *host = (pk_parse_hst*) malloc(sizeof(pk_parse_hst) * 1);
        if(host == NULL) return PK_ERR_MALLOC_FAILED;
        memset(host, 0, sizeof(pk_parse_hst));

        /* Copy over contents to heap memory */
        memcpy(host, &hosts[i], sizeof(pk_parse_hst));

        /* Write pointer to data pointer list */
        ctx->hosts[i] = host;
    }

    ctx->hused = i;
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
int pk_parse_query(pk_parse_ctx *ctx, pk_parse_hst **data, const char *host_id)
{
    CHECK_CTX

    int i;
    for(i = 0; i < ctx->hused; i++) {
        pk_parse_hst *host = ctx->hosts[i];

        if(strcmp(host->host_id, host_id) == 0) {
            (*data) = host;
            break;
        }
    }

    return PK_ERR_SUCCESS;
}


/** Free parser context from memory completely */
int pk_parse_free(pk_parse_ctx *ctx)
{
    CHECK_CTX


    int i;
    for(i = 0; i < ctx->hsize; i++) {
        free(ctx->hosts[i]);
    }

    free(ctx->ssh_path);
    free(ctx->raw_data);
    free(ctx->hosts);

    return PK_ERR_SUCCESS;
}


void pk_parse_printhst(pk_parse_hst *host)
{
    /* Do a quick check if we expect this host to be valid - Avoid info bleeding */
    if(host == NULL || host->host_id == NULL || host->hostname == NULL)
        return;

    /* Then (one after another) print out the data from the struct */
    printf("=== Host: %s ===\n", host->host_id);
    printf("\tHostName: %s\n", host->hostname);
    printf("\tUser: %s\n", host->username);
    printf("\tPort: %s\n", host->port);
    printf("\tID Only: %s\n", host->id_only);
    printf("\tID File: %s\n", host->id_file);
    printf("\n");
    printf("\tPK Updated: %s\n", host->pk_updated);
    printf("\tPK Blacklisted: %s\n", host->pk_blacklist);

    /* Fill in '=' symbols to make it pretty */
    size_t host_len = strlen(host->host_id) + 9 /* Beginning */ + 4 /* End */;
    int i;
    for(i = 0; i <= host_len; i++) {
        printf("=");
    }

    /* Then just add new lines */
    printf("\n\n");
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

