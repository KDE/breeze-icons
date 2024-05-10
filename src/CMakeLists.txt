# helper functions to ensure we load the icon theme
set(kbreezeicons_SRCS breezeicons.cpp)

# generate resource file for all breeze icons
set(ICON_SRC_DIR ${CMAKE_SOURCE_DIR}/icons)
set(RESOURCES_WORKING_DIR ${CMAKE_CURRENT_BINARY_DIR}/res)
set(RESOURCE_FILE ${RESOURCES_WORKING_DIR}/breeze-icons.qrc)
set(RESOURCE_FILE_BINARY ${CMAKE_CURRENT_BINARY_DIR}/breeze-icons.rcc)

# we only will use the normal icons, we do recoloring later
get_target_property(QT_RCC_EXECUTABLE Qt6::rcc LOCATION)
add_custom_command(OUTPUT ${RESOURCE_FILE}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${RESOURCES_WORKING_DIR}
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${ICON_SRC_DIR} ${RESOURCES_WORKING_DIR}
    COMMAND qrcAlias -i ${ICON_SRC_DIR} -o ${RESOURCE_FILE}
    COMMAND ${QT_RCC_EXECUTABLE} --binary -o ${RESOURCE_FILE_BINARY} ${RESOURCE_FILE}
    DEPENDS qrcAlias
)

# install as compatibility resource file if really requested
# FIXME: remove after e.g. Kexi is ported
if(BINARY_ICONS_RESOURCE)
    install(FILES ${RESOURCE_FILE_BINARY} DESTINATION ${KDE_INSTALL_FULL_ICONDIR}/breeze)
endif()

qt_add_big_resources(kbreezeicons_resource_SRCS
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

