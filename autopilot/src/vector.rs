use crate::point::Point;

#[warn(dead_code)]
pub struct Vector {
    start_point: Point,
    end_point: Point,
}

impl Vector {
    #[warn(dead_code)]
    pub fn new(start_point: Point, end_point: Point) -> Self {
        Vector{start_point, end_point}
    }

    pub fn modulo(&mut self) -> f64 {
        let delta_x_sq = (self.start_point.x - self.end_point.x).powi(2);
        let delta_y_sq = (self.start_point.y - self.end_point.y).powi(2);
        let delta_z_sq = (self.start_point.z - self.end_point.z).powi(2);
        (delta_x_sq + delta_y_sq + delta_z_sq).sqrt()
    }
}
