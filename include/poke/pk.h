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


#define PK_ERR_SUCCESS          0
#define PK_ERR_GENERROR         1
#define PK_ERR_MALLOC_FAILED    2
#define PK_ERR_INVALID_PARAMS   3


/* Base data struct to represent a server in the ssh config */
typedef struct pk_trgt_ctx
{
    char *hostname;
    char *username;
    char *key_id;

    long last_updated;
} pk_trgt_ctx;

/** Initialise a new pk target with a hostname and username, kid can be null */
int pk_trgt_init(pk_trgt_ctx *ctx, const char *hst_n, const char *usr_n, char *kid);

/** Changes the key ID of the provided context and updates the access time */
int pk_trgt_update(pk_trgt_ctx *ctx, char *kid);

/** Cleanly de-allocates all the resources from the context */
int pk_trgt_free(pk_trgt_ctx *ctx);

/**************************************************************************************/

/** Main poke daemon context struct */
typedef struct pk_dm_ctx
{
    const char      *cfg_pth;
    long            start_t;
    pk_trgt_ctx     **targets;
} pk_dm_ctx;

/** Initialises a context with everything that is required for it to work **/
int pk_dm_init(pk_dm_ctx *ctx, const char *cfg_pth);

/** Queries target information from the known hosts. Can replace ssh **/
int pk_dm_query(pk_dm_ctx *ctx, pk_trgt_ctx **trgt, const char *host);

/** Safely frees a context from memory **/
int pk_dm_free(pk_dm_ctx *ctx);

#endif // POKE_PK_H