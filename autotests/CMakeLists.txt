remove_definitions(-DQT_NO_CAST_FROM_ASCII)

include(ECMAddTests)

find_package(Qt5 ${REQUIRED_QT_VERSION} CONFIG REQUIRED Core Test)

configure_file(testdata.h.cmake ${CMAKE_CURRENT_BINARY_DIR}/testdata.h)
ecm_add_test(symlinktest.cpp
    TEST_NAME "symlink"
    LINK_LIBRARIES Qt5::Test
)
