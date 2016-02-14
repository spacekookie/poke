extern crate rustc_serialize;
extern crate docopt;

/** External imports */
use std::io::prelude::*;
use std::io::BufReader;
use std::error::Error;
use std::path::Path;
use std::fs::File;

use docopt::Docopt;

/* Internal imports */


/* Docopt definitions */
const VERSION: &'static str = "0.7.0";
const USAGE: &'static str = "Ghost in the Shell
Usage:
  ghost --add <server> <sshcommand>
  ghost --add <server>
  ghost --rm <server>
  ghost [-q] <server>
  ghost --list
  ghost (-h | --help)
  ghost (--version)

Options:
  -h, --help      Show this screen.
  --version       Show version.

  add             Add a new entry to your ssh config from your shell history
  ls              Show all targets from ssh config
  <server>        Connect to that server from your ssh config
";

#[derive(Debug, RustcDecodable)]
struct Args {
    flag_q: bool,
    flag_add: bool,
    flag_rm: bool,
    flag_list: bool,

    arg_server: Vec<String>,
    arg_sshcommand: Vec<String>,
}

struct ConfigHelper<'a> {
    ssh_path: &'a str,
}

impl<'a> ConfigHelper<'a> {
    pub fn new(ssh_path: &str) -> ConfigHelper {
        ConfigHelper {
            ssh_path: ssh_path,
        }
    }

    fn parseConfig(&self) {
        /* The `description` method of `io::Error` returns a string that describes the error */
        let file = match File::open(self.ssh_path) {
          Err(why) => panic!("couldn't open {}: {}", self.ssh_path, Error::description(&why)),
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
            } else if l.trim().starts_with("User") {
                // println!("> {}", l);
            }
        }
    }
}

/* Main entry point for our application */
fn main() {
    let version = VERSION.to_owned();
    // let args = Docopt::new(USAGE).and_then( |dopt| dopt.version(Some(version)).parse() ).unwrap_or_else( |e| e.exit() );
    let args: Args = Docopt::new(USAGE).and_then(|d| d.version(Some(version)).decode()).unwrap_or_else(|e| e.exit());

    if args.flag_list {
      let cfg = ConfigHelper::new("/home/spacekookie/.ssh/config");
      cfg.parseConfig();
    } 
}

/*    println!("\nSome values:");
    println!("  Server {:?}", args.arg_server);
    println!("  SSH CMD {:?}", args.arg_sshcommand);
    println!("  Invoking q: {:?}", args.flag_q);
    println!("  Invoking add: {:?}", args.flag_add);
    println!("  Invoking rm: {:?}", args.flag_rm);*/