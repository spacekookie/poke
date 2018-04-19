//! Small utility modules which initialises and defines the CLI parsing tree

use clap::{App, Arg, SubCommand};

const APP_NAME: &'static str = env!("CARGO_PKG_NAME");
const VERSION: &'static str = env!("CARGO_PKG_VERSION");
const ABOUT: &'static str = env!("CARGO_PKG_DESCRIPTION");
const AUTHOR: &'static str = env!("CARGO_PKG_AUTHORS");

/// Crete the parsing tree for poke
pub fn create() -> App<'static, 'static> {
    return App::new(APP_NAME)
        .version(VERSION)
        .about(ABOUT)
        .author(AUTHOR)
        .subcommand(
            SubCommand::with_name("setup")
                .display_order(1)
                .alias("s")
                .about("Setup poke keystore backend. This can either crate a fresh \
                        keystore or link into an existing one.")
                .arg(Arg::with_name("path")
                        .short("p")
                        .long("store-path")
                        .takes_value(true)
                        .required(true)
                        .display_order(1)
                        .help("Provide the path to a poke keystore")),
        )
        .subcommand(
            SubCommand::with_name("generate")
                .display_order(2)
                .alias("g")
                .about("Generate a new key for this computer for a specific server and store it in the poke keystore.")
                .arg(
                    Arg::with_name("name")
                        .required(true)
                        .help("Provide a name for the new generated keyfile"),
                )
                .arg(
                    Arg::with_name("addr")
                        .required(true)
                        .help("Provide the remote address for your server"),
                ),
        )
        .subcommand(
            SubCommand::with_name("load")
                .display_order(3)
                .alias("l")
                .about("Load all keys associated to this computer from the poke keystore.")
                .arg(
                    Arg::with_name("name")
                        .short("n")
                        .long("name")
                        .help("Manually provide a hostname if your machine hostname is not accurate."),
                )
        );
}
