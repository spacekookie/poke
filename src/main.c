#include <poke.h>

#include <stdio.h>
#include <stdlib.h>

#include <argp.h>

const char *argp_program_version = "Poke 0.6b";
const char *argp_program_bug_address = "<kookie@spacekookie.de>";
static char doc[] = "Poke -- a powerful ssh utility";
static char args_doc[] = "SERVER";

static struct argp_option options[] = { {"generate",  'g', 0,      0,  "Generate a new key for the provided server" } };

struct arguments {
    char *args[1];
    int generate;
};

static error_t parse_opt (int key, char *arg, struct argp_state *state)
{
    struct arguments *arguments = state->input;

    switch (key) {
        case 'g':
            arguments->generate = 1;
            break;

        case ARGP_KEY_ARG:
            if (state->arg_num >= 2)
                argp_usage (state);

            arguments->args[state->arg_num] = arg;

            break;

        case ARGP_KEY_END:
            if (state->arg_num < 1)

                /* Not enough arguments. */
                argp_usage (state);
            break;

        default:
            return ARGP_ERR_UNKNOWN;
    }
    return 0;
}

/* Our argp parser. */
static struct argp argp = { options, parse_opt, args_doc, doc };

int main (int argc, char **argv)
{
    /* Start by parsing arguments */
    struct arguments arguments = { 0, 0 };
    argp_parse (&argp, argc, argv, 0, 0, &arguments);

    /* Print out the options and stuff */
    printf ("Server = %s\nGenerate = %s\n", arguments.args[0], arguments.generate ? "yes" : "no");

    exit (0);
}




//    /* Check if we were given a "host" */
//    if(argn < 1) {
//        printf("No host provided\n");
//        return 255;
//    }
//
//    /* Copy a reference to the provided hostname */
//    char hostname[256];
//    memset(hostname, 0, sizeof(char) * 256)
//    strcpy(hostname, argv[1]);
//
//    /* Create a context for a test path */
//    pk_parse_ctx parser;
//
//    /* Parse the ssh config */
//    pk_parse_init(&parser, SSH_PATH);
//
//    pk_parse_load(&parser);
//
//    pk_parse_hst *host;
//    int err = pk_parse_query(&parser, &host, hostname);
//
//    /* If the host was null */
//    if(host == NULL) {
//        printf("The host provided wasn't found in %s\n", SSH_PATH);
//        return 155;
//    }
//
//    /* Free resources */
//    pk_parse_free(&parser);
//    return 0;

int poke_genkey(pk_parse_hst *host)
{
    char cmd[256];
    memset(cmd, 0, 256);
    sprintf(cmd, "echo -e  'y\\n' | ssh-keygen -t ed25519 -f ~/.ssh/%s_auto -P ''", host->host_id);

    /* Execute command */
    system(cmd);


    return 0;
}