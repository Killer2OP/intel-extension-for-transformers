//  Copyright (c) 2022 Intel Corporation
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.

#ifndef ENGINE_SPARSELIB_INCLUDE_JIT_DOMAIN_JIT_BINARY_INJECTOR_HPP_
#define ENGINE_SPARSELIB_INCLUDE_JIT_DOMAIN_JIT_BINARY_INJECTOR_HPP_

#include <vector>
#include "jit_generator.hpp"
#include "utils.hpp"
#include "param_types.hpp"

namespace jd {
class jit_binary_injector {
 public:
  jit_binary_injector() {}
  virtual ~jit_binary_injector() {}
  void binary_injector_init(jit_generator* ptr);
  void set_mask(Opmask mask);
  void get_addr(Reg64 reg, binaryop_attr op_attr);  // mov addr_ptr from op_attr to reg64.
  void compute_vector(Zmm zmm_src1, RegExp src2, binaryop_attr op_attr, data_type op_dt, bool enable_mask = false,
                      bool broadcast = false);

  void add(Zmm src1, RegExp src2, data_type op_dt, bool enable_mask, bool broadcast);

 private:
  jit_generator* h;
  Opmask mask;
};
}  // namespace jd
#endif  // ENGINE_SPARSELIB_INCLUDE_JIT_DOMAIN_JIT_BINARY_INJECTOR_HPP_
