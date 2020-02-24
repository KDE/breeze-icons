if(BINARY_ICONS_RESOURCE)
    generate_binary_resource(icons-dark binary_resource)
endif()

########### install files ###############

set(breeze_icon_dark_dirs
    actions animations applets apps categories preferences devices emblems
    emotes mimetypes places status)

set(BREEZE_INSTALL_DIR ${KDE_INSTALL_FULL_ICONDIR}/breeze-dark)

if (NOT SKIP_INSTALL_ICONS)
    install( DIRECTORY ${breeze_icon_dark_dirs} DESTINATION ${BREEZE_INSTALL_DIR} )
    install( FILES index.theme DESTINATION ${BREEZE_INSTALL_DIR})
endif()

# Auto-generate 24px monochrome icons from 22px versions
if(NOT WIN32)
    find_program(BASH_EXE bash)
    add_custom_target(breeze-generate-24px-versions ALL
        COMMAND ${BASH_EXE} ${CMAKE_SOURCE_DIR}/generate-24px-versions.sh ${BREEZE_INSTALL_DIR}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )
endif()

gtk_update_icon_cache(${BREEZE_INSTALL_DIR})

if(BINARY_ICONS_RESOURCE)
    install( FILES ${binary_resource} DESTINATION ${BREEZE_INSTALL_DIR})
endif()
