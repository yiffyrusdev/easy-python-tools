//
// Created by psycho on 20.12.2021.
//

#ifndef CPP_LIB_TREES_H
#define CPP_LIB_TREES_H

#include <boost/python.hpp>
#include "binary_tree.h"
#include "prefix_tree.h"

using namespace boost::python;

BOOST_PYTHON_MODULE(trees){
  class_<binary_tree>("BinaryTree")
          .def("add", &binary_tree::add)
          .def("is_empty", &binary_tree::is_empty)
          .def("contains", &binary_tree::contains)
          .add_property("depth", &binary_tree::get_depth)
          ;
  class_<prefix_tree>("PrefixTree")
          .def("add", &prefix_tree::add)
          .def("contains", &prefix_tree::contains)
          .def("count", &prefix_tree::count)
          ;
}

#endif //CPP_LIB_TREES_H
