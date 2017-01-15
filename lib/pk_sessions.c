#include <poke.h>

#include <string.h>

#include <time.h>
#include <stdio.h>
#include <malloc.h>
#include <errno.h>

#define CHECK_CTX \
    if(ctx == NULL) return PK_ERR_INVALID_PARAMS;


/** Some forward declared function headers */
int verify_knownhost(ssh_session session);


/** Initialises a context with everything that is required for it to work **/
int pk_sm_init(pk_sm_ctx *ctx, pk_client *cl)
{
    CHECK_CTX

    /* Blank memory for safety */
    memset(ctx, 0, sizeof(pk_sm_ctx));

    /* Copy pk_client into struct */
    memcpy(&ctx->client, cl, sizeof(pk_client));

    /* Create a dummy ssh session we can work with in the future */
    ctx->session = ssh_new();
    if(ctx->session == NULL) return PK_INIT_FAILED;

    /* Update times & return */
    ctx->creation = time(0);
    ctx->updated = ctx->creation;
    return PK_ERR_SUCCESS;
}

int pk_sm_start(pk_sm_ctx *ctx)
{
    CHECK_CTX

    int ret;
    int verbosity = SSH_LOG_PROTOCOL;

    /* Initialise our SSH session with some basic settings */
    ret = ssh_options_set(ctx->session, SSH_OPTIONS_HOST, ctx->client.hostname);
    ret = ssh_options_set(ctx->session, SSH_OPTIONS_LOG_VERBOSITY, &verbosity);
    ret = ssh_options_set(ctx->session, SSH_OPTIONS_PORT, &ctx->client.port);

    /* Attempt to open a connection - carefully */
    ret =  ssh_connect(ctx->session);
    if (ret != SSH_OK) {
        fprintf(stdout, "Error connecting to localhost: %s\n", ssh_get_error(ctx->session));
        return PK_ERR_ERROR;
    }

    /* After opening the connection - verify it */
    verify_knownhost(ctx->session);
}

/** Safely frees a context from memory **/
int pk_sm_free(pk_sm_ctx *ctx)
{
    return PK_ERR_SUCCESS;
}


/******************************************************************************/

/**
 * Verifies the identity of a server with the end user
 *
 * TODO: Remove depreciated function calls
 *
 * @param session
 * @return
 */
int verify_knownhost(ssh_session session)
{
    int state;
    size_t hlen;
    unsigned char *hash = NULL;
    char *hexa;
    char buf[10];
    state = ssh_is_server_known(session);
    hlen = (size_t) ssh_get_pubkey_hash(session, &hash);

    if (hlen < 0)
        return -1;

    switch (state) {
        case SSH_SERVER_KNOWN_OK:
            break; /* ok */

        case SSH_SERVER_KNOWN_CHANGED:
            fprintf(stdout, "Host key for server changed: it is now:\n");
            ssh_print_hexa("Public key hash", hash, hlen);
            fprintf(stdout, "For security reasons, connection will be stopped\n");
            free(hash);
            return -1;

        case SSH_SERVER_FOUND_OTHER:
            fprintf(stdout, "The host key for this server was not found but an other type of key exists.\n");
            fprintf(stdout, "An attacker might change the default server key to confuse your client into thinking the key does not exist\n");
            free(hash);
            return -1;

        case SSH_SERVER_FILE_NOT_FOUND:
            fprintf(stdout, "Could not find known host file.\n");
            fprintf(stdout, "If you accept the host key here, the file will be automatically created.\n");
            /* fallback to SSH_SERVER_NOT_KNOWN behavior */

        case SSH_SERVER_NOT_KNOWN:
            hexa = ssh_get_hexa(hash, hlen);
            fprintf(stdout,"The server is unknown. Do you trust the host key?\n");
            fprintf(stdout, "Public key hash: %s\n", hexa);
            free(hexa);

            if (fgets(buf, sizeof(buf), stdin) == NULL) {
                free(hash);
                return -1;
            }

            if (strncasecmp(buf, "yes", 3) != 0) {
                free(hash);
                return -1;
            }

            if (ssh_write_knownhost(session) < 0) {
                fprintf(stdout, "Error %s\n", strerror(errno));
                free(hash);
                return -1;
            }

            break;

        case SSH_SERVER_ERROR:
        default:
            fprintf(stdout, "Error %s", ssh_get_error(session));
            free(hash);
            return -1;
    }
    free(hash);
    return 0;
}