#include <poke/pk.h>

#include <time.h>
#include <string.h>
#include <malloc.h>

#define CHECK_CTX \
    if(ctx == NULL) return PK_ERR_INVALID_PARAMS;


/** Initialises a context with everything that is required for it to work **/
int pk_dm_init(pk_sm_ctx *ctx, const char *cfg_pth)
{
    return PK_ERR_SUCCESS;
}

/** Safely frees a context from memory **/
int pk_dm_free(pk_sm_ctx *ctx)
{
    return PK_ERR_SUCCESS;
}