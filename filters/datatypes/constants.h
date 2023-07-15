#include "Eigen/Dense"

struct PositionOnlyMeasurementParameter
{
    std::uint32_t column_size;
    Eigen::Matrix<double,2,2> measurement_noise;
};