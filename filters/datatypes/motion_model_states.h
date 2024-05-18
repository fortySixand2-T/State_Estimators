#include "filters/datatypes/state.h"

struct constant_acceleration_states
{
    State<double> position_x;
    State<double> position_y;
    State<double> velocity_x;
    State<double> velocity_y;
    State<double> acceleration_x;
    State<double> acceleration_y;
};

struct constant_velocity_states
{
    State<double> position_x;
    State<double> position_y;
    State<double> velocity_x;
    State<double> velocity_y;
};

struct constant_turnrate_velocity_states
{
    State<double> position_x;
    State<double> position_y;
    State<double> velocity;
    State<double> yaw;
    State<double> yaw_dd;
};
