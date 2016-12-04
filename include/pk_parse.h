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

#include <poke/pk.h>


typedef struct pk_parse_hst
{
  char  hostname[128];
  char  username[128];
  char  keyfile[128];
  int   port;
}


typedef struct pk_parse_ctx
{
  char  *ssh_path;
  char  *ssh_config;

  char          *raw_data;
  pk_parse_hst  **hosts;
};


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