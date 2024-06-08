# takes light theme icons and makes modified copies of them with dark theme stylesheets
add_executable(generate-symbolic-dark generate-symbolic-dark.cpp)
target_link_libraries(generate-symbolic-dark PRIVATE Qt6::Core)
ecm_mark_nongui_executable(generate-symbolic-dark)

# qrc generator
add_executable(qrcAlias qrcAlias.cpp)
target_link_libraries(qrcAlias PRIVATE Qt6::Core)
ecm_mark_nongui_executable(qrcAlias)
