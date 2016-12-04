/* libpoke - pk_target.h
 *
 * A simple data storage file that handles ssh targets seen
 *    by libpoke. It makes handling with target structs in
 *    in memory easier.
 *
 * (c) 2016 					Katharina Sabel.
 * Authors:						Katharina 'spacekookie' Sabel
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
 * -------------------------------------------
 *
 */


/* Base data struct to represent a server in the ssh config */
typedef struct pk_trgt_ctx
{
	const char *hostname;
	const char *username;
	
	char *key_id;
	long last_updated;
};


/** Initialise a new pk target with a hostname and username, kid can be null */
int pk_trgt_init(pk_trgt_ctx *ctx, const char *hst_n, const char *usr_n, char *kid);


/** Changes the key ID of the provided context and updates the access time */
int pk_trgt_update(pk_trgt_ctx *ctx, char *kid);


/** Cleanly de-allocates all the resources from the context */
int pk_trgt_destroy(pk_trgt_ctx *ctx);