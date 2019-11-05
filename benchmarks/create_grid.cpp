#include "xtensor/xnoalias.hpp"
#include "xtensor/xtensor.hpp"
#include "xtensor/xarray.hpp"
#include "xtensor/xrandom.hpp"
#include "xtensor/xview.hpp"
#include "xtensor/xfixed.hpp"
#define FORCE_IMPORT_ARRAY

#include "xtensor-python/pyarray.hpp"
#include "xtensor-python/pytensor.hpp"


using namespace xt;

template<typename X>
auto create_grid(X const& x)
{
  auto N = x.shape()[0];
  xtensor<double, 3> z = zeros<double>({N, N, 3L});
  // see https://github.com/xtensor-stack/xtensor/issues/1795
  view(z, all(), all(), 0) = x.reshape({-1, 1});
  view(z, all(), all(), 1) = x;
  auto fast_grid = z.reshape({N * N, 3L});
  return fast_grid;
}

pytensor<double, 2> py_create_grid(pytensor<double, 1> const& x)
{
  return create_grid(x);
}

PYBIND11_MODULE(xtensor_create_grid, m)
{
    import_numpy();
    m.def("create_grid", py_create_grid);
}
