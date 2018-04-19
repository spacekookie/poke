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
    let ks_path = String::from(matches.value_of("path").unwrap());

    /* Either create or load existing config */
    let mut cfg = Config::load().unwrap_or_else(|| Config::create_empty());
    cfg.if_no_keystore(|| {
        let cont = Question::new("Keystore already registered. Change location?")
            .default(Answer::NO)
            .show_defaults()
            .confirm();

        if cont == Answer::NO {
            println!("Aborting re-setup!");
            process::exit(2);
        }
    });

    /* Set the new keystore path & sync */
    cfg.set_keystore(&ks_path);
    cfg.sync();

    /* Get a desired user password */
    let pass = rpassword::prompt_password_stdout("Set a keystore password: ").unwrap();
    let pass_confirm = rpassword::prompt_password_stdout("Confirm the password: ").unwrap();
    if pass != pass_confirm {
        eprintln!("{}", "The two passwords did not match!".red());
        process::exit(2);
    }

    let pub_path = keywoman::generate_root(ks_path, pass);

    /* Print about our success */
    println!("");
    println!("{}", "✨ A new keystore was generated for you ✨".green());
    println!("Your root public key can be found here: '{}'", pub_path);
}

fn handle_load(matches: &ArgMatches) {}
