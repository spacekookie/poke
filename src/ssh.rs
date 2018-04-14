//! An ssh runner utility

use std::process::Command;

/// Generate a new key and store it in $USER/.ssh/poke
pub fn generate_key(path: &str, name: &str) {
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
