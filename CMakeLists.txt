cmake_minimum_required(VERSION 2.8.12)

project(BreezeIcons)

# ECM setup
include(FeatureSummary)
find_package(ECM 5.19.0  NO_MODULE)
set_package_properties(ECM PROPERTIES TYPE REQUIRED DESCRIPTION "Extra CMake Modules." URL "https://projects.kde.org/projects/kdesupport/extra-cmake-modules")
feature_summary(WHAT REQUIRED_PACKAGES_NOT_FOUND FATAL_ON_MISSING_REQUIRED_PACKAGES)

set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} ${ECM_KDE_MODULE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
set(KF5_VERSION "5.19.0") # handled by release scripts

include(KDEInstallDirs)
include(KDECMakeSettings)
include(KDECompilerSettings NO_POLICY_SCOPE)
include(GtkUpdateIconCache)

# Dependencies
set(REQUIRED_QT_VERSION "5.3.0")

add_subdirectory(autotests)
add_subdirectory(icons)
add_subdirectory(icons-dark)

feature_summary(WHAT ALL FATAL_ON_MISSING_REQUIRED_PACKAGES)
