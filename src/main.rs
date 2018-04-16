extern crate clap;
extern crate lockchain_core as lockchain;

extern crate serde;
#[macro_use]
extern crate serde_derive;
extern crate toml;

mod cli;
mod config;
mod keystore;
mod ssh;

use clap::ArgMatches;
use keystore::KeyStore;
use std::{fs, path::PathBuf};

fn main() {
    let m = cli::create().get_matches();

    /* In this block we can unwrap quite viciously because clap will protect us */
    match m.subcommand() {
        ("setup", Some(m)) => handle_setup(m),
        ("load", Some(m)) => handle_load(m),
        ("generate", Some(m)) => handle_generate(m),
        _ => println!("Missing arguments: type `poke --help` for more help!"),
    }
}

fn handle_generate(matches: &ArgMatches) {
    if !get_ssh_dir().exists() {
        fs::create_dir_all(get_ssh_dir()).unwrap();
    }

    let name = matches.value_of("name").unwrap();
    let addr = matches.value_of("addr").unwrap();
    ssh::generate_key(&get_ssh_dir().to_str().unwrap(), &format!("{}_local", name));
    ssh::send_key(
        get_ssh_dir()
            .join(&format!("{}_local.pub", &name))
            .to_str()
            .unwrap(),
        &addr,
    );
}

fn handle_setup(matches: &ArgMatches) {
    let path = matches.value_of("path").unwrap();
}

fn handle_load(matches: &ArgMatches) {}

fn get_ssh_dir() -> PathBuf {
    let mut base = PathBuf::from(std::env::home_dir().unwrap());
    base = base.join(".ssh").join("poke");
    return base;
}
