/* File handling */
use std::io::prelude::*;
use std::io::BufReader;
use std::error::Error;
use std::fs::File;

struct ConfigHelper<'a> {
    ssh_path: &'a str,
}

impl<'a> ConfigHelper<'a> {
    pub fn new(ssh_path: &str) -> ConfigHelper {
        ConfigHelper {
            ssh_path: ssh_path,
        }
    }

    fn parse_config(&self) {
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