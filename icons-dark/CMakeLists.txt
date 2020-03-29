if(BINARY_ICONS_RESOURCE)
    generate_binary_resource(icons-dark binary_resource)
endif()

########### install files ###############

set(breeze_icon_dark_dirs
    actions animations applets apps categories preferences devices emblems
    emotes mimetypes places status)

set(BREEZE_INSTALL_DIR ${KDE_INSTALL_FULL_ICONDIR}/breeze-dark)

# Auto-generate 24px monochrome icons from 22px versions
if(NOT WIN32)
    add_custom_target(breeze-generate-24px-versions-dark ALL
        COMMENT "Generating 24px icons dark"
        COMMAND ${BASH_EXE} ${CMAKE_SOURCE_DIR}/generate-24px-versions.sh ${CMAKE_CURRENT_BINARY_DIR}/generated/
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )
    if (TARGET breeze-validate-svg)
        add_dependencies(breeze-validate-svg breeze-generate-24px-versions-dark)
    endif()
    if(NOT SKIP_INSTALL_ICONS)
        install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated/ DESTINATION ${BREEZE_INSTALL_DIR})
    endif()
endif()

if(NOT SKIP_INSTALL_ICONS)
    install(DIRECTORY ${breeze_icon_dark_dirs} DESTINATION ${BREEZE_INSTALL_DIR})
    install(FILES index.theme DESTINATION ${BREEZE_INSTALL_DIR})
endif()

gtk_update_icon_cache(${BREEZE_INSTALL_DIR})

if(BINARY_ICONS_RESOURCE)
    install(FILES ${binary_resource} DESTINATION ${BREEZE_INSTALL_DIR})
endif()
