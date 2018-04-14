extern crate clap;

mod ssh;

use clap::{App, Arg, SubCommand};
use std::fs;
use std::path::PathBuf;

fn get_ssh_dir() -> PathBuf {
    let mut base = PathBuf::from(std::env::home_dir().unwrap());
    base = base.join(".ssh").join("poke");
    return base;
}

fn main() {
    let app = App::new("poke")
        .version("0.0.0")
        .about("Powerful utility to manage ssh keys")
        .subcommand(
            SubCommand::with_name("generate")
                .alias("g")
                .about("Generate new keys for this computer for a specific server")
                .arg(Arg::with_name("name").required(true)),
        );

    match app.get_matches().subcommand() {
        ("generate", Some(m)) => {
            if !get_ssh_dir().exists() {
                fs::create_dir_all(get_ssh_dir()).unwrap();
            }

            let name = m.value_of("name").unwrap();
            ssh::generate_key(get_ssh_dir().to_str().unwrap(), name);
        }
        _ => {}
    }
}
