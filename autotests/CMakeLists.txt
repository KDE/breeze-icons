remove_definitions(-DQT_NO_CAST_FROM_ASCII)

include(ECMAddTests)

if(BUILD_TESTING)
    find_package(Qt5 ${REQUIRED_QT_VERSION} CONFIG REQUIRED Core Test)
    find_package(KF5Config 5.0 QUIET)
    find_package(KF5IconThemes 5.0 QUIET)

    set_package_properties(KF5Config PROPERTIES
                                     PURPOSE "Auto tests"
                                     TYPE OPTIONAL)
    set_package_properties(KF5IconThemes PROPERTIES
                                     PURPOSE "Auto tests"
                                     TYPE OPTIONAL)


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
    if (KF5::IconThemes AND KF5::ConfigCore)
        ecm_add_test(scalabletest.cpp
            TEST_NAME "scalable"
            LINK_LIBRARIES Qt5::Test KF5::IconThemes KF5::ConfigCore
        )
    endif()
endif()
