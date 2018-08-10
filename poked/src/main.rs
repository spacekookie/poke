extern crate libpoke as poke;
extern crate ssh_agent;

// use poke::rand::{thread_rng, Rng};
use std::os::unix::net::{UnixStream, UnixListener};

fn main() {
    let listener = UnixListener::bind("/path/to/the/socket").unwrap();
}
