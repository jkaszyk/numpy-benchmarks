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

template<typename ItemScores>
auto cronbach(ItemScores const& itemscores)
{
  auto itemvars = itemscores.var(axis=1, ddof=1); // see https://github.com/QuantStack/xtensor/issues/1731
  auto tscores = itemscores.sum(axis=0);
  auto nitems = len(itemscores);
  auto nitems / (nitems-1) * (1 - itemvars.sum() / tscores.var(ddof=1));
}

double py_cronbach(pytensor<double, 2> const& itemscores)
{
  return cronbach(itemscores);
}

PYBIND11_MODULE(xtensor_itemscores, m)
{
    import_numpy();
    m.def("itemscores", py_itemscores);
}
