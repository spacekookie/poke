// External includes
/*use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

use std::io::BufReader;*/

// Internal includes

/*fn main() {

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
*/
extern crate rustc_serialize;
extern crate docopt;

use docopt::Docopt;

const VERSION: &'static str = "0.7.0";

const USAGE: &'static str = "Ghost in the Shell

Usage:
  ghost <server> <ssh command>
  ghost (add | a) <server>
  ghost rm <server>
  ghost [-q] <server> [ssh options]
  ghost (list | ls)
  ghost (-h | --help)
  ghost (--version)

Options:
  -h, --help      Show this screen.
  --version       Show version.

  add             Add a new entry to your ssh config from your shell history
  ls              Show all targets from ssh config
  <server>        Connect to that server from your ssh config
";
//  -q <server>   Connect to that server without copying files from .pokerc

#[derive(Debug, RustcDecodable)]
struct Args {

    /* Additional flags */
    flag_q: bool,
    flag_version: bool,

    /* Arguments */
    arg_server: Vec<String>,
    arg_x: Option<i32>,
    arg_y: Option<i32>,

    /* Commands */
    cmd_add: bool,
    cmd_list: bool,
    cmd_rm: bool,
}

fn main() {
  let version = VERSION.to_owned();
  let args = Docopt::new(USAGE).and_then(|dopt| dopt.version(Some(version)).parse()).unwrap_or_else(|e| e.exit());

  println!("Some arguments:");
  println!("  Speed: {}", args.get_str("--speed"));
}