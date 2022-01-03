//
// Created by psycho on 19.12.2021.
//

#ifndef CPP_LIB_PRIMITIVES_H
#define CPP_LIB_PRIMITIVES_H

#include <boost/python.hpp>
#include "stack.h"
#include "queue.h"

BOOST_PYTHON_MODULE(primitives)
{
  class_<stack>("Stack")
          .def("push", &stack::push)
          .def("pop", &stack::pop)
          .def("is_empty", &stack::is_empty)
          .add_property("top", &stack::top)
          .add_property("size", &stack::get_size);

  class_<queue>("Queue")
          .def("add", &queue::add)
          .def("next", &queue::next)
          .def("is_empty", &queue::is_empty)
          .add_property("first", &queue::get_first)
          .add_property("last", &queue::get_last)
          .add_property("size", &queue::get_size);
}

#endif //CPP_LIB_PRIMITIVES_H
