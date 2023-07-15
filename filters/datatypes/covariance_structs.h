#include "Eigen/Dense"

struct variance_const_acceleration_params
{
    Eigen::Vector2d sigma_position;
    Eigen::Vector2d sigma_velocity;
    Eigen::Vector2d sigma_acceleration;
};