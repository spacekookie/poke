#include <poke.h>

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


int count_lines(const char *buffer)
{
    int i;
    int count = 0;

    for(i = 0; i < strlen(buffer); i++) {
        char c = buffer[i];
        if(strcmp(&c, "\n") == 0) count++;
    }

    return count;
}


void append_char(char *buffer, int *ctr, char c)
{
    sprintf(buffer + (*ctr), "%c", c);
}


void pk_expand_newlines(char buffer[], const char *source)
{
    int i;
    int insert = 0;

    for(i = 0; i < strlen(source); i++) {
        char c = source[i];

        /** We look-ahead of +1 to see if newline */
        if(c == '\n') {
            sprintf(buffer + insert, " \n");
            insert += 2;

            continue;
        }

        sprintf(buffer + insert, "%c", c);
        insert++;
    }

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

    /** Allocate a new dtree root node */
    dt_err err = dtree_malloc(&ctx->struc);
    if(err) return PK_ERR_MALLOC_FAILED;

    return PK_ERR_SUCCESS;
}

/** Load the config to RAM and store a series of tokens to work on */
int pk_parse_load(pk_parse_ctx *ctx)
{
    CHECK_CTX

    /** Open config and seek through for size */
    FILE *f = fopen(ctx->ssh_path, "r");
    fseek(f, 0, SEEK_END);
    size_t cfg_size = (size_t) ftell(f);
    fseek(f, 0, SEEK_SET);  //same as rewind(f);

    /** Buffer the config in an array */
    char tmp[cfg_size + 1];
    memset(tmp, 0, cfg_size + 1);
    fread(tmp, cfg_size, 1, f);
    fclose(f);

    /** Expand buffer so newlines aren't empty */
    int lines = count_lines(tmp);
    char str[cfg_size + 1 + lines];
    memset(str, 0, cfg_size + 1 + lines);
    pk_expand_newlines(str, tmp);


    /** Create some stack variables to parse with */
    char *pch;
    int position = 0;
    int host_ctr = -1;
    pk_parse_hst hosts[HOST_BUFFER_SIZE];
    memset(hosts, 0, sizeof(pk_parse_hst) * HOST_BUFFER_SIZE);

    /** Read first token and then iterate over tokens */
    pch = strtok (str,"\n");
    while (pch != NULL) {

        /** Update line position */
        position += 1;

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

            /** Save new position and hostname as node list (pair) child */
            dtree *node;
            dt_err err;

            err = dtree_addlist(ctx->struc, &node);
            if(err) return PK_ERR_MALLOC_FAILED;

            dtree *key, *val;
            err = dtree_addpair(node, &key, &val);
            if(err) return PK_ERR_GENERROR;


            char literal[128];
            memset(literal, 0, sizeof(char) * 128);
            pk_string_parse(trimmed, literal, 128, HOST_ID);

            err = dtree_addliteral(key, literal);
            if(err) return PK_ERR_GENERROR;

            err = dtree_addnumeral(val, position);
            if(err) return PK_ERR_GENERROR;
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
    ctx->hosts = (pk_parse_hst*) malloc(sizeof(pk_parse_hst) * count);
    if(ctx->hosts == NULL) return PK_ERR_MALLOC_FAILED;

    /** Copy array over and number of items */
    memcpy(ctx->hosts, hosts, sizeof(pk_parse_hst) * count);
    ctx->count = count;

    /** Return with glorious success */
    return PK_ERR_SUCCESS;
}

/** Remove the store token stream and list from memory */
int pk_parse_dump(pk_parse_ctx *ctx)
{
    CHECK_CTX

    free(ctx->hosts);

    /** Dump all child data without removing the root node */
    dt_err err = dtree_resettype(ctx->struc);
    if(err) return PK_ERR_GENERROR;

    return PK_ERR_SUCCESS;
}

/** Find information in the token stream for access */
int pk_parse_query(pk_parse_ctx *ctx, pk_parse_hst **data, const char *hostname)
{
    CHECK_CTX

    int i;

    /** For every host - alloc on heap and then copy pointer */
    for(i = 0; i < ctx->count; i++) {

        // printf("%s VS %s\n", hostname, ctx->hosts[i].host_id);

        /** Check if the hostname for our entry is correct */
        if(strcmp(ctx->hosts[i].host_id, hostname) == 0) {
            *data = &ctx->hosts[i];
            return PK_ERR_SUCCESS;

        }
    }

    return PK_ERR_NOT_FOUND;
}

int pk_parse_print(pk_parse_ctx *ctx)
{

    int i;
    for(i = 0; i < ctx->count; i++) {
        if(strlen(ctx->hosts[i].hostname) == 0) continue;
        print_host_struct(&ctx->hosts[i]);
    }

    return PK_ERR_SUCCESS;
}

/** Free parser context from memory completely */
int pk_parse_free(pk_parse_ctx *ctx)
{
    CHECK_CTX

    /** Free the dtree node structure first */
    dt_err err = dtree_free(ctx->struc);
    if(err) return PK_ERR_GENERROR;

    free(ctx->ssh_path);
    free(ctx->hosts);

    return PK_ERR_SUCCESS;
}