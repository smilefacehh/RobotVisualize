cmake_minimum_required(VERSION 3.0.2)

project(robot_vis)

add_definitions(-std=c++11 -O3)

find_package(catkin REQUIRED COMPONENTS
        roscpp)

find_package(Threads REQUIRED)

catkin_package()

include_directories(
        ${catkin_INCLUDE_DIRS})

FILE(GLOB ALL_SOURCES "./src/*.cpp")
FILE(GLOB ALL_INCLUDES "./src/*.h")
set(ALL_SRCS ${ALL_SOURCES} ${ALL_INCLUDES})

add_executable(${PROJECT_NAME} ${ALL_SRCS})

target_link_libraries(${PROJECT_NAME}
        ${catkin_LIBRARIES}
        Threads::Threads
        curl)