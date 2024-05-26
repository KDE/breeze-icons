# helper functions to ensure we load the icon theme
set(kbreezeicons_SRCS breezeicons.cpp)

# avoid dependency cycle with add resource
set(CMAKE_AUTOMOC OFF)

# generate resource file for all breeze icons
set(RESOURCE_FILE ${CMAKE_CURRENT_BINARY_DIR}/breeze-icons.qrc)
set(RESOURCE_FILE_BINARY ${CMAKE_CURRENT_BINARY_DIR}/breeze-icons.rcc)

# we only will use the normal icons, we do recoloring later
# we run the tool over the dark ones just to do all checks on them, too
add_custom_command(OUTPUT ${RESOURCE_FILE}
    COMMAND qrcAlias -o ${RESOURCE_FILE} ${CMAKE_SOURCE_DIR}/icons ${CMAKE_BINARY_DIR}/breeze-icons # used for the resource
    COMMAND qrcAlias -o ${RESOURCE_FILE}.dark.dummy ${CMAKE_SOURCE_DIR}/icons-dark ${CMAKE_BINARY_DIR}/breeze-icons-dark # used for checking only
    COMMAND Qt6::rcc --binary -o ${RESOURCE_FILE_BINARY} ${RESOURCE_FILE} # FIXME: remove after e.g. Kexi is ported
    DEPENDS qrcAlias breeze-generate-24px-versions breeze-generate-24px-versions-dark # ensure we run after the generation steps
    USES_TERMINAL
)

# install as compatibility resource file if really requested
# FIXME: remove after e.g. Kexi is ported
if(BINARY_ICONS_RESOURCE)
    install(FILES ${RESOURCE_FILE_BINARY} DESTINATION ${KDE_INSTALL_FULL_ICONDIR}/breeze)
endif()

# use normal resource adding, big resource variant has issue with LTO
qt_add_resources(kbreezeicons_resource_SRCS
    ${RESOURCE_FILE}
    OPTIONS --root /icons/breeze
)

add_library(KF6BreezeIcons ${kbreezeicons_resource_SRCS} ${kbreezeicons_SRCS})
add_library(KF6::BreezeIcons ALIAS KF6BreezeIcons)

set_target_properties(KF6BreezeIcons
    PROPERTIES
        VERSION ${BREEZEICONS_VERSION}
        SOVERSION ${BREEZEICONS_SOVERSION}
        EXPORT_NAME BreezeIcons
)

generate_export_header(KF6BreezeIcons BASE_NAME BreezeIcons)

target_include_directories(KF6BreezeIcons
    INTERFACE
        "$<INSTALL_INTERFACE:${KDE_INSTALL_INCLUDEDIR_KF}/BreezeIcons>"
)

target_link_libraries(KF6BreezeIcons
    PUBLIC
        Qt6::Gui
)

ecm_generate_headers(KF6BreezeIcons_CamelCase_HEADERS
    HEADER_NAMES
        BreezeIcons

    REQUIRED_HEADERS
        KF6BreezeIcons_HEADERS
)

install(TARGETS KF6BreezeIcons EXPORT KF6BreezeIconsTargets ${KF_INSTALL_TARGETS_DEFAULT_ARGS})

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/breezeicons_export.h
    ${KF6BreezeIcons_HEADERS}
    DESTINATION ${KDE_INSTALL_INCLUDEDIR_KF}/BreezeIcons
    COMPONENT Devel
)

install(FILES
    ${KF6BreezeIcons_CamelCase_HEADERS}
    DESTINATION ${KDE_INSTALL_INCLUDEDIR_KF}/BreezeIcons
    COMPONENT Devel
)

