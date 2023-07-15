#include "Eigen/Dense"
#include "filters/datatypes/constants.h"

class position_only_measurement
{
public:
    position_only_measurement(PositionOnlyMeasurementParameter params) : column_size_{params.column_size},
                                                                         measurement_noise_{params.measurement_noise}
    {
        measurement_matrix_.resize(row_size_,column_size_);
        measurement_matrix_.setZero(row_size_,column_size_);
        measurement_matrix_[0][row_size_-1] = 1;
        measurement_matrix_[row_size_-1][0] = 1;
    }

    const Eigen::Matrix<double,row_size_,column_size_> getMeasurementmatrix(){ return this->measurement_matrix_;}
private:
    const std::uint32_t row_size_{2};
    const std::uint32_t column_size_;
    const Eigen::MatrixXd measurement_matrix_;
    const Eigen::Matrix<double,2,2> measurement_noise_;
};