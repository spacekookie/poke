//! SSH Keystore module using lockchain

use lockchain::{Payload, Vault, record::Record};

/// The poke keystore
pub(crate) struct KeyStore {
    vault: Vault,
}

impl KeyStore {
    pub fn new(path: &str, pw: &str) -> Option<KeyStore> {
        return match Vault::new("poke", path, pw) {
            Ok(vault) => Some(KeyStore { vault }),
            Err(_) => None,
        };
    }

    pub fn load(path: &str, pw: &str) -> Option<KeyStore> {
        return match Vault::load("poke", path, pw) {
            Ok(vault) => Some(KeyStore { vault }),
            Err(_) => None,
        };
    }

    /// Insert a key with a name into the keystore
    ///
    /// This can either add a new key or override an existing
    /// key. When overriding, the old key *technically* remainds
    /// available in the versioning of the lockchain record.
    pub fn insert_key(&mut self, name: &str, key: String) {
        self.vault.add_record(name, "keys", Vec::new());
        self.vault.add_data(name, "key", Payload::Text(key));
    }

    /// Get the current key for a certain domain
    pub fn get_key(&mut self, name: &str) -> Option<String> {
        let r: &mut Record = self.vault.records.get_mut(name).unwrap();
        let payload = r.get_data("key");

        return match payload {
            Payload::Text(t) => Some(t),
            _ => None,
        };
    }
}
