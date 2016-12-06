#include <poke/pk.h>

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define CHECK_CTX if(ctx == NULL) return PK_ERR_INVALID_PARAMS;
#define BUFFER_SIZE 32768

#define PK_STR_STARTS(src, check) strncmp(src, check, strlen(check))
#define PK_DATA_WRITER(data, target, pattern) \
    { \
    if(PK_STR_STARTS(data, pattern) == 0) { \
        pk_string_parse(data, target, 128, pattern); \
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
int pk_parse_load(pk_parse_ctx *ctx, pk_config *cfg)
{
    CHECK_CTX

    /* Clear cfg pointer in case of error */
    memset(cfg, 0, sizeof(pk_config));

    /* Open the file and seek through it for length */
    FILE *f = fopen(ctx->ssh_path, "r");
    fseek(f, 0, SEEK_END);
    size_t cfg_size = (size_t) ftell(f);
    fseek(f, 0, SEEK_SET);

    /* Create a buffer of the correct size */
    char cfg_buf[cfg_size + 1];
    memset(cfg_buf, 0, cfg_size + 1);
    fread(cfg_buf, cfg_size, 1, f);
    fclose(f);

    /* Copy the raw data into a struct buffer for future reference */
    ctx->raw_data = (char*) malloc(sizeof(char) * cfg_size);
    if(ctx->raw_data == NULL) return PK_ERR_MALLOC_FAILED;
    strcpy(ctx->raw_data, cfg_buf);

    /* Scan through the config first once to find host count */
    char skim_buf[cfg_size + 1];
    memset(skim_buf, 0, cfg_size + 1);
    memcpy(skim_buf, cfg_buf, cfg_size + 1);

    size_t host_n = 0;
    char *temp;

    /* Skim through the config once to count Host entries */
    temp = strtok(skim_buf, "\n");
    while(temp != NULL) {

        /* Trim string for later matching */
        char trimmed[strlen(temp) + 1];
        pk_string_trim(temp, trimmed);

        /* Explicitly match "HostName" to avoid collisions */
        if(PK_STR_STARTS(trimmed, PK_PARSE_HOST_NAME) == 0) {
        } else if(PK_STR_STARTS(trimmed, PK_PARSE_HOST_ID) == 0) {
            host_n++;
        }

        temp = strtok(NULL, "\n");
    }

    /* Create some stack variables for future parsing */
    const char delims[] = "\n";
    pk_config buffer;
    char *pch;

    /* Buffer for current snippet (block or client) */
    pk_cfg_snippet *current = NULL;

    enum pk_parse_type { BLOCK, CLIENT };
    enum pk_parse_type curr_t = CLIENT;

    /* Allocate space for snippet list on the heap - might be resized */
    size_t snippets_size = sizeof(pk_cfg_snippet) * host_n * 2;
    buffer.snippets = (pk_cfg_snippet**) malloc(snippets_size);
    memset(buffer.snippets, 0, snippets_size);
    buffer.snip_max = snippets_size;

    /* Start parsing - first token */
    pch = strtok (cfg_buf, delims);

    /* Then iterate through the token list */
    while(pch != NULL) {

        /* Trim string for later matching */
        char trimmed[strlen(pch) + 1];
        pk_string_trim(pch, trimmed);

        /* These two need to be in this order to avoid "Host" vs "HostName" conflicts */
        PK_DATA_WRITER(trimmed, current->pl.client->hostname, PK_PARSE_HOST_NAME)

        /* For each new host fill in default data */
        if(PK_STR_STARTS(trimmed, PK_PARSE_HOST_ID) == 0) {

            /* Write pointer to data pointer list */
            pk_cfg_snippet *nhost = (pk_cfg_snippet*) malloc(sizeof(pk_cfg_snippet));
            nhost->pl.client = malloc(sizeof(pk_client));
            memset(nhost->pl.client, 0, sizeof(pk_client));

            /*
             * Make sure we have enough space for snippets. Especially
             * with recursive configs, this can be called often!
             */
            if(buffer.snip_curr + 1 >= buffer.snip_max) {
                buffer.snip_max += 4; // TODO: Pick a sane value
                buffer.snippets = realloc(buffer.snippets, buffer.snip_max);
            }

            /* Save the client in our snippet list */
            buffer.snippets[buffer.snip_curr++] = nhost;

            /* Override the current buffer */
            current = nhost;
            curr_t = CLIENT;
            nhost->type = PK_SNIP_CLIENT;

            /* Write some initial default values into the client */
            strcpy(current->pl.client->pk_updated, PK_DEFAULT_UPDATED);
            strcpy(current->pl.client->pk_blacklist, PK_DEFAULT_BLACKLIST);
            strcpy(current->pl.client->id_only, PK_DEFAULT_ID_ONLY);

            current->pl.client->port = atoi(PK_DEFAULT_PORT);

            PK_DATA_WRITER(trimmed, current->pl.client->host_id, PK_PARSE_HOST_ID)
        }

        if(PK_STR_STARTS(trimmed, PK_EXT) == 0) {

            /* First remove the known "#poke" indicator */
            char poke_ext[128];
            pk_string_parse(trimmed, poke_ext, 128, "#poke");

            /* Parse global extentions */
            if(PK_STR_STARTS(poke_ext, PK_VERSION) == 0) buffer.pk_version = atoi(poke_ext + strlen(PK_VERSION));
            if(PK_STR_STARTS(poke_ext, PK_UP_FREQ) == 0) buffer.pk_upfreq = atol(poke_ext + strlen(PK_UP_FREQ));

            /* Parse host specific extentions */
            if(PK_STR_STARTS(poke_ext, PK_BLACKLIST) == 0)
                pk_string_parse(poke_ext, current->pl.client->pk_blacklist, 128, PK_BLACKLIST);

            if(PK_STR_STARTS(poke_ext, PK_UPDATED) == 0)
                pk_string_parse(poke_ext, current->pl.client->pk_updated, 128, PK_UPDATED);
        }

        if(curr_t == CLIENT && current != NULL ) {
            PK_DATA_WRITER(trimmed, current->pl.client->id_only, PK_PARSE_ID_ONLY)
            PK_DATA_WRITER(trimmed, current->pl.client->id_file, PK_PARSE_ID_FILE)
            PK_DATA_WRITER(trimmed, current->pl.client->username, PK_PARSE_USER)

            /* Special case for numbers */
            if(PK_STR_STARTS(trimmed, PK_PARSE_PORT) == 0) {
                char port_number[32];
                pk_string_parse(trimmed, port_number, 32, PK_PARSE_PORT);

                /* Atoi asign port number and GOTO end */
                current->pl.client->port = atoi(port_number);
                goto end_value_write;
            }

            /****************/
        }

        /* Parse escape label to avoid assignment collisions */
        end_value_write:
        pch = strtok (NULL, delims);
    }

    /* Finally copy over our shallow data (heap data follows) */
    memcpy(cfg, &buffer, sizeof(pk_config));

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
int pk_parse_query(pk_config *cfg, pk_client **data, const char *host_id)
{
    *data = NULL;

    int i;
    for(i = 0; i < cfg->snip_curr; i++) {
        pk_cfg_snippet *s = cfg->snippets[i];

        if(s->type == PK_SNIP_CLIENT && strcmp(s->pl.client->host_id, host_id) == 0) {
            *data = s->pl.client;
            break;
        }
    }

    return PK_ERR_SUCCESS;
}


/** Free parser context from memory completely */
int pk_parse_free(pk_parse_ctx *ctx)
{
    CHECK_CTX

    free(ctx->ssh_path);
    free(ctx->raw_data);

    return PK_ERR_SUCCESS;
}


void pk_parse_printhst(pk_client *host)
{
    /* Do a quick check if we expect this host to be valid - Avoid info bleeding */
    if(host == NULL || host->host_id == NULL || host->hostname == NULL)
        return;

    /* Then (one after another) print out the data from the struct */
    printf("=== Host: %s ===\n", host->host_id);
    printf("\tHostName: %s\n", host->hostname);
    printf("\tUser: %s\n", host->username);
    printf("\tPort: %d\n", host->port);
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

