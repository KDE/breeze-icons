# helper functions to ensure we load the icon theme
set(kbreezeicons_SRCS
    breezeicons.cpp
)

# add our icons for normal mode
qt_add_resources(kbreezeicons_SRCS
    ${CMAKE_BINARY_DIR}/icons/res/breeze-icons.qrc
    OPTIONS --root /icons/breeze
)

# add our icons for dark mode
qt_add_resources(kbreezeicons_SRCS
    ${CMAKE_BINARY_DIR}/icons-dark/res/breeze-icons-dark.qrc
    OPTIONS --root /icons/breeze-dark
)

add_library(KF5BreezeIcons ${kbreezeicons_SRCS})
add_library(KF5::BreezeIcons ALIAS KF5BreezeIcons)


set_target_properties(KF5BreezeIcons
    PROPERTIES
        VERSION ${BREEZEICONS_VERSION}
        SOVERSION ${BREEZEICONS_SOVERSION}
        EXPORT_NAME BreezeIcons
)


generate_export_header(KF5BreezeIcons BASE_NAME BreezeIcons)

target_include_directories(KF5BreezeIcons
    INTERFACE
        "$<INSTALL_INTERFACE:${KDE_INSTALL_INCLUDEDIR_KF}/BreezeIcons>"
)

target_link_libraries(KF5BreezeIcons
    PUBLIC
        Qt${QT_MAJOR_VERSION}::Gui
)

ecm_generate_headers(KF5BreezeIcons_CamelCase_HEADERS
    HEADER_NAMES
        BreezeIcons

    REQUIRED_HEADERS
        KF5BreezeIcons_HEADERS
)

install(TARGETS KF5BreezeIcons EXPORT KF5BreezeIconsTargets ${KF_INSTALL_TARGETS_DEFAULT_ARGS})

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/breezeicons_export.h
    ${KF5BreezeIcons_HEADERS}
    DESTINATION ${KDE_INSTALL_INCLUDEDIR_KF}/BreezeIcons
    COMPONENT Devel
)

install(FILES
    ${KF5BreezeIcons_CamelCase_HEADERS}
    DESTINATION ${KDE_INSTALL_INCLUDEDIR_KF}/BreezeIcons
    COMPONENT Devel
)

include(ECMGeneratePriFile)

ecm_generate_pri_file(
    BASE_NAME BreezeIcons
    LIB_NAME KF5BreezeIcons
    DEPS "gui"
    FILENAME_VAR PRI_FILENAME
    INCLUDE_INSTALL_DIR ${KDE_INSTALL_INCLUDEDIR_KF}/BreezeIcons
)

install(FILES ${PRI_FILENAME} DESTINATION ${ECM_MKSPECS_INSTALL_DIR})
