//! A key manager who happens to be a woman
//!
//! This module is called from setup, load and generate. It
//! hooks straight into the poke cfg and the keystore
//! provided via `lockchain-core`

use colored::*;
use keystore::KeyStore;
use ssh;

use std::fs::{self, File};
use std::process;
use std::{io::Read, path::PathBuf};

/// A utility function to generate a new root-key
///
/// Generates a key that is essentially the same as
/// any other key, except that it can't be exported
/// via `poke load`.
///
/// It can also only be written once without triggering
/// th `poke panic` command.
pub fn generate_root(ks_path: String, ks_pw: String) -> String {
    let mut ks = KeyStore::load(&ks_path, &ks_pw).unwrap();
    if let Some(_) = ks.get_key("root@everybody") {
        eprintln!(
            "{}",
            "A root key has already been registered for this keystore!".red()
        );
        eprintln!("{}", " ... You can remove it with `poke panic`".red());
        process::exit(5);
    }

    /* Generate a new key */
    ssh::generate_key(
        &ssh::get_directory().to_str().unwrap(),
        "root@everybody_temporary",
    );

    /* Read the root key contents */
    let (key, path) = get_key_contents_then_delete("root@everybody_temporary");

    /* Store the root key contents in the keystore (vault) */
    ks.insert_key("root@everybody", key);
    return path;
}

/// If you couldn't tell from the function name: utility function
///
/// Only deletes the private variant of the root key
fn get_key_contents_then_delete(name: &str) -> (String, String) {
    let mut path = PathBuf::new();
    path.push(ssh::get_directory());
    path.push(name);

    let mut key_content = String::new();
    let mut f = File::open(&path).unwrap();
    f.read_to_string(&mut key_content)
        .expect("Failed to read newly generated ROOT key!");
    fs::remove_file(&path).expect("Failed to delete newly generated ROOT key!");

    /* Concat .pub at the end of it for the users benefit */
    let mut pub_root = String::from(path.to_str().unwrap());
    pub_root.push_str(".pub");

    return (key_content, pub_root);
}
