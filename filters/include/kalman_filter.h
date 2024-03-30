#include "filters/include/filter.h"
#include "filters/motion_models/constant_acceleration_model.h"
#include "filters/measurement_models/position_measurement.h"
#include "filters/datatypes/constants.h"

template<typename MotionModel, typename MeasurementModel>
class KalmanFilter : public Filter
{
public:
    KalmanFilter():motion_model_(),measurement_model_{motion_model_.getStateVectorSize()}{};
    // KalmanFilter(const PositionOnlyMeasurementParameter params): measurement_model_{params};
    ~KalmanFilter(){};
    // void updateKalmanGain();
private:
    void predict(const double delta_t);
    void update(Eigen::MatrixXd& measurement);
    double delta_t_{0.04};
    Eigen::MatrixXd kalman_gain_;
    MotionModel motion_model_;
    MeasurementModel measurement_model_;
};

void KalmanFilter::predict(const double delta_t)
{
    assert(delta_t > 0.0);
    motion_model_.transitionStatesForward(delta_t);
}

// void KalmanFilter::updateKalmanGain()
// {
    // Eigen::Matrix<double, 6, 6> tmp_covariance_mat{ this->motion_model_.getCovarianceMat() };
    // const std::uint32_t meas_model_rows{ this->measurement_model_.getMeasurementMatrixRows() };
    // const std::uint32_t meas_model_cols{ this->measurement_model_.getMeasurementMatrixCols() };
    // const std::uint32_t meas_noise_rows{ this->measurement_model_.getMeasurementNoiseRows() };
    // const std::uint32_t meas_noise_cols{ this->measurement_model_.getMeasurementNoise() };
    // Eigen::Matrix<double, meas_model_rows, meas_model_cols> measurement_mat{ this->measurement_model_.getMeasurementMatrix() };

    // Eigen::Matrix<double, meas_noise_rows, meas_noise_cols> innovation_inverse = measurement_mat * tmp_covariance_mat * measurement_mat.transpose() + measurement_model_.getMeasurementNoise();
    // this->kalman_gain_ = tmp_covariance_mat * measurement_mat.transpose() * innovation_inverse.inverse();
// }

void KalmanFilter::update(Eigen::MatrixXd& measurement)
{
    const std::uint32_t state_dimensions{ this->motion_model_.getStateVectorSize() };
    Eigen::Matrix<double, state_dimensions, state_dimensions> tmp_covariance_mat{ this->motion_model_.getCovarianceMat() };
    Eigen::Matrix<double, state_dimensions, 1> current_states{ this->motion_model_.getStatesInMatrix() };

    const std::uint32_t meas_model_rows{ this->measurement_model_.getMeasurementMatrixRows() };
    const std::uint32_t meas_model_cols{ this->measurement_model_.getMeasurementMatrixCols() };
    const std::uint32_t meas_noise_rows{ this->measurement_model_.getMeasurementNoiseRows() };
    const std::uint32_t meas_noise_cols{ this->measurement_model_.getMeasurementNoise() };
    Eigen::Matrix<double, meas_model_rows, meas_model_cols> measurement_mat{ this->measurement_model_.getMeasurementMatrix() };

    Eigen::Matrix<double, meas_noise_rows, meas_noise_cols> 
                    innovation_inverse = measurement_mat * tmp_covariance_mat * measurement_mat.transpose()
                                         + measurement_model_.getMeasurementNoise();
    this->kalman_gain_ = tmp_covariance_mat * measurement_mat.transpose() * innovation_inverse.inverse();

    Eigen::Matrix<double,meas_model_rows, meas_model_rows> y = measurement - measurement_mat * current_states;

    //Update the State and Covariance
    const auto update_states = current_states + this->kalma_gain_ * y;
    this->motion_model_.updateCurrentStates(update_states);
    const auto update_covariance_mat = (Eigen::Matrix<double, state_dimensions, state_dimensions>::Identity() 
                                        - this->kalma_gain_ * measurement_mat) * tmp_covariance_mat;
    this->motion_model_.updateCovarianceMatrix(update_covariance_mat);
}
