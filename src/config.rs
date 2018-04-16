//! A small utility module handling poke configs
//!
//! The config is stored in .ssh/poke/config.toml and contains
//! metadata fields about the keystore as well as key-timeouts
//! and...stuff

use std::{fs::File,
          io::{Read, Write},
          path::Path};
use toml as serde_toml;

#[derive(Serialize, Deserialize)]
struct Config {
    pub keystore: Option<String>,
    pub experimental: bool,
    pub renew_keys: bool,
}

impl Config {
    /// Store an empty config to disk
    pub fn create_empty(path: &str) -> Config {
        let toml = serde_toml::to_string(&Config {
            keystore: None,
            experimental: false,
            renew_keys: false,
        }).unwrap();
        return Config::load(path);
    }

    /// Load an existing config int a struct
    pub fn load(path: &str) -> Config {
        return match Path::new(path).exists() {
            true => {
                let mut content = String::new();
                let mut f = File::open(path).unwrap();
                f.read_to_string(&mut content).unwrap();
                serde_toml::from_str(&content).unwrap()
            }

            false => Config::create_empty(path),
        };
    }

    /// Save changes made to the struct to disk
    pub fn save(&mut self, path: &str) {
        let toml = serde_toml::to_string(self).unwrap();
        let mut f = File::open(path).unwrap();
        f.write_all(toml.as_bytes()).unwrap();
    }
}
