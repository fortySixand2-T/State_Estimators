template <class T>
class State
{
public:
    State(T state_val):state_value_{state_val}{};
    State():state_value_{static_cast<T>(0.0)}{};
    T getStateValue(){return this->state_value_;}
    void updateStateValue(T state_val){ state_value_ = state_val;}
private:
    T state_value_;
};
