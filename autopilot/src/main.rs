use crate::autopilot::Autopilot;

mod autopilot;

fn main() {
    let mut autopilot = Autopilot::new("127.0.0.1", 1000, 1001);
    autopilot.land();
}
