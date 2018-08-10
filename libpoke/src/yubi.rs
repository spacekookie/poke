use yubico::config::{Command, Config, Mode, Slot};
use yubico::configure::DeviceModeConfig;
use yubico::hmacmode::HmacKey;
use yubico::Yubico;

use rand::distributions::Alphanumeric;
use rand::{thread_rng, Rng};

use hex;
use std::ops::Deref;

pub fn setup_secret() -> Result<(), String> {
    let mut yubi = Yubico::new();

    // We assume the first device
    if let Ok(device) = yubi.find_yubikey() {
        let config = Config::default()
            .set_vendor_id(device.vendor_id)
            .set_product_id(device.product_id)
            .set_command(Command::Configuration2);

        let mut rng = thread_rng();
        let require_press_button = true;
        let secret: String = rng.sample_iter(&Alphanumeric).take(20).collect();
        let hmac_key: HmacKey = HmacKey::from_slice(secret.as_bytes());

        let mut device_config = DeviceModeConfig::default();
        device_config.challenge_response_hmac(&hmac_key, false, require_press_button);

        if let Err(_) = yubi.write_config(config, &mut device_config) {
            return Err("Failed to write configation".into());
        } else {
            return Ok(());
        }
    }

    Err("Yubikey not found".into())
}

pub fn retrieve_secret(token: [u8; 20]) -> Option<String> {
    let mut yubi = Yubico::new();

    if let Ok(device) = yubi.find_yubikey() {
        let config = Config::default()
            .set_vendor_id(device.vendor_id)
            .set_product_id(device.product_id)
            .set_variable_size(true)
            .set_mode(Mode::Sha1)
            .set_slot(Slot::Slot2);

        let hmac_result = yubi.challenge_response_hmac(&token, config).unwrap();
        let v: &[u8] = hmac_result.deref();
        return Some(hex::encode(v));
    } else {
        return None;
    }
}
