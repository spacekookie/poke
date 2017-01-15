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


/** A few import statements */
#include <dtree/dtree.h>
#include <libssh/libssh.h>


/*********** ERROR MESSAGE DEFINITIONS ***********/


#define PK_ERR_SUCCESS          0
#define PK_ERR_GENERROR         1
#define PK_ERR_MALLOC_FAILED    2
#define PK_ERR_INVALID_PARAMS   3
#define PK_ERR_NOT_FOUND        4
#define PK_ERR_INIT_FAILED      5


/*********** CONFIG PARSER FUNCTION DEFINITIONS ***********/


typedef struct pk_parse_hst
{
    char    host_id[128];
    char    hostname[128];
    char    username[128];

    char    id_only[128];
    char    id_file[128];

    char    port[128];

    /* Some poke specific metadata */
    char    pk_updated[128];
    char    pk_blacklist[128];
} pk_parse_hst;


typedef struct pk_parse_ctx
{
    char            *ssh_path;

    pk_parse_hst    *hosts;
    dtree           *struc;
    int             count;

    /* Cfg metadata as  #poke=<field> */
    int             pk_version;
    long            pk_update_t;
    char            *pk_key_t;
    int             pk_key_len;
} pk_parse_ctx;


/** Prepare a parser context for a config file */
int pk_parse_init(pk_parse_ctx *ctx, const char *path);

/** Load the config to RAM and store a series of tokens to work on */
int pk_parse_load(pk_parse_ctx *ctx);

/** Remove the store token stream and list from memory */
int pk_parse_dump(pk_parse_ctx *ctx);

/** Find information in the token stream for access */
int pk_parse_query(pk_parse_ctx *ctx, pk_parse_hst **data, const char *hostname);

/** Print all the hosts in a context */
int pk_parse_print(pk_parse_ctx *ctx);

/** Free parser context from memory completely */
int pk_parse_free(pk_parse_ctx *ctx);


/*********** CONFIG GENERATOR FUNCTION DEFINITIONS ***********/


/*********** POKE SESSION MANAGER FUNCTION DEFINITIONS ***********/

typedef struct pk_sm_ctx {
    ssh_session     sess;

    pk_parse_hst    *host;
    time_t          creation, updated;
} pk_sm_ctx;

/** Initialise a new session to a specific host - does not connect */
int pk_sm_init(pk_sm_ctx *ctx, pk_parse_hst *host);

/** Open an ssh connection with the host */
int pk_sm_start(pk_sm_ctx *ctx);

/** */
int pk_sm_stop(pk_sm_ctx *ctx);

/** Free all allocated memory from */
int pk_sm_free(pk_sm_ctx *ctx);

#endif // POKE_PK_H