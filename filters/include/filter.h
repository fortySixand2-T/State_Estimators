#include <vector>
#include <Eigen/Dense>

class Filter
{
public:
    Filter(){};
    ~Filter(){};
private:
    virtual void predict() = 0;
    virtual void update() = 0;
};
