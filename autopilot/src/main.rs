use crate::autopilot::Autopilot;

mod autopilot;
mod vector;
mod point;

fn main() {
    println!("Hello, world!");
    let mut autopilot = Autopilot::new("127.0.0.1", 1000, 1001);
    autopilot.land();
}
