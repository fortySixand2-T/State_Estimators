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
        initializeStateTransitionMat();
        initializeProcessNoise();
    }
    ConstantAccelerationModel(variance_const_acceleration_params variance_vector):
                                state_size_{6U},
                                variance_vector_{variance_vector},
    {
        initializeStates();
        initializeCovarianceMat();
        initializeStateTransitionMat();
        initializeProcessNoise();
    }

    ConstantAccelerationModel(variance_const_acceleration_params variance_vector, Eigen::Matrix<double,6,1>& states):
                                state_size_{6U},
                                variance_vector_{variance_vector} 
    {
        updateCurrentStates(states);
        initializeCovarianceMat();
        initializeStateTransitionMat();
        initializeProcessNoise();
    }

    const auto getCurrentStates(){return states_;}
    const std::uint32_t getNumberOfStates(){ return this->state_size_;}
    Eigen::Matrix<double, 6, 6> getCovarianceMat(){return this->covariance_matrix_;}
    Eigen::Matrix<double, 6, 6> getStateTransitionMat(){return this->state_transition_matrix_;}
    Eigen::Matrix<double, 6, 6> getProccessNoise(){ return this->process_noise_;}
    const auto getVarianceVector(){return this->variance_vector_;} const
    
    void transitionStatesForward(const double delta_time);

    void updateCovarianceMatrix(const Eigen::Matrix <double, 6, 6>& kalman_updated_covariance_matrix)
    {
        this->covariance_matrix_ = kalman_updated_covariance_matrix;
    }
    void updateCurrentStates(const Eigen::Matrix <double, 6, 1>& kalman_updated_states);

    void updateStateTransitionMat(const double delta_t);

    void updateProcessNoise(const double delta_t);

    void updateCovarianceMatrix();

private:
    void initializeVarianceToDefaults();
    void initializeStates();
    void initializeCovarianceMat();
    void initializeStateTransitionMat();
    void initializeProcessNoise();

    const variance_const_acceleration_params variance_vector_;
    const std::uint32_t state_size_;
    constant_acceleration_states states_;
    Eigen::Matrix<double, 6, 6> covariance_matrix_;
    Eigen::Matrix<double, 6, 6> state_transition_matrix_;
    Eigen::Matrix<double, 6, 6> process_noise_;
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
    updateStateTransitionMat(delta_time);
    updateProcessNoise(delta_time);
    updateCovarianceMatrix();
    
    Eigen::Matrix<double, 6, 1> state_vector{};

    state_vector[4][0] = states_.acceleration_x.getStateValue();
    state_vector[5][0] = states_.acceleration_y.getStateValue();

    double velocity_x{states_.velocity_x.getStateValue()};
    double velocity_y{states_.velocity_y.getStateValue()};
    
    state_vector[2][0] += velocity_x + state_vector[4][0] * delta_time;
    state_vector[3][0] += velocity_y + state_vector[5][0] * delta_time;

    double position_x{states_.position_x.getStateValue()};
    double position_y{states_.position_y.getStateValue()};

    state_vector[0][0] = position_x + delta_time * state_vector[2][0] + state_vector[4][0] * delta_time * delta_time;
    state_vector[1][0] = position_y + delta_time * state_vector[3][0] + state_vector[5][0] * delta_time * delta_time;

    updateCurrentStates(state_vector);
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
    covariance_matrix_.setZero();
    covariance_matrix_.diagonal()[0] = variance_vector_.sigma_position[0];
    covariance_matrix_.diagonal()[1] = variance_vector_.sigma_position[1];
    covariance_matrix_.diagonal()[2] = variance_vector_.sigma_velocity[0];
    covariance_matrix_.diagonal()[3] = variance_vector_.sigma_velocity[1];
    covariance_matrix_.diagonal()[4] = variance_vector_.sigma_acceleration[0];
    covariance_matrix_.diagonal()[5] = variance_vector_.sigma_acceleration[1];

}

void ConstantAccelerationModel::initializeStateTransitionMat()
{
    const double delta_t{0.04};
    updateStateTransitionMat(delta_t);
}

void ConstantAccelerationModel::initializeProcessNoise()
{
    const double delta_t{0.04};
    updateProcessNoise(delta_t);
}

void ConstantAccelerationModel::updateStateTransitionMat(const double delta_t)
{
    this->state_transition_matrix_.setIdentity();
    this->state_transition_matrix_[0][1] = delta_t;
    this->state_transition_matrix_[0][2] = std::pow(delta_t, 2)/2.0;
    
    this->state_transition_matrix_[1][2] = delta_t;

    this->state_transition_matrix_[3][4] = delta_t;
    this->state_transition_matrix_[3][5] = std::pow(delta_t, 2)/2.0;

    this->state_transition_matrix_[4][5] = delta_t;
}

void ConstantAccelerationModel::updateProcessNoise(const double delta_t)
{
    this->process_noise_.setZero();
    this->process_noise_[0][0] = std::pow(delta_t,4.0)/4.0;
    this->process_noise_[0][1] = std::pow(delta_t,3.0)/2.0;
    this->process_noise_[0][2] = std::pow(delta_t,2.0)/2.0;

    this->process_noise_[1][0] = std::pow(delta_t,3.0)/2.0;
    this->process_noise_[1][1] = std::pow(delta_t,2.0);
    this->process_noise_[1][2] = delta_t;

    this->process_noise_[2][0] = std::pow(delta_t,2.0)/2.0;
    this->process_noise_[2][1] = delta_t;
    this->process_noise_[2][2] = 1.0;

    this->process_noise_[3][3] = std::pow(delta_t,4.0)/4.0;
    this->process_noise_[3][4] = std::pow(delta_t,3.0)/2.0;
    this->process_noise_[3][5] = std::pow(delta_t,2.0)/2.0;

    this->process_noise_[4][3] = std::pow(delta_t,3.0)/2.0;
    this->process_noise_[4][4] = std::pow(delta_t,2.0);
    this->process_noise_[4][5] = delta_t;

    this->process_noise_[5][3] = std::pow(delta_t,2.0)/2.0;
    this->process_noise_[5][4] = delta_t;
    this->process_noise_[5][5] = 1.0;

    this->process_noise_ = this->process_noise_ * variance_vector_.sigma_acceleration[0];
}

void ConstantAccelerationModel::updateCovarianceMatrix()
{
    assert(delta_t > 0.0);
    Eigen::Matrix<double, 6, 6> tmp_covariance_mat = this->getStateTransitionMat() * this->getCovarianceMat() * this->getStateTransitionMat().transpose() + this->getProccessNoise();
    this->updateCovarianceMatrix(tmp_covariance_mat);
}

void ConstantAccelerationModel::updateCurrentStates(Eigen::Matrix <double, 6, 1>& kalman_updated_states)
{
    this->states_.position_x.updateStateValue(kalman_updated_states[0][0]);
    this->states_.position_y.updateStateValue(kalman_updated_states[1][0]);
    this->states_.velocity_x.updateStateValue(kalman_updated_states[2][0]);
    this->states_.velocity_y.updateStateValue(kalman_updated_states[3][0]);
    this->states_.acceleration_x.updateStateValue(kalman_updated_states[4][0]);
    this->states_.acceleration_y.updateStateValue(kalman_updated_states[5][0]);
}