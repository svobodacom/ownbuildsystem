cmake_minimum_required(VERSION 3.10)
set(PROJECT_NAME FightClubGame)
project(${PROJECT_NAME} VERSION 1.0.0)

# set the directory for saving build files
#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG   ${CMAKE_BINARY_DIR}/bin/Debug)
#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/bin/Release)
#set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# set some properties in Visual Studio (ON OFF - its the same like TRUE FALSE)
set_property(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT ${PROJECT_NAME})
set_property(GLOBAL PROPERTY USE_FOLDERS ON)
set(CMAKE_SUPPRESS_REGENERATION TRUE)

# cpp options
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

#sources and variables
set(SOURCES Main.cpp)
set(MATH_SOURCES Math.cpp)
set(MATH_INCLUDES Math.h)
set(DLL_GAME_SOURCES Character.cpp Weapon.cpp)
set(DLL_GAME_INCLUDES Character.h Weapon.h)

# targets
add_executable(${PROJECT_NAME} ${SOURCES})
add_library(MathLib STATIC ${MATH_SOURCES} ${MATH_INCLUDES})
add_library(GameLib SHARED ${DLL_GAME_SOURCES} ${DLL_GAME_INCLUDES})

#preprocessing
target_compile_definitions(GameLib PRIVATE _EXPORTING)
target_compile_definitions(${PROJECT_NAME} PUBLIC _IMPORTING)

#link the library
target_link_libraries(GameLib PRIVATE MathLib)
target_link_libraries(${PROJECT_NAME} PRIVATE GameLib)
#target_link_libraries(${PROJECT_NAME} PRIVATE MathLib)

# .lib/.dll/.exe куда класть
set_target_properties(MathLib PROPERTIES ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set_target_properties(GameLib PROPERTIES 
    ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set_target_properties(${PROJECT_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

message("Using ${CMAKE_CXX_COMPILER_ID} compiler")

if(MSVC)
    message("MSVC version: ${MSVC_VERSION}")
    target_compile_options(${PROJECT_NAME} PRIVATE /FAc)
endif()

message("---------------- Project files generation -----------------")
message("Compiler flags: ${CMAKE_CXX_FLAGS}")
message("Compiler DEBUG flags: ${CMAKE_CXX_FLAGS_DEBUG}")