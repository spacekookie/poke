#include <poke/pk_parse.h>
#include <stdio.h>
#include <string.h>
#include <malloc.h>


/*********************************************************************************************/


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


/*********************************************************************************************/


#define CHECK_CTX if(ctx == NULL) return PK_ERR_INVALID_PARAMS;
#define HOST_BUFFER_SIZE 256

/* All of the identifier fields */
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

#define STR_STARTS(src, check) strncmp(src, check, strlen(check))


#define PK_EXT          "#poke"
#define PK_UPDATED      "pk_updated"
#define PK_BLACKLIST    "pk_blacklisted"


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

    /** Open config and seek through for size */
    FILE *f = fopen(ctx->ssh_config, "r");
    fseek(f, 0, SEEK_END);
    size_t cfg_size = (size_t) ftell(f);
    fseek(f, 0, SEEK_SET);  //same as rewind(f);

    /** Buffer the config in an array */
    char str[cfg_size + 1];
    memset(str, 0, cfg_size + 1);
    fread(str, cfg_size, 1, f);
    fclose(f);

    /** Create some stack variables to parse with */
    char *pch;
    int ctr = 0;
    int host_ctr = -1;
    pk_parse_hst hosts[HOST_BUFFER_SIZE];
    memset(hosts, 0, sizeof(pk_parse_hst) * HOST_BUFFER_SIZE);

    /** Read first token and then iterate over tokens */
    pch = strtok (str,"\n");
    while (pch != NULL) {

        /** First trim the input for easy matching */
        char trimmed[strlen(pch) + 1];
        pk_string_trim(pch, trimmed);

        /** These two need to be in this order to avoid "Host" vs "HostName" conflicts */
        PK_DATA_WRITER(trimmed, hosts[host_ctr].hostname, HOST_NAME)

        /** Creating a new host entry with default values */
        if(STR_STARTS(trimmed, HOST_ID) == 0) {
            host_ctr++;
            strcpy(hosts[host_ctr].pk_updated, "-1");
            strcpy(hosts[host_ctr].pk_blacklist, "no");
            strcpy(hosts[host_ctr].port, "22");
            strcpy(hosts[host_ctr].id_only, "no");
        }

        /** If protected macros that assign values to current host */
        PK_DATA_WRITER(trimmed, hosts[host_ctr].host_id, HOST_ID)
        PK_DATA_WRITER(trimmed, hosts[host_ctr].id_only, ID_ONLY)
        PK_DATA_WRITER(trimmed, hosts[host_ctr].id_file, ID_FILE)
        PK_DATA_WRITER(trimmed, hosts[host_ctr].username, USER)
        PK_DATA_WRITER(trimmed, hosts[host_ctr].port, PORT)

        /** Check for our own #poke extentions */
        if(STR_STARTS(trimmed, PK_EXT) == 0) {

            /** Trim the poke extention away */
            char poke_extention[128];
            memset(poke_extention, 0, sizeof(char) * 128);
            strcpy(poke_extention, trimmed + strlen(PK_EXT));

            /** (Again) if protected MACROs that assign values to current host */
            PK_DATA_WRITER(poke_extention, hosts[host_ctr].pk_updated, PK_UPDATED);
            PK_DATA_WRITER(poke_extention, hosts[host_ctr].pk_blacklist, PK_BLACKLIST);
        }

        /* A label at the end to avoid any re-assignments through double if statements */
        end_value_write:
        pch = strtok (NULL, "\n");
    }

    int count = 0;
    int i;

    /** Assume we're successful and count hosts */
    for(i = 0; i < HOST_BUFFER_SIZE; i++) {
        if(strlen(hosts[i].hostname) == 0) continue;
        count++;
    }

    /** Then allocate a buffer of the correct size */
    ctx->hosts = (pk_parse_hst**) malloc(sizeof(pk_parse_hst*) * count);
    if(ctx->hosts == NULL) return PK_ERR_MALLOC_FAILED;

    /** For every host - alloc on heap and then copy pointer */
    for(i = 0; i < HOST_BUFFER_SIZE; i++) {
        if(strlen(hosts[i].hostname) == 0) continue;

        pk_parse_hst *host = (pk_parse_hst*) malloc(sizeof(pk_parse_hst) * 1);
        if(host == NULL) return PK_ERR_MALLOC_FAILED;

        /** Copy memoy from stack to heap */
        memcpy(host, &hosts[i], sizeof(pk_parse_hst));

        /** Then copy pointer to heap array */
        ctx->hosts[i] = host;
    }

    /** Return with glorious success */
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