#include "filters/include/filter.h"
#include "filters/motion_models/constant_acceleration_model.h"
#include "filters/measurement_models/position_measurement.h"
#include "filters/datatypes/constants.h"

class KalmanFilter : public Filter
{
public:
    KalmanFilter(){};
    KalmanFilter(const PositionOnlyMeasurementParameter params): measurement_model_{params};
    ~KalmanFilter(){};
    void updateKalmanGain();
private:
    void predict(const double delta_t);
    void update();
    double delta_t_{0.04};
    Eigen::MatrixXd kalman_gain_;
    ConstantAccelerationModel motion_model_;
    PositionMeasurement measurement_model_;
};

void KalmanFilter::predict(const double delta_t)
{
    assert(delta_t > 0.0);
    motion_model_.transitionStatesForward(delta_t);
    updateKalmanGain();
}

void KalmanFilter::updateKalmanGain()
{
    Eigen::Matrix<double, 6, 6> tmp_covariance_mat{ this->motion_model_.getCovarianceMat() };
    const std::uint32_t meas_model_rows{ this->measurement_model_.getMeasurementMatrixRows() };
    const std::uint32_t meas_model_cols{ this->measurement_model_.getMeasurementMatrixCols() };
    const std::uint32_t meas_noise_rows{ this->measurement_model_.getMeasurementNoiseRows() };
    const std::uint32_t meas_noise_cols{ this->measurement_model_.getMeasurementNoise() };
    Eigen::Matrix<double, meas_model_rows, meas_model_cols> measurement_mat{ this->measurement_model_.getMeasurementMatrix() };

    Eigen::Matrix<double, meas_noise_rows, meas_noise_cols> innovation_inverse = measurement_mat * tmp_covariance_mat * measurement_mat.transpose() + measurement_model_.getMeasurementNoise();
    this->kalman_gain_ = tmp_covariance_mat * measurement_mat.transpose() * innovation_inverse.inverse();
}

void KalmanFilter::update()
{
    
}