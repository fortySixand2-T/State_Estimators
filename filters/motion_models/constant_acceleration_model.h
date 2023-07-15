#include "motion_models.h"
#include "filters/datatypes/motion_model_states.h"
#include "filters/datatypes/covariance_structs.h"
#include "vector"
#include "Eigen/Dense"

// const constant_acceleration_states default_accel_states_
class ConstantAccelerationModel: public MotionModels
{
public:
    ConstantAccelerationModel(): state_size_{6U} 
    {
        initializeVarianceToDefaults();
        initializeStates();
        initializeCovarianceMat();
    }
    ConstantAccelerationModel(variance_const_acceleration_params variance_vector):
                                state_size_{6U},
                                variance_vector_{variance_vector},
    {
        initializeStates();
        initializeCovarianceMat();
    }

    ConstantAccelerationModel(variance_const_acceleration_params variance_vector, Eigen::Matrix<double,6,1>& states):
                                state_size_{6U},
                                variance_vector_{variance_vector} 
    {
        updateCurrentStates(states);
        initializeCovarianceMat();
    }
    const auto getCurrentStates(){return states_;}
    const std::uint32_t getNumberOfStates(){ return this->state_size_;}
    Eigen::Matrix<double, 6, 6> getCovarianceMat(){return this->covariance_matrix_;}
    const auto getVarianceVector(){return this->variance_vector_;} const
    
    void transitionStatesForward(const double delta_time);

    void updateCovarianceMatrix(const Eigen::Matrix <double, 6, 6>& kalman_updated_covariance_matrix)
    {
        this->covariance_matrix_ = kalman_updated_covariance_matrix;
    }
    void updateCurrentStates(const Eigen::Matrix <double, 6, 1>& kalman_updated_states);
private:
    void initializeVarianceToDefaults();
    void initializeStates();
    void initializeCovarianceMat();
    const variance_const_acceleration_params variance_vector_;
    const std::uint32_t state_size_;
    constant_acceleration_states states_;
    Eigen::Matrix<double, 6, 6> covariance_matrix_;
};

void ConstantAccelerationModel::initializeVarianceToDefaults()
{
    variance_vector_.sigma_position[0] = 5.0;
    variance_vector_.sigma_position[1] = 1.0;
    variance_vector_.sigma_velocity[0] = 0.5;
    variance_vector_.sigma_velocity[1] = 0.5;
    variance_vector_.sigma_acceleration[0] = 0.025;
    variance_vector_.sigma_acceleration[1] = 0.025;
}

void ConstantAccelerationModel::initializeStates()
{
    states_.acceleration_x.updateStateValue(variance_vector_.sigma_acceleration[0]);
    states_.acceleration_x.updateStateValue(variance_vector_.sigma_acceleration[1]);
}


void ConstantAccelerationModel::transitionStatesForward(const double delta_time)
{
    double velocity_x{states_.velocity_x.getStateValue()};
    double velocity_y{states_.velocity_y.getStateValue()};
    
    velocity_x += velocity_x + states_.acceleration_x.getStateValue * delta_time;
    velocity_y += velocity_y + states_.acceleration_y.getStateValue * delta_time;

    double position_x{states_.position_x.getStateValue()};
    double position_y{states_.position_y.getStateValue()};

    position_x = position_x + delta_time * velocity_x + states_.acceleration_x.getStateValue() * delta_time * delta_time;
    position_y = position_y + delta_time * velocity_y + states_.acceleration_y.getStateValue() * delta_time * delta_time;
}

void ConstantAccelerationModel::initializeCovarianceMat()
{
    // for(std::uint32_t i{0U}; i< covariance_matrix_.rows(); i++)
    // {
    //     if( i < 2)
    //     {
    //         covariance_matrix_.diagonal()[i] = variance_vector_.sigma_position[i%2];
    //     }
    //     else if ( (i > 1 ) && (i < 4))
    //     {
    //         covariance_matrix_.diagonal()[i] = variance_vector_.sigma_velocity[i%2];
    //     }
    //     else if ((i > 3) && (i < covariance_matrix_.rows()))
    //     {
    //         covariance_matrix_.diagonal()[i] = variance_vector_.sigma_acceleration[i%2];
    //     }
    // }
    covariance_matrix_.diagonal()[0] = variance_vector_.sigma_position[0];
    covariance_matrix_.diagonal()[1] = variance_vector_.sigma_position[1];
    covariance_matrix_.diagonal()[2] = variance_vector_.sigma_velocity[0];
    covariance_matrix_.diagonal()[3] = variance_vector_.sigma_velocity[1];
    covariance_matrix_.diagonal()[4] = variance_vector_.sigma_acceleration[0];
    covariance_matrix_.diagonal()[5] = variance_vector_.sigma_acceleration[1];

}
void ConstantAccelerationModel::updateCurrentStates(Eigen::Matrix <double, 6, 1>& kalman_updated_states)
{
    states_.position_x.updateStateValue(kalman_updated_states[0][0]);
    states_.position_y.updateStateValue(kalman_updated_states[1][0]);
    states_.velocity_x.updateStateValue(kalman_updated_states[2][0]);
    states_.velocity_y.updateStateValue(kalman_updated_states[3][0]);
    states_.acceleration_x.updateStateValue(kalman_updated_states[4][0]);
    states_.acceleration_y.updateStateValue(kalman_updated_states[5][0]);
}