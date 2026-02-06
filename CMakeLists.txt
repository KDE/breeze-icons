cmake_minimum_required(VERSION 3.27)

set(KF_VERSION "6.24.0") # handled by release scripts
project(BreezeIcons VERSION ${KF_VERSION})

# Disallow in-source build
if("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
   message(FATAL_ERROR "Breeze Icons requires an out-of-source build. Please create a separate build directory and run 'cmake path_to_breeze_icons [options]' there.")
endif()

# ECM setup
include(FeatureSummary)
find_package(ECM 6.23.0  NO_MODULE)
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
set(REQUIRED_QT_VERSION 6.8.0)
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

# 24x24 generation (requires python)
option(WITH_ICON_GENERATION "24x24 icon generation" ON)
add_feature_info("Icon generation" ${WITH_ICON_GENERATION} "for 24x24 icons, this feature requires Python 3 and the lxml Python 3 module.")
if(WITH_ICON_GENERATION)
    find_package(Python 3 COMPONENTS Interpreter REQUIRED)
endif()

# don't install the individual icons
# useful if you only want to link with the generated icon library
option(SKIP_INSTALL_ICONS "Skip installing the icons files" OFF)

# pure compatibility option for e.g. Kexi, not used in general and wastes disk space
# FIXME: remove after e.g. Kexi is ported
option(BINARY_ICONS_RESOURCE "Install Qt binary resource file containing breeze icons (breeze-icons.rcc), should only be used if needed for compatibility" OFF)

option(WITH_ICONS_LIBRARY "Build the Breeze icons library" ON)

if(WITH_ICONS_LIBRARY)
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
endif()

# tools to generate icons and resources
add_subdirectory(tools)

# generate and install both variants
add_subdirectory(icons)

# unit tests
add_subdirectory(autotests)

include(ECMFeatureSummary)
ecm_feature_summary(WHAT ALL FATAL_ON_MISSING_REQUIRED_PACKAGES INCLUDE_QUIET_PACKAGES)

kde_configure_git_pre_commit_hook(CHECKS CLANG_FORMAT)
