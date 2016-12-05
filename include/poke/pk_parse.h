/* libpoke - pk_parse.h
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

#ifndef POKE_PK_PARSE_H
#define POKE_PK_PARSE_H

#include "pk.h"


#define PK_EXT          "#poke"
#define PK_UPDATED      "pk_updated"
#define PK_BLACKLIST    "pk_blacklisted"


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
    char            *raw_data;

    pk_parse_hst    **hosts;
    int             hsize, hused;

    /*
    * Store some metadata about the cfg.
    * Defined as "#poke (...)"
    */
    int           pk_version;
    long          pk_update_t;
    char          *pk_key_t;
    int           pk_key_len;
} pk_parse_ctx;


/** Prepare a parser context for a config file */
int pk_parse_init(pk_parse_ctx *ctx, const char *path);

/** Load the config to RAM and store a series of tokens to work on */
int pk_parse_load(pk_parse_ctx *ctx);

/** Remove the store token stream and list from memory */
int pk_parse_dump(pk_parse_ctx *ctx);

/** Find information in the token stream for access */
int pk_parse_query(pk_parse_ctx *ctx, pk_parse_hst **data, const char *hostname);

/** Free parser context from memory completely */
int pk_parse_free(pk_parse_ctx *ctx);

void pk_parse_printhst(pk_parse_hst *host);

#endif