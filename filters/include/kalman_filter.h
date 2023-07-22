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

}
