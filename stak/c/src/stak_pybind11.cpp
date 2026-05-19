#include "stak_pybind11.h"

#include <pybind11/pybind11.h>

#include "stak_interface.h"


namespace py = pybind11;


PYBIND11_MODULE(c_stak, m) {
    m.doc() = "stak_c Python bindings";

    m.def("stak_init", &stak_init, "Initialize STAK");

    m.def("stak_set_is_dev", [](bool isDev) {
    	stak_set_is_dev(isDev ? 1 : 0);
	});

}