#include <poke/pk.h>

#include <time.h>
#include <string.h>
#include <malloc.h>

#define CHECK_CTX \
    if(ctx == NULL) return PK_ERR_INVALID_PARAMS;

/** Initialise a new pk target with a hostname and username, kid can be null */
int pk_trgt_init(pk_trgt_ctx *ctx, const char *hst_n, const char *usr_n, char *kid)
{
    CHECK_CTX

    /* Check other non optional parameters */
    if(hst_n == NULL) return PK_ERR_INVALID_PARAMS;
    if(usr_n == NULL) return PK_ERR_INVALID_PARAMS;

    /* Clean our provided memory */
    memset(ctx, 0, sizeof(struct pk_trgt_ctx));

    ctx->hostname = (char*) malloc(sizeof(char) * strlen(hst_n));
    if(ctx->hostname == NULL) return PK_ERR_MALLOC_FAILED;
    strcpy(ctx->hostname, hst_n);

    ctx->username = (char*) malloc(sizeof(char) * strlen(usr_n));
    if(ctx->username == NULL) return PK_ERR_MALLOC_FAILED;
    strcpy(ctx->username, usr_n);

    /** Copy over the key if we have one */
    if(kid != NULL) {

        ctx->key_id = (char*) malloc(sizeof(char) * strlen(kid));
        if(ctx->key_id == NULL) return PK_ERR_MALLOC_FAILED;
        strcpy(ctx->key_id, kid);
    }

    /* Write down the current time */
    ctx->last_updated = time(0);

    /* Return with GOOD NEWS EVERYBODY! */
    return PK_ERR_SUCCESS;
}

/** Changes the key ID of the provided context and updates the access time */
int pk_trgt_update(pk_trgt_ctx *ctx, char *kid)
{
    CHECK_CTX

    /* Check other non-optional parameter */
    if(kid == NULL) return PK_ERR_INVALID_PARAMS;

    free(ctx->key_id);
    ctx->key_id = (char*) malloc(sizeof(char) * strlen(kid));
    if(ctx->key_id == NULL) return PK_ERR_MALLOC_FAILED;
    strcpy(ctx->key_id, kid);

    /* Finally update the key time */
    ctx->last_updated = time(0);

    return PK_ERR_SUCCESS;
}

/** Cleanly de-allocates all the resources from the context */
int pk_trgt_free(pk_trgt_ctx *ctx)
{
    CHECK_CTX

    free(ctx->key_id);
    free(ctx->username);
    free(ctx->hostname);
    free(ctx);

    return PK_ERR_SUCCESS;
}

/** Initialises a context with everything that is required for it to work **/
int pk_dm_init(pk_dm_ctx *ctx, const char *cfg_pth)
{
    return PK_ERR_SUCCESS;
}

/** Queries target information from the known hosts. Can replace ssh **/
int pk_dm_query(pk_dm_ctx *ctx, pk_trgt_ctx **trgt, const char *host)
{
    return PK_ERR_SUCCESS;
}

/** Safely frees a context from memory **/
int pk_dm_free(pk_dm_ctx *ctx)
{
    return PK_ERR_SUCCESS;
}