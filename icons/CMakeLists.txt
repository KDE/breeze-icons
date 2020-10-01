if(BINARY_ICONS_RESOURCE)
    generate_binary_resource(icons binary_resource)
endif()

########### install files ###############

set(breeze_icon_dirs
    actions animations applets apps categories preferences devices emblems
    emotes mimetypes places status)

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
    install(FILES index.theme DESTINATION ${BREEZE_INSTALL_DIR})
    if(WITH_ICON_GENERATION)
        install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated/ DESTINATION ${BREEZE_INSTALL_DIR})
    endif()
endif()

gtk_update_icon_cache(${BREEZE_INSTALL_DIR})

if(BINARY_ICONS_RESOURCE)
    install(FILES ${binary_resource} DESTINATION ${BREEZE_INSTALL_DIR})
endif()
