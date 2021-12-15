if(BINARY_ICONS_RESOURCE)
    generate_binary_resource(icons binary_resource)
endif()

########### install files ###############

FILE(GLOB possible_icon_dirs RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/*)
SET(breeze_icon_dirs "")
FOREACH(possible_icon_dir ${possible_icon_dirs})
    IF(IS_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${possible_icon_dir})
        LIST(APPEND breeze_icon_dirs ${possible_icon_dir})
    ENDIF()
ENDFOREACH()

set(BREEZE_INSTALL_DIR ${KDE_INSTALL_FULL_ICONDIR}/breeze)

if(WITH_ICON_GENERATION)
    # Auto-generate 24px monochrome icons from 22px versions
    add_custom_target(breeze-generate-24px-versions ALL
        COMMENT "Generating 24px icons"
        COMMAND ${Python_EXECUTABLE} ${CMAKE_SOURCE_DIR}/generate-24px-versions.py ${CMAKE_CURRENT_BINARY_DIR}/generated/
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )
endif()

if(NOT WIN32)
    if (TARGET breeze-validate-svg AND WITH_ICON_GENERATION)
        add_dependencies(breeze-validate-svg breeze-generate-24px-versions)
    endif()
endif()

if(NOT SKIP_INSTALL_ICONS)
    install(DIRECTORY ${breeze_icon_dirs} DESTINATION ${BREEZE_INSTALL_DIR})
    # collect all our icons we need to install, will be used by dark icon set as fallback icons if not there, too
    file(GLOB_RECURSE icon_files RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "${CMAKE_CURRENT_SOURCE_DIR}/*.svg")
    set(BREEZE_LIGHT_ICONS ${icon_files} PARENT_SCOPE)

    install(FILES index.theme DESTINATION ${BREEZE_INSTALL_DIR})
    if(WITH_ICON_GENERATION)
        install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated/ DESTINATION ${BREEZE_INSTALL_DIR})
    endif()
endif()

gtk_update_icon_cache(${BREEZE_INSTALL_DIR})

if(BINARY_ICONS_RESOURCE)
    install(FILES ${binary_resource} DESTINATION ${BREEZE_INSTALL_DIR})
endif()
