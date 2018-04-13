extern crate clap;

use clap::{App, SubCommand};

fn main() {
    let app = App::new("poke")
        .version("0.0.0")
        .author("Katharina Fey")
        .about("Powerful utility to manage ssh keys")
        .subcommand(
            SubCommand::with_name("generate")
                .alias("g")
                .about("Generate new keys for this computer for a specific server"),
        );

    match app.get_matches() {
        _ => unreachable!("The compiler should prevent this."),
    }
}
