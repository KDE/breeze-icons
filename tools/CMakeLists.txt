include(ECMMarkNonGuiExecutable)

if (CMAKE_CROSSCOMPILING AND KF6_HOST_TOOLING)
    find_program(GENERATE_SYMBOLIC_DARK generate-symbolic-dark PATHS ${KF6_HOST_TOOLING} NO_CACHE NO_CMAKE_FIND_ROOT_PATH)
    find_program(QRC_ALIAS qrcAlias PATHS ${KF6_HOST_TOOLING} NO_CACHE NO_CMAKE_FIND_ROOT_PATH)
    if (GENERATE_SYMBOLIC_DARK)
        add_executable(generate-symbolic-dark IMPORTED GLOBAL)
        set_target_properties(generate-symbolic-dark PROPERTIES IMPORTED_LOCATION
                              ${GENERATE_SYMBOLIC_DARK})
        message (STATUS "Using generate-symbolic-dark from '${GENERATE_SYMBOLIC_DARK}'")
    else ()
        message (WARNING "Could not find generate-symbolic-dark in '${KF6_HOST_TOOLING}'.")
    endif ()

    if (QRC_ALIAS)
        add_executable(qrcAlias IMPORTED GLOBAL)
        set_target_properties(qrcAlias PROPERTIES IMPORTED_LOCATION
                              ${QRC_ALIAS})
        message (STATUS "Using qrcAlias from '${QRC_ALIAS}'")
    else ()
        message (WARNING "Could not find qrcAlias in '${KF6_HOST_TOOLING}'.")
    endif ()
else ()
    # takes light theme icons and makes modified copies of them with dark theme stylesheets
    add_executable(generate-symbolic-dark generate-symbolic-dark.cpp)
    target_link_libraries(generate-symbolic-dark PRIVATE Qt6::Core)
    ecm_mark_nongui_executable(generate-symbolic-dark)
    if (INSTALL_HOST_TOOLS)
        install(TARGETS generate-symbolic-dark ${KF_INSTALL_TARGETS_DEFAULT_ARGS})
    endif()


    # qrc generator
    add_executable(qrcAlias qrcAlias.cpp)
    target_link_libraries(qrcAlias PRIVATE Qt6::Core)
    ecm_mark_nongui_executable(qrcAlias)
    if (INSTALL_HOST_TOOLS)
        install(TARGETS qrcAlias ${KF_INSTALL_TARGETS_DEFAULT_ARGS})
    endif()
endif ()
