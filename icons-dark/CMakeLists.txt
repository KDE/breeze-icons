########### install files ###############

FILE(GLOB possible_icon_dirs RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/*)
SET(breeze_icon_dark_dirs "")
FOREACH(possible_icon_dir ${possible_icon_dirs})
    IF(IS_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${possible_icon_dir})
        LIST(APPEND breeze_icon_dark_dirs ${possible_icon_dir})
    ENDIF()
ENDFOREACH()

set(BREEZE_INSTALL_DIR ${KDE_INSTALL_FULL_ICONDIR}/breeze-dark)

set(ICON_GEN_DIR ${CMAKE_BINARY_DIR}/breeze-icons-dark)
if(WITH_ICON_GENERATION)
    # No trainling slashes on dirs. It will break scripts.
    add_custom_target(breeze-generate-symbolic-dark ALL
        COMMENT "Generating symbolic dark icons"
        COMMAND $<TARGET_FILE:generate-symbolic-dark> ${CMAKE_SOURCE_DIR}/icons ${ICON_GEN_DIR}
    )
    # Auto-generate 24px monochrome icons from 22px versions
    add_custom_target(breeze-generate-24px-versions-dark ALL
        DEPENDS breeze-generate-symbolic-dark
        COMMENT "Generating 24px icons-dark"
        COMMAND ${Python_EXECUTABLE} ${CMAKE_SOURCE_DIR}/generate-24px-versions.py
                ${CMAKE_CURRENT_SOURCE_DIR} ${ICON_GEN_DIR}
                ${ICON_GEN_DIR}
    )
else()
    # create the target dir, we need it for resource creation
    add_custom_target(breeze-generate-24px-versions-dark ALL
        COMMENT "Generating 24px icons-dark placeholder"
        COMMAND ${CMAKE_COMMAND} -E make_directory ${ICON_GEN_DIR}
    )
endif()

if(NOT SKIP_INSTALL_ICONS)
    install(DIRECTORY ${breeze_icon_dark_dirs} DESTINATION ${BREEZE_INSTALL_DIR})
    file(GLOB_RECURSE icon_files RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "${CMAKE_CURRENT_SOURCE_DIR}/*.svg")
    # install for all missing icons the light icons as fallback
    foreach (icon_file ${BREEZE_LIGHT_ICONS})
        if (NOT ${icon_file} IN_LIST icon_files)
            install(FILES ${CMAKE_SOURCE_DIR}/icons/${icon_file} DESTINATION ${BREEZE_INSTALL_DIR} RENAME ${icon_file})
        endif()
    endforeach()

    install(FILES index.theme DESTINATION ${BREEZE_INSTALL_DIR})
    if(NOT WIN32)
        install(DIRECTORY ${CMAKE_BINARY_DIR}/icons/aliases/ DESTINATION ${BREEZE_INSTALL_DIR})
    endif()
    if(WITH_ICON_GENERATION)
        install(DIRECTORY ${ICON_GEN_DIR}/ DESTINATION ${BREEZE_INSTALL_DIR})
    endif()
endif()

gtk_update_icon_cache(${BREEZE_INSTALL_DIR})
