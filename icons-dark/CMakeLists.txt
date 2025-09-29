# index.theme is used by the lib (via qrc/rcc)
# and gets installed in the condition below
file(COPY_FILE index.theme.in index.theme)
file(READ ../commonthemeinfo.theme.in COMMON_THEME_INFO)
file(APPEND index.theme ${COMMON_THEME_INFO})

# just refresh cache & install the theme file, icons got handled in the icons dir
if(NOT SKIP_INSTALL_ICONS)
    install(FILES index.theme DESTINATION ${BREEZE_DARK_INSTALL_DIR})
    gtk_update_icon_cache(${BREEZE_DARK_INSTALL_DIR})
endif()
