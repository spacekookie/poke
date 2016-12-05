/* libpoke - poke.h
 *
 * (c) 2016           Katharina Sabel.
 * Authors:           Katharina 'spacekookie' Sabel
 *
 * This program and the accompanying materials
 * are made available under the terms of the GNU Lesser General Public License
 * (LGPL) version 3 which accompanies this distribution, and is available at
 * http://www.gnu.org/licenses/lgpl-3.html
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 */

/**************************************************************************************/

#ifndef POKE_PK_H
#define POKE_PK_H


#include <stdbool.h>
#include <unistd.h>


/***********************************************
 *
 * ERROR RETURN VALUE DEFINITIONS
 *
 ***********************************************/


#define PK_ERR_SUCCESS          0
#define PK_ERR_GENERROR         1
#define PK_ERR_MALLOC_FAILED    2
#define PK_ERR_INVALID_PARAMS   3


/** A unified pk_client struct that holds host data **/
// TODO: Change fields to heap-pointers
typedef struct pk_client
{
    char    host_id[128];           // Host name (ID)
    char    hostname[128];          // Address (IP or DNS)
    char    username[128];          // Username required

    char    id_only[128];           // Only use keys
    char    id_file[128];           // What key to use
    char    port[128];              // SSH port

    char    pk_updated[128];        // Last key update time
    char    pk_blacklist[128];      // Ignore pk_* variables
} pk_client;


union pk_cfg_snippet{
    pk_client   *client;
    char        *block;
};


typedef struct pk_config {
    int         pk_version;
    long        pk_upfreq;

    union pk_cfg_snippet    **snippets;
    size_t                  snip_curr, snip_max;
} pk_config;


/***********************************************
 *
 * PK PARSER DEFINITIONS
 *
 ***********************************************/


/* Define some pk extentions (protocol version 1) */
#define PK_EXT          "#poke"
#define PK_VERSION      "pk_version"
#define PK_UP_FREQ      "pk_upfreq"
#define PK_UPDATED      "pk_updated"
#define PK_BLACKLIST    "pk_blacklisted"

/* Define our key value markers */
#define HOST_NAME   "HostName"
#define HOST_ID     "Host"
#define PORT        "Port"
#define USER        "User"
#define ID_ONLY     "IdentitiesOnly"
#define ID_FILE     "IdentityFile"


/* Define some default parameters that can be overwritten at compile time */
// TODO: Find out actual default values
#define PK_DEFAULT_UPDATED      "-1"
#define PK_DEFAULT_BLACKLIST    "no"
#define PK_DEFAULT_PORT         "22"
#define PK_DEFAULT_ID_ONLY      "no"


typedef struct pk_parse_ctx
{
    char        *ssh_path;
    char        *raw_data;

    bool        recursive;
} pk_parse_ctx;


/** Prepare a parser context for a config file */
int pk_parse_init(pk_parse_ctx *ctx, const char *path);

/** Load the config to RAM and store a series of tokens to work on */
int pk_parse_load(pk_parse_ctx *ctx, pk_config **cfg);

/** Remove the store token stream and list from memory */
int pk_parse_dump(pk_parse_ctx *ctx);

/** Find information in the token stream for access */
int pk_parse_query(pk_parse_ctx *ctx, pk_client **data, const char *host_id);

/** Free parser context from memory completely */
int pk_parse_free(pk_parse_ctx *ctx);

void pk_parse_printhst(pk_client *host);


/***********************************************
 *
 * PK SESSION MANAGER DEFINITIONS
 *
 ***********************************************/


/** Define a session manager context that holds metadata about current session **/
typedef struct pk_sm_ctx
{
    const pk_client *target;
    char            *cmd;
    char            *key_swap;
} pk_sm_ctx;


/** Initialises a context with everything that is required for it to work **/
int pk_sm_init(pk_sm_ctx *ctx, const char *cfg_pth);

/** Safely frees a context from memory **/
int pk_sm_free(pk_sm_ctx *ctx);


#endif // POKE_PK_H