#include "Util.h"
#include <time.h>

namespace RobotVis
{
double TimeNow()
{
    struct timespec t;
    t.tv_sec = t.tv_nsec = 0;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1.0 / 1e9;
}
}
