#include "filters/include/filter.h"
#include "filters/motion_models/constant_acceleration_model.h"

class KalmanFilter : public Filter
{
public:
    KalmanFilter(){};
    ~KalmanFilter(){};
private:
    void predict();
    void update();
    Eigen::MatrixXd kalman_gain_;
    ConstantAccelerationModel motion_model;
};

void KalmanFilter::predict()
{

}
