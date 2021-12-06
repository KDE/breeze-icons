if(BINARY_ICONS_RESOURCE)
    generate_binary_resource(icons-dark binary_resource)
endif()

########### install files ###############

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
    file(GLOB_RECURSE icon_files RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "${CMAKE_CURRENT_SOURCE_DIR}/*.svg")
    foreach (icon_file ${icon_files})
        install(FILES ${icon_file} DESTINATION ${BREEZE_INSTALL_DIR} RENAME ${icon_file})
    endforeach()

    # install for all missing icons the light icons as fallback
    foreach (icon_file ${BREEZE_LIGHT_ICONS})
        if (NOT ${icon_file} IN_LIST icon_files)
            install(FILES ${CMAKE_SOURCE_DIR}/icons/${icon_file} DESTINATION ${BREEZE_INSTALL_DIR} RENAME ${icon_file})
        endif()
    endforeach()

    install(FILES index.theme DESTINATION ${BREEZE_INSTALL_DIR})
    if(WITH_ICON_GENERATION)
        install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated/ DESTINATION ${BREEZE_INSTALL_DIR})
    endif()
endif()

gtk_update_icon_cache(${BREEZE_INSTALL_DIR})

if(BINARY_ICONS_RESOURCE)
    install(FILES ${binary_resource} DESTINATION ${BREEZE_INSTALL_DIR})
endif()
