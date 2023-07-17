# helper functions to ensure we load the icon theme
set(kbreezeicons_SRCS
    breezeicons.cpp
)

# add our icons for normal mode
qt_add_big_resources(kbreezeicons_SRCS
    ${CMAKE_BINARY_DIR}/icons/res/breeze-icons.qrc
    OPTIONS --root /icons/breeze
)

# add our icons for dark mode
qt_add_big_resources(kbreezeicons_SRCS
    ${CMAKE_BINARY_DIR}/icons-dark/res/breeze-icons-dark.qrc
    OPTIONS --root /icons/breeze-dark
)

add_library(KF6BreezeIcons ${kbreezeicons_SRCS})
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

include(ECMGeneratePriFile)

ecm_generate_pri_file(
    BASE_NAME BreezeIcons
    LIB_NAME KF6BreezeIcons
    DEPS "gui"
    FILENAME_VAR PRI_FILENAME
    INCLUDE_INSTALL_DIR ${KDE_INSTALL_INCLUDEDIR_KF}/BreezeIcons
)

install(FILES ${PRI_FILENAME} DESTINATION ${ECM_MKSPECS_INSTALL_DIR})
