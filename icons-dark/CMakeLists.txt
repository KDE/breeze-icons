if(BINARY_ICONS_RESOURCE)
    generate_binary_resource(icons-dark binary_resource)
endif()

########### install files ###############

set(breeze_icon_dark_dirs
    actions animations applets apps devices emblems
    mimetypes places status)

set(BREEZE_INSTALL_DIR ${KDE_INSTALL_FULL_ICONDIR}/breeze-dark)

if(WITH_ICON_GENERATION)
    # Auto-generate 24px monochrome icons from 22px versions
    add_custom_target(breeze-generate-24px-versions-dark ALL
        COMMENT "Generating 24px icons-dark"
        COMMAND ${Python_EXECUTABLE} ${CMAKE_SOURCE_DIR}/generate-24px-versions.py ${CMAKE_CURRENT_BINARY_DIR}/generated/
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )
endif()

if(NOT WIN32)
    if (TARGET breeze-validate-svg AND WITH_ICON_GENERATION)
        add_dependencies(breeze-validate-svg breeze-generate-24px-versions-dark)
    endif()
endif()

if(NOT SKIP_INSTALL_ICONS)
    # In order to ensure the dark icons are copied over the light icons which
    # are installed into the dark theme for BUG:444095, we need to execute the
    # copy command ourselves rather than using CMake's internal copy mechanism
    # used by the normal install command, so we use CODE mode of install to
    # execute_process and print an appropriate status message.
    # See https://bugs.kde.org/show_bug.cgi?id=445489
    set(COPY_CMD "cp -a")
    set(XCOPY_ARGS "")
    if(WIN32)
        set(COPY_CMD "xcopy")
        set(XCOPY_ARGS "/q /e /y")
    endif(WIN32)
    install(CODE "cmake_policy(VERSION 3.6)
        foreach(CAT_DIR ${breeze_icon_dark_dirs})
            execute_process(COMMAND ${COPY_CMD} \${CAT_DIR} \"\$ENV{DESTDIR}${BREEZE_INSTALL_DIR}\" ${XCOPY_ARGS} ERROR_QUIET WORKING_DIRECTORY \"${CMAKE_CURRENT_SOURCE_DIR}\" COMMAND_ERROR_IS_FATAL LAST)
        endforeach()
        file(GLOB_RECURSE ICON_FILES RELATIVE \"${CMAKE_CURRENT_SOURCE_DIR}\" LIST_DIRECTORIES false \"${CMAKE_CURRENT_SOURCE_DIR}/*.svg\")
        foreach(ICON_FILE IN LISTS ICON_FILES)
            message(STATUS \"Installing: \$ENV{DESTDIR}${BREEZE_INSTALL_DIR}/\${ICON_FILE}\")
        endforeach()")
    install(FILES index.theme DESTINATION ${BREEZE_INSTALL_DIR})
    if(WITH_ICON_GENERATION)
        install(CODE "cmake_policy(VERSION 3.6)
            foreach(GEN_DIR ${breeze_icon_dark_dirs})
                execute_process(COMMAND ${COPY_CMD} \${GEN_DIR} \"\$ENV{DESTDIR}${BREEZE_INSTALL_DIR}\" ${XCOPY_ARGS} ERROR_QUIET WORKING_DIRECTORY \"${CMAKE_CURRENT_BINARY_DIR}/generated\" COMMAND_ERROR_IS_FATAL LAST)
            endforeach()
            file(GLOB_RECURSE ICON_FILES RELATIVE \"${CMAKE_CURRENT_BINARY_DIR}/generated\" LIST_DIRECTORIES false \"${CMAKE_CURRENT_BINARY_DIR}/generated/*.svg\")
            foreach(ICON_FILE IN LISTS ICON_FILES)
                message(STATUS \"Installing: \$ENV{DESTDIR}${BREEZE_INSTALL_DIR}/\${ICON_FILE}\")
            endforeach()")
    endif()
endif()

gtk_update_icon_cache(${BREEZE_INSTALL_DIR})

if(BINARY_ICONS_RESOURCE)
    install(FILES ${binary_resource} DESTINATION ${BREEZE_INSTALL_DIR})
endif()
