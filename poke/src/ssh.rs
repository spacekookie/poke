//! An ssh runner utility

use std::{env::home_dir, path::PathBuf, process::Command};

pub(crate) fn get_directory() -> PathBuf {
    let mut base = PathBuf::from(home_dir().unwrap());
    base = base.join(".ssh").join("poke");
    return base;
}

/// Generate a new key and store it in $USER/.ssh/poke
pub(crate) fn generate_key(path: &str, name: &str) {
    let foo = Command::new("ssh-keygen")
        .arg("-t")
        .arg("ed25519")
        .arg("-f")
        .arg(&format!("{}/{}", path, name))
        .arg("-N")
        .arg("''")
        .output()
        .expect("Failed to execute `ssh-keygen`");

    print!("{}", String::from_utf8(foo.stdout).unwrap());
}

/// Register a new key with a remote server
pub(crate) fn send_key(file_path: &str, server: &str) {
    println!("Adding public key to server...");
    let foo = Command::new("scp")
        .arg(file_path)
        .arg(&format!("{}:~/.ssh", server))
        .output()
        .expect("Failed to copy key to server!");

    println!("{}", String::from_utf8(foo.stdout).unwrap());
    println!("{}", String::from_utf8(foo.stderr).unwrap());
}
