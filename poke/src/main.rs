// External includes
use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

use std::io::BufReader;

// Internal includes

fn main() {

  /* Create a path to the desired file */
  let path = Path::new("/home/spacekookie/.ssh/config");
  let display = path.display();

  /* The `description` method of `io::Error` returns a string that describes the error */
  let file = match File::open(&path) {
    Err(why) => panic!("couldn't open {}: {}", display, Error::description(&why)),
    Ok(file) => file,
  };

  /* Iterate over the lines and print them */
  let br = BufReader::new(&file);
  for line in br.lines() {
    let l = line.unwrap();

    if l.trim().starts_with("HostName") {
      // print!("\t\t {}\n", &l[12..]);
    } else if l.trim().starts_with("Host") {
      print!("- {}\n", &l[5..]);
    } else if l.trim().starts_with("User")
    // println!("> {}", l);
  }
}

// fn main() {

//   print!("Display is {}", display);

//   Open the path in read-only mode, returns `io::Result<File>`


//   Read the file contents into a string, returns `io::Result<usize>`
//   let mut s = String::new();
//   match file.read_to_string(&mut s) {
//       Err(why) => panic!("couldn't read {}: {}", display, Error::description(&why)),
//       Ok(_) => print!("{} contains:\n{}", display, s),
//   }

//   `file` goes out of scope, and the "hello.txt" file gets closed
// }

// extern crate rustc_serialize;
// extern crate docopt;

// use docopt::Docopt;

// const USAGE: &'static str = "___
// \\  \\ 
//  \\  \\  Poke 
//  /  /      ssh connection utility
// /__/

// Usage:
//   poke <server> <ssh command>
//   poke (add | a) <server>
//   poke rm <server>
//   poke [-q] <server> [ssh options]
//   poke (list | ls)
//   poke (-h | --help)
//   poke (-v | --version)

// Options:
//   -h, --help    Show this screen.
//   --version     Show version.
//   add           Add a new entry to your ssh config from your shell history
//   ls            Show all targets from ssh config
//   <server>      Connect to that server from your ssh config
//   -q <server>   Connect to that server without copying files from .pokerc
// ";

// #[derive(Debug, RustcDecodable)]
// struct Args {
//     flag_speed: isize,
//     flag_drifting: bool,
//     arg_name: Vec<String>,
//     arg_x: Option<i32>,
//     arg_y: Option<i32>,
//     cmd_ship: bool,
//     cmd_mine: bool,
// }

// use std::io;

// fn main() {
//   let file = match File::open("/home/spacekookie/.ssh/config") {
//     Ok(file) => file,
//     Err(..)  => panic!("room"),
//   };
// }

// fn main() {
//     let args: Args = Docopt::new(USAGE)
//                             .and_then(|d| d.decode())
//                             .unwrap_or_else(|e| e.exit());
//     println!("{:?}", args);
// }
