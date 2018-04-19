extern crate clap;
extern crate colored;
extern crate lockchain_core as lockchain;
extern crate question;
extern crate rpassword;

extern crate serde;
#[macro_use]
extern crate serde_derive;
extern crate toml;

// #[macro_use]
// extern crate human_panic;

mod cli;
mod keystore;
mod keywoman;
mod ssh;

mod config;
use config::Config;

use clap::ArgMatches;
use colored::*;
use question::{Answer, Question};
use std::process;
use std::{env, fs};

fn main() {
    /* This makes panic! pretty */
    // setup_panic!();

    /* Define our CLI App */
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
    if !ssh::get_directory().exists() {
        fs::create_dir_all(ssh::get_directory()).unwrap();
    }

    let name = matches.value_of("name").unwrap();
    let addr = matches.value_of("addr").unwrap();
    ssh::generate_key(
        &ssh::get_directory().to_str().unwrap(),
        &format!("{}_local", name),
    );
    ssh::send_key(
        ssh::get_directory()
            .join(&format!("{}_local.pub", &name))
            .to_str()
            .unwrap(),
        &addr,
    );
}

fn handle_setup(matches: &ArgMatches) {
    let path = String::from(matches.value_of("path").unwrap());
    let cfg_path = &format!(
        "{}/.config/poke.toml",
        env::home_dir().unwrap().to_str().unwrap()
    );

    /* Create or load config */
    let mut cfg = match Config::load(cfg_path) {
        None => Config::create_empty(&cfg_path),
        Some(cfg) => cfg,
    };

    if cfg.keystore.is_some() {
        let cont = Question::new("Keystore already registered. Change location?")
            .default(Answer::NO)
            .show_defaults()
            .confirm();

        if cont == Answer::NO {
            println!("Aborting re-setup!");
            process::exit(2);
        }
    }

    /* Store the absolute path to the keystore */
    let p_slice = fs::canonicalize(&path).unwrap();
    cfg.keystore = Some(String::from(p_slice.to_str().unwrap()));
    cfg.save(cfg_path);

    /* Get a desired user password */
    let pass = rpassword::prompt_password_stdout("Set a keystore password: ").unwrap();
    let pub_path = keywoman::generate_root(path, pass);

    println!("{}", "✨ A new keystore was generated for you ✨".green());
    println!("");
    println!("Your root public key can be found here: '{}'", pub_path);
}

fn handle_load(matches: &ArgMatches) {}
