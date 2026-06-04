cmake_minimum_required(VERSION 3.5)

project(SAAS-HC)

set(CMAKE_CXX_STANDARD 17)

set(OMP_NUM_THREADS 1)
set(ENV{OMP_NUM_THREADS} 1)

add_compile_options(-DARMA_DONT_USE_OPENMP)

include_directories($ENV{CONDA_PREFIX}/include)

file(GLOB MAIN_SRC "./*.cpp")

add_executable(acothop ${MAIN_SRC})