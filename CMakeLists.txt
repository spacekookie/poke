cmake_minimum_required(VERSION 3.6)
set(CMAKE_CXX_STANDARD 11)

# Set some flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c11")
set(CMAKE_BUILD_TYPE Debug)

# Add libdtree as a subfolder for linking later
add_subdirectory(libdtree)

# Define our project for future reference
project(poke)

# Define files for libpoke
set(LIBPOKE_SRC
        lib/parser.c
        lib/sessions.c
        lib/keywoman.c)

# Define libpoke library with dependencies
add_library(libpoke STATIC ${LIBPOKE_SRC})

# Add some libraries to libpoke
target_link_libraries(libpoke
        libdyntree
        config
        ssh)

# Officially add our file scopes
target_include_directories(libpoke PUBLIC "include")
target_include_directories(libpoke PRIVATE "lib")

#########################################################

# Define files for libpoke
set(POKE_SRC
        src/main.c)

# Then add the executable
add_executable(poke ${POKE_SRC})
target_link_libraries(poke libpoke)