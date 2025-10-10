# avoid dependency cycle with add resource
set(CMAKE_AUTOMOC OFF)

# declare both install dirs, icons will install fallback icons to dark, too!
set(BREEZE_INSTALL_DIR ${KDE_INSTALL_FULL_ICONDIR}/breeze)
set(BREEZE_DARK_INSTALL_DIR ${KDE_INSTALL_FULL_ICONDIR}/breeze-dark)

# generate resource file for all breeze icons
set(RESOURCE_FILE ${CMAKE_CURRENT_BINARY_DIR}/breeze-icons.qrc)
set(RESOURCE_FILE_BINARY ${CMAKE_CURRENT_BINARY_DIR}/breeze-icons.rcc)

# set and create the generation directories, we always need them
set(ICON_GEN_DIR ${CMAKE_BINARY_DIR}/breeze/icons)
set(ICON_DARK_GEN_DIR ${CMAKE_BINARY_DIR}/breeze/icons-dark)
file(MAKE_DIRECTORY ${ICON_GEN_DIR})
file(MAKE_DIRECTORY ${ICON_DARK_GEN_DIR})

# get all icon categories
FILE(GLOB possible_icon_dirs RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/*)
SET(breeze_icon_dirs "")
FOREACH(possible_icon_dir ${possible_icon_dirs})
    IF(IS_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${possible_icon_dir})
        LIST(APPEND breeze_icon_dirs ${possible_icon_dir})
    ENDIF()
ENDFOREACH()

# get all icons as dependencies for the generation
file(GLOB_RECURSE icon_svgs ${CMAKE_CURRENT_SOURCE_DIR}/*.svg)

# generate the two theme indices
file(COPY_FILE breeze.theme.in ${ICON_GEN_DIR}/index.theme)
file(READ commonthemeinfo.theme.in COMMON_THEME_INFO)
file(APPEND ${ICON_GEN_DIR}/index.theme ${COMMON_THEME_INFO})
file(COPY_FILE breeze-dark.theme.in ${ICON_DARK_GEN_DIR}/index.theme)
file(READ commonthemeinfo.theme.in COMMON_THEME_INFO)
file(APPEND ${ICON_DARK_GEN_DIR}/index.theme ${COMMON_THEME_INFO})

# generate stuff if wanted
if(WITH_ICON_GENERATION)
    # generate 24px & dark icons + do checking and create the resource
    add_custom_command(OUTPUT ${RESOURCE_FILE}
        COMMENT "Generating 24px & symbolic dark icons and resources"
        COMMAND ${Python_EXECUTABLE} ${CMAKE_SOURCE_DIR}/tools/generate-24px-versions.py ${CMAKE_CURRENT_SOURCE_DIR} ${ICON_GEN_DIR}
        COMMAND $<TARGET_FILE:generate-symbolic-dark> ${CMAKE_SOURCE_DIR}/icons ${ICON_GEN_DIR} ${ICON_DARK_GEN_DIR}
        COMMAND $<TARGET_FILE:qrcAlias> -o ${RESOURCE_FILE} ${CMAKE_SOURCE_DIR}/icons ${ICON_GEN_DIR} # used for the resource
        COMMAND $<TARGET_FILE:qrcAlias> -o ${RESOURCE_FILE}.dark.dummy ${ICON_DARK_GEN_DIR} # used for checking only
        COMMAND Qt6::rcc --binary -o ${RESOURCE_FILE_BINARY} ${RESOURCE_FILE} # FIXME: remove after e.g. Kexi is ported
        DEPENDS ${icon_svgs} commonthemeinfo.theme.in breeze.theme.in breeze-dark.theme.in
        USES_TERMINAL
    )
else()
    # generate dark icons + do checking and create the resource
    add_custom_command(OUTPUT ${RESOURCE_FILE}
        COMMENT "Generating symbolic dark icons and resources"
        COMMAND $<TARGET_FILE:generate-symbolic-dark> ${CMAKE_SOURCE_DIR}/icons ${ICON_GEN_DIR} ${ICON_DARK_GEN_DIR}
        COMMAND $<TARGET_FILE:qrcAlias> -o ${RESOURCE_FILE} ${CMAKE_SOURCE_DIR}/icons ${ICON_GEN_DIR} # used for the resource
        COMMAND $<TARGET_FILE:qrcAlias> -o ${RESOURCE_FILE}.dark.dummy ${ICON_DARK_GEN_DIR} # used for checking only
        COMMAND Qt6::rcc --binary -o ${RESOURCE_FILE_BINARY} ${RESOURCE_FILE} # FIXME: remove after e.g. Kexi is ported
        DEPENDS ${icon_svgs} commonthemeinfo.theme.in breeze.theme.in breeze-dark.theme.in
        USES_TERMINAL
    )
endif()

# install as compatibility resource file if really requested
# FIXME: remove after e.g. Kexi is ported
if(BINARY_ICONS_RESOURCE)
    install(FILES ${RESOURCE_FILE_BINARY} DESTINATION ${BREEZE_INSTALL_DIR})
endif()

if(NOT SKIP_INSTALL_ICONS)
    # install the instantiated theme indices
    install(FILES ${ICON_GEN_DIR}/index.theme DESTINATION ${BREEZE_INSTALL_DIR})
    install(FILES ${ICON_DARK_GEN_DIR}/index.theme DESTINATION ${BREEZE_DARK_INSTALL_DIR})

    # we install icons as breeze and as fallback for breeze-dark
    # breeze-dark will overwrite some installed files with generated color patched ones

    install(DIRECTORY ${breeze_icon_dirs} DESTINATION ${BREEZE_INSTALL_DIR})
    install(DIRECTORY ${breeze_icon_dirs} DESTINATION ${BREEZE_DARK_INSTALL_DIR})

    if(WITH_ICON_GENERATION)
        install(DIRECTORY ${ICON_GEN_DIR}/ DESTINATION ${BREEZE_INSTALL_DIR})
        install(DIRECTORY ${ICON_GEN_DIR}/ DESTINATION ${BREEZE_DARK_INSTALL_DIR})

        # generated dark icons are installed on-top
        install(DIRECTORY ${ICON_DARK_GEN_DIR}/ DESTINATION ${BREEZE_DARK_INSTALL_DIR})
    endif()

    # update the icon caches
    gtk_update_icon_cache(${BREEZE_INSTALL_DIR})
    gtk_update_icon_cache(${BREEZE_DARK_INSTALL_DIR})
endif()

# helper functions to ensure we load the icon theme
set(kbreezeicons_SRCS breezeicons.cpp)

# use big resource variant, else we OOM on 32 bit machines
# this has issues with LTO, we have a unit test that tells if stuff got lost in the DLL
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
