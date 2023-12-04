use std::thread::sleep;
use std::time::Duration;
use krpc_client::Client;
use krpc_client::services::space_center::{Control, Flight, SASMode, SpaceCenter, Vessel};
use crate::autopilot::AltitudeWaitingMode::{PeriapsisAltitudeWaitingMode, SurfaceAltitudeWaitingMode};

#[derive(PartialEq)]
enum AltitudeWaitingMode {
    PeriapsisAltitudeWaitingMode,
    SurfaceAltitudeWaitingMode
}

const MIN_PERIAPSIS_ALTITUDE: f64 = 30.0 * 1e3;
const PARACHUTES_DEPLOY_ALTITUDE: f64 = 11.0 * 1e3;
const SUN_SHIELD_DETACH_ALTITUDE: f64 = 3.0 * 1e3;
const PARACHUTES_DETACH_ALTITUDE: f64 = 1.5 * 1e3;
const LANDING_SPEED: f64 = -10.0;

const LANDING_SPEED_RIGHT_BEFORE_LANDING: f64 = -3.0;

pub struct Autopilot{
    vessel: Vessel,
    controller: Control,
    flight: Flight
}

impl Autopilot{
    pub fn new(address: &str, port: u16, stream_port: u16) -> Self {
        println!("Address: {:} Port: {:} Stream port: {:}", address, port, stream_port);
        let client = Client::new("Autopilot Client", address, port, stream_port).unwrap();
        let space_center = SpaceCenter::new(client.clone());
        let vessel = space_center.get_active_vessel().unwrap();
        let controller = vessel.get_control().unwrap();
        let bodies = space_center.get_bodies().unwrap();
        let duna = bodies.get("Duna").unwrap();
        let flight = vessel.flight(Some(&duna.get_reference_frame().unwrap())).unwrap();

        Autopilot{vessel, controller, flight}
    }

    fn get_periapsis_altitude(&mut self) -> f64{
        self.vessel.get_orbit().unwrap().get_periapsis_altitude().unwrap()
    }

    fn lower_periapsis_altitude(&mut self) {
        let periapsis_altitude = self.get_periapsis_altitude();

        if periapsis_altitude <= MIN_PERIAPSIS_ALTITUDE {
            return;
        }

        self.controller.set_sas(true).unwrap();
        self.controller.set_sas_mode(SASMode::Retrograde).unwrap();
        self.controller.set_throttle(0.1).unwrap();

        self.wait_until_altitude(MIN_PERIAPSIS_ALTITUDE, PeriapsisAltitudeWaitingMode);

        self.controller.set_throttle(0.0).unwrap();
        self.controller.set_sas_mode(SASMode::Prograde).unwrap();

        println!("Periapsis altitude has been lowered to {:}", periapsis_altitude);
    }

    fn get_current_surface_altitude(&mut self) -> f64 {
        self.flight.get_surface_altitude().unwrap()
    }

    fn detach_engine(&mut self){
        self.controller.activate_next_stage().unwrap();
        self.controller.set_sas_mode(SASMode::StabilityAssist).unwrap();
    }

    fn wait_until_altitude(&mut self, value: f64, waiting_mode: AltitudeWaitingMode) {

        let mut current_altitude;
        if waiting_mode == SurfaceAltitudeWaitingMode {
            current_altitude = self.get_current_surface_altitude();
        }else{
            current_altitude = self.get_periapsis_altitude();
        }

        while current_altitude > value {
            if waiting_mode == SurfaceAltitudeWaitingMode {
                current_altitude = self.get_current_surface_altitude();
            }else{
                current_altitude = self.get_periapsis_altitude();
            }
            println!("Waiting... Current altitude = {:}", current_altitude);
        }

        println!("Waiting complete Current altitude = {:}", current_altitude);
    }

    fn prepare_hinges(&mut self) {
        let parts = self.vessel.get_parts().unwrap();
        let robotic_hinges = parts.get_robotic_hinges().unwrap();
        for hinge in robotic_hinges {
            hinge.set_target_angle(90.0).unwrap();
            hinge.set_motor_engaged(true).unwrap();
        }
    }

    fn get_current_vertical_velocity(&mut self) -> f64{
        self.flight.get_vertical_speed().unwrap()
    }

    fn set_velocity_landing_engines(&mut self, value: f32) {
        self.controller.set_throttle(value).unwrap();
    }

    fn slow_descend(&mut self) {
        let mut current_surface_altitude = self.get_current_surface_altitude();
        while current_surface_altitude > 2.0 {
            let current_velocity = self.get_current_vertical_velocity();
            println!("Current velocity: {}, Current altitude {}", current_velocity, current_surface_altitude);
            let speed_limit: f64;
            if current_surface_altitude > 50.0 {
                speed_limit = LANDING_SPEED;
            } else{
                speed_limit = LANDING_SPEED_RIGHT_BEFORE_LANDING;
            }
            if current_velocity < speed_limit {
                self.set_velocity_landing_engines(1.0);
            }else{
                self.set_velocity_landing_engines(0.0);
            }
            current_surface_altitude = self.get_current_surface_altitude();
        }
        self.controller.activate_next_stage().unwrap();
    }

    pub fn land(&mut self) {
        self.lower_periapsis_altitude();
        sleep(Duration::from_secs(15));
        self.detach_engine();
        self.wait_until_altitude(PARACHUTES_DEPLOY_ALTITUDE, SurfaceAltitudeWaitingMode);
        self.controller.activate_next_stage().unwrap();
        self.wait_until_altitude(SUN_SHIELD_DETACH_ALTITUDE, SurfaceAltitudeWaitingMode);
        self.controller.activate_next_stage().unwrap();
        self.controller.set_sas_mode(SASMode::Radial).unwrap();
        self.prepare_hinges();
        self.wait_until_altitude(PARACHUTES_DETACH_ALTITUDE, SurfaceAltitudeWaitingMode);
        self.controller.activate_next_stage().unwrap();
        self.controller.activate_next_stage().unwrap();
        sleep(Duration::from_secs(2));
        self.slow_descend();
    }


}