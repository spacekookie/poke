extern crate clap;

mod ssh;

use clap::{App, Arg, SubCommand};
use std::fs;
use std::path::PathBuf;

const APP_NAME: &'static str = env!("CARGO_PKG_NAME");
const VERSION: &'static str = env!("CARGO_PKG_VERSION");
const ABOUT: &'static str = env!("CARGO_PKG_DESCRIPTION");
const AUTHOR: &'static str = env!("CARGO_PKG_AUTHORS");

fn main() {
    let m = App::new(APP_NAME)
        .version(VERSION)
        .about(ABOUT)
        .author(AUTHOR)
        .subcommand(
            SubCommand::with_name("generate")
                .alias("g")
                .about("Generate new keys for this computer for a specific server")
                .arg(Arg::with_name("name").required(true).help("Provide a name for the new generated keyfile"))
                .arg(Arg::with_name("addr").required(true).help("Provide the remote address for your server")),
        )
        .get_matches();

    match m.subcommand() {
        ("generate", Some(m)) => {
            if !get_ssh_dir().exists() {
                fs::create_dir_all(get_ssh_dir()).unwrap();
            }

            let name = m.value_of("name").unwrap();
            let addr = m.value_of("addr").unwrap();
            ssh::generate_key(&get_ssh_dir().to_str().unwrap(), &format!("{}_local", name));
            ssh::send_key(
                get_ssh_dir()
                    .join(&format!("{}_local.pub", &name))
                    .to_str()
                    .unwrap(),
                &addr,
            );
        }
        _ => println!("Missing arguments: type `poke --help` for more help!"),
    }
}

fn get_ssh_dir() -> PathBuf {
    let mut base = PathBuf::from(std::env::home_dir().unwrap());
    base = base.join(".ssh").join("poke");
    return base;
}
