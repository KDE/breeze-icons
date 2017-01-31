remove_definitions(-DQT_NO_CAST_FROM_ASCII)

include(ECMAddTests)

find_package(Qt5 ${REQUIRED_QT_VERSION} CONFIG REQUIRED Core Test)
find_packagE(KF5Config 5.0)
find_packagE(KF5IconThemes 5.0)

configure_file(testdata.h.cmake ${CMAKE_CURRENT_BINARY_DIR}/testdata.h)
ecm_add_test(symlinktest.cpp
    TEST_NAME "symlink"
    LINK_LIBRARIES Qt5::Test
)
ecm_add_test(newlinetest.cpp
    TEST_NAME "newline"
    LINK_LIBRARIES Qt5::Test
)
ecm_add_test(dupetest.cpp
    TEST_NAME "dupe"
    LINK_LIBRARIES Qt5::Test
)
ecm_add_test(scalabletest.cpp
    TEST_NAME "scalable"
    LINK_LIBRARIES Qt5::Test KF5::IconThemes KF5::ConfigCore
)
