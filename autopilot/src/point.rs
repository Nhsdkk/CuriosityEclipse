#[warn(dead_code)]
pub struct Point {
    pub x: f64,
    pub y: f64,
    pub z: f64
}

impl Point{
    #[warn(dead_code)]
    pub fn new(x: f64, y: f64, z: f64) -> Self {
        Point{x, y, z}
    }
}
