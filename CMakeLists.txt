cmake_minimum_required(VERSION 3.16)

set(KF_VERSION "6.19.0") # handled by release scripts
project(BreezeIcons VERSION ${KF_VERSION})

# Disallow in-source build
if("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
   message(FATAL_ERROR "Breeze Icons requires an out-of-source build. Please create a separate build directory and run 'cmake path_to_breeze_icons [options]' there.")
endif()

# ECM setup
include(FeatureSummary)
find_package(ECM 6.18.0  NO_MODULE)
set_package_properties(ECM PROPERTIES TYPE REQUIRED DESCRIPTION "Extra CMake Modules." URL "https://commits.kde.org/extra-cmake-modules")
feature_summary(WHAT REQUIRED_PACKAGES_NOT_FOUND FATAL_ON_MISSING_REQUIRED_PACKAGES)

set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

include(ECMSetupVersion)
include(KDEInstallDirs)
include(KDECMakeSettings)
include(KDEGitCommitHooks)
include(KDEFrameworkCompilerSettings NO_POLICY_SCOPE)
include(GtkUpdateIconCache)
include(ECMGenerateExportHeader)
include(ECMGenerateHeaders)
include(ECMSetupVersion)

# Dependencies
set(REQUIRED_QT_VERSION 6.7.0)
find_package(Qt6 ${REQUIRED_QT_VERSION} NO_MODULE REQUIRED COMPONENTS Core Gui)

# Find Python 3
find_package(Python 3 COMPONENTS Interpreter)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# We need this for KDE-BUG 499674. qt_add_resources has issues with 32-bit
# systems, while qt_add_big_resources has issues with LTO. We use qt_add_big_resources
# and disable LTO.
check_cxx_compiler_flag(-fno-lto COMPILER_SUPPORTS_NO_LTO)
check_cxx_compiler_flag(/GL- COMPILER_SUPPORTS_NO_GL)
if(COMPILER_SUPPORTS_NO_LTO)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-lto")
elseif(COMPILER_SUPPORTS_NO_GL)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /GL-")
endif()
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION OFF)

if(Python_FOUND)
    # Find lxml Python 3 module
    exec_program(${Python_EXECUTABLE}
        ARGS "-c \"import lxml; from lxml import etree; print(lxml.get_include())\""
        RETURN_VALUE LXML_NOT_FOUND # Returns 0 or false if successful
    )

    # Generating icons is not required, but strongly recommended in most cases
    if(LXML_NOT_FOUND)
        message(WARNING "lxml or lxml.etree not found; icon generation disabled")
        set(WITH_ICON_GENERATION OFF)
    else()
        option(WITH_ICON_GENERATION "Icon generation" ON)
    endif()
else()
    set(WITH_ICON_GENERATION OFF)
endif()

add_feature_info("Icon generation" ${WITH_ICON_GENERATION} "for 24x24 and symbolic dark icons.
   This feature requires Python 3 and the lxml Python 3 module."
) # The exact amount of indentation used in the line(s) above is intentional

# don't install the individual icons
# useful if you only want to link with the generated icon library
option(SKIP_INSTALL_ICONS "Skip installing the icons files" OFF)

# pure compatibility option for e.g. Kexi, not used in general and wastes disk space
# FIXME: remove after e.g. Kexi is ported
option(BINARY_ICONS_RESOURCE "Install Qt binary resource file containing breeze icons (breeze-icons.rcc), should only be used if needed for compatibility" OFF)

set(CMAKECONFIG_INSTALL_DIR "${KDE_INSTALL_CMAKEPACKAGEDIR}/KF6BreezeIcons")

configure_package_config_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/KF6BreezeIconsConfig.cmake.in"
  "${CMAKE_CURRENT_BINARY_DIR}/KF6BreezeIconsConfig.cmake"
  INSTALL_DESTINATION  ${CMAKECONFIG_INSTALL_DIR}
  PATH_VARS  CMAKE_INSTALL_PREFIX
)

install(FILES
  "${CMAKE_CURRENT_BINARY_DIR}/KF6BreezeIconsConfig.cmake"
  "${CMAKE_CURRENT_BINARY_DIR}/KF6BreezeIconsConfigVersion.cmake"
  DESTINATION "${CMAKECONFIG_INSTALL_DIR}"
  COMPONENT Devel
)

ecm_setup_version(PROJECT
  VARIABLE_PREFIX BREEZEICONS
  VERSION_HEADER ${CMAKE_CURRENT_BINARY_DIR}/breezeicons_version.h
  PACKAGE_VERSION_FILE "${CMAKE_CURRENT_BINARY_DIR}/KF6BreezeIconsConfigVersion.cmake"
  SOVERSION 6)

install(EXPORT KF6BreezeIconsTargets
  DESTINATION "${CMAKECONFIG_INSTALL_DIR}"
  FILE KF6BreezeIconsTargets.cmake
  NAMESPACE KF6::
)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/breezeicons_version.h
  DESTINATION ${KDE_INSTALL_INCLUDEDIR_KF}/BreezeIcons COMPONENT Devel)

add_subdirectory(autotests)

# declare both install dirs, icons will install fallback icons to dark, too!
set(BREEZE_INSTALL_DIR ${KDE_INSTALL_FULL_ICONDIR}/breeze)
set(BREEZE_DARK_INSTALL_DIR ${KDE_INSTALL_FULL_ICONDIR}/breeze-dark)

# set and create the generation directories, we always need them
set(ICON_GEN_DIR ${CMAKE_BINARY_DIR}/breeze/icons)
set(ICON_DARK_GEN_DIR ${CMAKE_BINARY_DIR}/breeze/icons-dark)
file(MAKE_DIRECTORY ${ICON_GEN_DIR})
file(MAKE_DIRECTORY ${ICON_DARK_GEN_DIR})

# generate and install both variants
add_subdirectory(icons)

# build the icon library and tools
add_subdirectory(src)

include(ECMFeatureSummary)
ecm_feature_summary(WHAT ALL FATAL_ON_MISSING_REQUIRED_PACKAGES INCLUDE_QUIET_PACKAGES)

kde_configure_git_pre_commit_hook(CHECKS CLANG_FORMAT)
