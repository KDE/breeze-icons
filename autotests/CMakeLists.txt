include(ECMAddTests)

if(BUILD_TESTING)
    find_package(Qt6 ${REQUIRED_QT_VERSION} CONFIG REQUIRED Core Test)

    configure_file(testdata.h.cmake ${CMAKE_CURRENT_BINARY_DIR}/testdata.h)
    ecm_add_test(scalabletest.cpp
        TEST_NAME "scalable"
        LINK_LIBRARIES Qt6::Test
    )
    if(WITH_ICON_GENERATION)
        add_test(NAME "test24x24icons" COMMAND ${Python_EXECUTABLE} ${CMAKE_SOURCE_DIR}/autotests/test24x24icons.py
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        )
    endif()
endif()
