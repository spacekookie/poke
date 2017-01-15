#include <poke/pk_parse.h>
#include <stdio.h>
#include <string.h>
#include <malloc.h>

#define CHECK_CTX if(ctx == NULL) return PK_ERR_INVALID_PARAMS;
#define BUFFER_SIZE 32768

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

    /** Create a clean buffer for \0 string */
    char buffer[BUFFER_SIZE];
    memset(buffer, 0, BUFFER_SIZE);

    FILE *config = fopen(ctx->ssh_path, "r");
    size_t cfg_len = 1;

    /** Copy the raw data into a struct buffer for future reference */
    ctx->raw_data = (char*) malloc(sizeof(char) * cfg_len);
    if(ctx->raw_data == NULL) return PK_ERR_MALLOC_FAILED;
    strcpy(ctx->raw_data, buffer);

    char str[] ="- This, a sample string.";
    char * pch;
    printf ("Splitting string \"%s\" into tokens:\n",str);
    pch = strtok (str," ,.-");

    while (pch != NULL) {
        printf ("%s\n",pch);
        pch = strtok (NULL, " ,.-");
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