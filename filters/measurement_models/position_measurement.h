#include "Eigen/Dense"
#include "filters/datatypes/constants.h"

class PositionMeasurement
{
public:
    PositionMeasurement(const PositionOnlyMeasurementParameter params) : column_size_{params.column_size},
                                                                         measurement_noise_{params.measurement_noise}
    {
        initializeMeasurementMatrix();
    }

    PositionMeasurement(const std::uint32_t column_size) : column_size_{column_size}
    {
        initializeMeasurementMatrix();
        initializeMeasurementNoise();
    }

    PositionMeasurement(const Eigen::Vector2d measurement_noise_vector)
    {
        measurement_noise_[0][0] = measurement_noise_vector[0];
        measurement_noise_[1][1] = measurement_noise_vector[1];
        initializeMeasurementMatrix();
    }

    const Eigen::Matrix<double, row_size_, column_size_> getMeasurementMatrix(){ return this->measurement_matrix_;}
    const Eigen::Matrix<double, 2, 2> getMeasurementNoise(){ return this->measurement_noise_;}
    const std::uint32_t getMeasurementMatrixRows(){ return this->row_size_;}
    const std::uint32_t getMeasurementMatrixCols(){ return this->column_size_;}
    const auto getMeasurementNoiseRows(){ return static_cast<std::uint32_t>(this->measurement_noise_.rows());}
    const auto getMeasurementNoiseCols(){ return static_cast<std::uint32_t>(this->measurement_noise_.cols());}

private:

    void initializeMeasurementMatrix();
    void initializeMeasurementNoise();
    const std::uint32_t row_size_{2};
    const std::uint32_t column_size_;
    const Eigen::MatrixXd measurement_matrix_;
    const Eigen::Matrix<double, 2, 2> measurement_noise_;
};

void PositionMeasurement::initializeMeasurementMatrix()
{
    this->measurement_matrix_.resize(row_size_,column_size_);
    this->measurement_matrix_.setZero(row_size_,column_size_);
    this->measurement_matrix_[0][row_size_-1] = 1;
    this->measurement_matrix_[row_size_-1][0] = 1;
}

void PositionMeasurement::initializeMeasurementNoise()
{
    this->measurement_noise_.setIdentity();

}