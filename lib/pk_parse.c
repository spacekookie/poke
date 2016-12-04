#include <poke/pk_parse.h>
#include <stdio.h>
#include <string.h>

#define CHECK_CTX if(ctx == NULL) return PK_ERR_INVALID_PARAMS;

/** Prepare a parser context for a config file */
int pk_parse_init(pk_parse_ctx *ctx, const char *path)
{
  CHECK_CTX

  memset(ctx, 0, sizeof(pk_parse_ctx));
  
  ctx->ssh_path = (char*) malloc(sizeof(char) * strlen(path));
  if(ctx->ssh_path == NULL) return PK_ERR_MALLOC_FAILED,
  strcpy(ctx->ssh_path, path);

  return PK_ERR_SUCCESS;
}

/** Load the config to RAM and store a series of tokens to work on */
int pk_parse_load(pk_parse_ctx *ctx)
{
  CHECK_CTX

  

  return PK_ERR_SUCCESS;
}

/** Remove the store token stream and list from memory */
int pk_parse_dump(pk_parse_ctx *ctx)
{
  CHECK_CTX

  

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

  

  return PK_ERR_SUCCESS;  
}