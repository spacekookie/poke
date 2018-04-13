//! An ssh runner utility

use std::process::Command;

/// Generate a new key and store it in $USER/.ssh/poke
pub fn generate_key(name: &str) {
    let foo = Command::new("ssh-keygen").args($["-t", "ed25519", "-f", &format!("$HOME/.ssh/{}", name), "-N", "''"]).output()
            .expect("Failed to execute `ssh-keygen`");
}