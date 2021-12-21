//
// Created by psycho on 19.12.2021.
//

#ifndef CPP_LIB_QUEUE_H
#define CPP_LIB_QUEUE_H

#include <boost/python.hpp>
#include <utility>

using namespace boost;

struct queue_item{
  python::object value;
  queue_item *next;
  explicit queue_item(python::object value);
};

class queue {
  queue_item *first;
  queue_item *last;
  uint size;
public:
  queue();
  void add(python::object value);
  python::object next();
  python::object get_first();
  python::object get_last();
  bool is_empty();
  [[nodiscard]] uint get_size() const;
};


#endif //CPP_LIB_QUEUE_H
