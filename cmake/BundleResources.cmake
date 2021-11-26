function(__add_file_to_qrc_file)
    set(options "")
    set(oneValueArgs QRC_PATH FILE_PATH ALIAS ROOT)
    set(multiValueArgs)
    cmake_parse_arguments(__ADD_FILE_TO_QRC_FILE "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    foreach(param QRC_PATH FILE_PATH)
        if(NOT __ADD_FILE_TO_QRC_FILE_${param})
            message(FATAL_ERROR "${CMAKE_CURRENT_FUNCTION}: Argument missing: ${param}")
        endif()
    endforeach()
    set(INDENT "        ")

    if (TRUE)
        if (WIN32)
            # https://gitlab.kitware.com/cmake/cmake/-/issues/21246
            # super slow
            execute_process(
                COMMAND ${Python_EXECUTABLE} -u -c "import os; print(os.path.realpath('${__ADD_FILE_TO_QRC_FILE_FILE_PATH}'))"
                OUTPUT_VARIABLE SYMLINK_TARGET
                OUTPUT_STRIP_TRAILING_WHITESPACE
            )
        else()
            file(REAL_PATH ${__ADD_FILE_TO_QRC_FILE_FILE_PATH} SYMLINK_TARGET)
        endif()
        set(line "<!--${__ADD_FILE_TO_QRC_FILE_FILE_PATH} -> ${SYMLINK_TARGET}}-->\n${INDENT}<file alias=\"${__ADD_FILE_TO_QRC_FILE_ALIAS}\">${SYMLINK_TARGET}</file>")
    else()
        set(line "<file ")
        if(__ADD_FILE_TO_QRC_FILE_ALIAS)
            set(line "${line} alias=\"${__ADD_FILE_TO_QRC_FILE_ALIAS}\"")
        endif()
        set(line "${line}>${__ADD_FILE_TO_QRC_FILE_FILE_PATH}</file>")
    endif()
    file(APPEND ${__ADD_FILE_TO_QRC_FILE_QRC_PATH} "${INDENT}${line}\n")
endfunction()


function(__write_qrc_file_header QRC_PATH)
    file(WRITE ${QRC_PATH} "<RCC>\n")
    file(APPEND ${QRC_PATH} "    <qresource>\n")
endfunction()

function(__write_qrc_file_footer QRC_PATH)
    file(APPEND ${QRC_PATH} "    </qresource>\n")
    file(APPEND ${QRC_PATH} "</RCC>\n")
endfunction()

function(__generate_qrc_file)
    set(options "")
    set(oneValueArgs QRC_PATH PREFIX ROOT)
    set(multiValueArgs FILES)
    cmake_parse_arguments(GENERATE_QRC_FILE "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    foreach(param ${oneValueArgs} ${multiValueArgs})
        if(NOT GENERATE_QRC_FILE_${param})
            message(FATAL_ERROR "${CMAKE_CURRENT_FUNCTION}: Argument missing: ${param}")
        endif()
    endforeach()

    __write_qrc_file_header(${GENERATE_QRC_FILE_QRC_PATH})

    list(LENGTH GENERATE_QRC_FILE_FILES TOTAL)
    set(POS 1)
    set(PERCENT_OLD 0)
    foreach(file ${GENERATE_QRC_FILE_FILES})
        math(EXPR POS "${POS} + 1")
        math(EXPR PERCENT "100 * ${POS} / ${TOTAL}")
        if (NOT ${PERCENT_OLD} EQUAL ${PERCENT})
            set(PERCENT_OLD ${PERCENT})
            message(STATUS "Generating qrc: ${PERCENT}%")
        endif()
        file(RELATIVE_PATH file_name ${GENERATE_QRC_FILE_ROOT} ${file})
        set(file_alias ${GENERATE_QRC_FILE_PREFIX}/${file_name})
        __add_file_to_qrc_file(
            QRC_PATH ${GENERATE_QRC_FILE_QRC_PATH}
            FILE_PATH ${file}
            ALIAS ${file_alias}
            ROOT ${GENERATE_QRC_FILE_ROOT}
        )
    endforeach()

    __write_qrc_file_footer(${GENERATE_QRC_FILE_QRC_PATH})
endfunction()

# add resources to a target using the Qt resources system
# parameters:
#   - TARGET: the target to bundle the resources with
#   - PREFIX: virtual "subdirectory" the files will be available from
#   - FILES: the files to bundle
function(add_resources_to_target)
    set(options "")
    set(oneValueArgs TARGET PREFIX ROOT)
    set(multiValueArgs FILES)
    cmake_parse_arguments(ADD_RESOURCES_TO_TARGET "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    foreach(param ${oneValueArgs} ${multiValueArgs})
        if(NOT ADD_RESOURCES_TO_TARGET_${param})
            message(FATAL_ERROR "${CMAKE_CURRENT_FUNCTION}: Argument missing: ${param}")
        endif()
    endforeach()

    set(qrc_path ${CMAKE_CURRENT_BINARY_DIR}/${ADD_RESOURCES_TO_TARGET_TARGET}.qrc)
    __generate_qrc_file(
        QRC_PATH ${qrc_path}
        PREFIX ${ADD_RESOURCES_TO_TARGET_PREFIX}
        FILES "${ADD_RESOURCES_TO_TARGET_FILES}"
        ROOT "${ADD_RESOURCES_TO_TARGET_ROOT}"
    )
endfunction()

