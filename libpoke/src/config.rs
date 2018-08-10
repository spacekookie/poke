//! A small utility module handling poke configs
//!
//! The config is stored in .ssh/poke/config.toml and contains
//! metadata fields about the keystore as well as key-timeouts
//! and...stuff

use serde_toml;
use std::fs::{self, File, OpenOptions};
use std::io::{Read, Write};
use std::{env, path::Path};

#[derive(Serialize, Deserialize)]
pub struct Config {
    keystore: Option<String>,
    experimental: bool,
    renew_keys: bool,
}

impl Config {
    fn get_path() -> String {
        return format!(
            "{}/.config/poke.toml",
            env::home_dir().unwrap().to_str().unwrap()
        );
    }

    /// Store an empty config to disk
    pub fn create_empty() -> Config {
        Config {
            keystore: None,
            experimental: false,
            renew_keys: false,
        }.sync();
        return Config::load().unwrap();
    }

    /// Try to load an existing configuration
    pub fn load() -> Option<Config> {
        let path = Self::get_path();
        return match Path::new(&path).exists() {
            true => {
                let mut content = String::new();
                let mut f = File::open(path).unwrap();
                f.read_to_string(&mut content).unwrap();
                Some(serde_toml::from_str(&content).unwrap())
            }
            false => None,
        };
    }

    /// Stores the absolute (canonical) path to a keystore from
    /// the runtime relative path.
    pub fn set_keystore(&mut self, path: &str) {
        let p_slice = fs::canonicalize(&path).unwrap();
        self.keystore = Some(String::from(p_slice.to_str().unwrap()));
    }

    /// Runs a piece of code if a setting in the config is met
    pub fn if_keystore<F: 'static>(&self, function: F)
    where
        F: Fn(),
    {
        if self.keystore.is_some() {
            function();
        }
    }

    /// Sync changes made to the config to disk
    pub fn sync(&mut self) {
        let toml = serde_toml::to_string(self).unwrap();
        let path = Self::get_path();

        let mut f = OpenOptions::new()
            .write(true)
            .create(true)
            .open(path)
            .unwrap();
        f.write_all(toml.as_bytes()).unwrap();
    }
}
