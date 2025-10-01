########### install files ###############

FILE(GLOB possible_icon_dirs RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/*)
SET(breeze_icon_dirs "")
FOREACH(possible_icon_dir ${possible_icon_dirs})
    IF(IS_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${possible_icon_dir})
        LIST(APPEND breeze_icon_dirs ${possible_icon_dir})
    ENDIF()
ENDFOREACH()

if(NOT WIN32 AND NOT SKIP_INSTALL_ICONS)
    add_custom_target(create-app-symlinks ALL
        COMMENT "Creating icon symlinks for app aliases"
        COMMAND ${Python_EXECUTABLE} ${CMAKE_SOURCE_DIR}/create-app-symlinks.py ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}/aliases/
    )
endif()

set(ICON_GEN_DIR ${CMAKE_BINARY_DIR}/breeze/icons)
set(ICON_DARK_GEN_DIR ${CMAKE_BINARY_DIR}/breeze/icons-dark)
if(WITH_ICON_GENERATION)
    # Auto-generate 24px monochrome icons from 22px versions
    add_custom_target(breeze-generate-24px-versions ALL
        COMMENT "Generating 24px icons"
        COMMAND ${CMAKE_COMMAND} -E make_directory ${ICON_GEN_DIR}
        COMMAND ${CMAKE_COMMAND} -E make_directory ${ICON_DARK_GEN_DIR}
        COMMAND ${Python_EXECUTABLE} ${CMAKE_SOURCE_DIR}/generate-24px-versions.py
                ${CMAKE_CURRENT_SOURCE_DIR}
                ${ICON_GEN_DIR}
        COMMAND $<TARGET_FILE:generate-symbolic-dark> ${CMAKE_SOURCE_DIR}/icons ${ICON_GEN_DIR} ${ICON_DARK_GEN_DIR}
    )
else()
    # create the target dir, we need it for resource creation
    add_custom_target(breeze-generate-24px-versions ALL
        COMMENT "Generating 24px icons placeholder"
        COMMAND ${CMAKE_COMMAND} -E make_directory ${ICON_GEN_DIR}
        COMMAND ${CMAKE_COMMAND} -E make_directory ${ICON_DARK_GEN_DIR}
    )
endif()

# generate the two theme indices
file(COPY_FILE breeze.theme.in ${ICON_GEN_DIR}/index.theme)
file(READ commonthemeinfo.theme.in COMMON_THEME_INFO)
file(APPEND ${ICON_GEN_DIR}/index.theme ${COMMON_THEME_INFO})
file(COPY_FILE breeze-dark.theme.in ${ICON_DARK_GEN_DIR}/index.theme)
file(READ commonthemeinfo.theme.in COMMON_THEME_INFO)
file(APPEND ${ICON_DARK_GEN_DIR}/index.theme ${COMMON_THEME_INFO})

if(NOT SKIP_INSTALL_ICONS)
    # install the instantiated theme indices
    install(FILES ${ICON_GEN_DIR}/index.theme DESTINATION ${BREEZE_INSTALL_DIR})
    install(FILES ${ICON_DARK_GEN_DIR}/index.theme DESTINATION ${BREEZE_DARK_INSTALL_DIR})

    # we install icons as breeze and as fallback for breeze-dark
    # breeze-dark will overwrite some installed files with generated color patched ones

    install(DIRECTORY ${breeze_icon_dirs} DESTINATION ${BREEZE_INSTALL_DIR})
    install(DIRECTORY ${breeze_icon_dirs} DESTINATION ${BREEZE_DARK_INSTALL_DIR})

    if(NOT WIN32)
        install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/aliases/ DESTINATION ${BREEZE_INSTALL_DIR})
        install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/aliases/ DESTINATION ${BREEZE_DARK_INSTALL_DIR})
    endif()
    if(WITH_ICON_GENERATION)
        install(DIRECTORY ${ICON_GEN_DIR}/ DESTINATION ${BREEZE_INSTALL_DIR})
        install(DIRECTORY ${ICON_GEN_DIR}/ DESTINATION ${BREEZE_DARK_INSTALL_DIR})

        # generated dark icons are installed on-top
        install(DIRECTORY ${ICON_DARK_GEN_DIR}/ DESTINATION ${BREEZE_DARK_INSTALL_DIR})
    endif()

    # update the icon caches
    gtk_update_icon_cache(${BREEZE_INSTALL_DIR})
    gtk_update_icon_cache(${BREEZE_DARK_INSTALL_DIR})
endif()

