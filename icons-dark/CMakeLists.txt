########### install files ###############

set( breeze_icon_dark_dirs  actions apps categories devices emblems emotes mimetypes places status)

set(BREEZE_INSTALL_DIR ${KDE_INSTALL_FULL_ICONDIR}/breeze-dark)
install( DIRECTORY ${breeze_icon_dark_dirs} DESTINATION ${BREEZE_INSTALL_DIR} )
install( FILES index.theme DESTINATION ${BREEZE_INSTALL_DIR})

gtk_update_icon_cache(${BREEZE_INSTALL_DIR})
