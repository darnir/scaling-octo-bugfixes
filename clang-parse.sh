#!/bin/bash

# Source config file for setting variables
# Expects WFLAGS and CFLAGS variables here. If not, no error handling is
# performed and the script WILL blow up.
[[ -f issuerc ]] && . issuerc

# Shift to the project directory first
cd "${PROJ_DIR}"

# Clean the directory to ensure all files are compiled.
# Define the function clean() in issuerc.
clean

# bootstrap the source repository. Perform all the actions required *before*
# running make in bootstrap(). Remember, any CFLAGS you set during configure
# will be overridden using the CFLAGS and WFLAGS defined in issuerc.
bootstrap

# Runs make assumes the compiler is already set to clang. With GCC, this will
# produce no results.
make "CFLAGS=${WFLAGS} ${CFLAGS}" 1> /dev/null 2> clang_warnings.txt

# Remove extraneous lines that are not warning messages
sed -i "/^In file included from/d" ./clang_warnings.txt
sed -i "/note:/d" ./clang_warnings.txt

# Assumes all GNU utilities. Not portable code.

# SET2 contains a list of all the files against which warnings were generated.
# SET1 is the list of files whose warnings we care about. i.e., they are the
# source files for our project.
# IGNORE_FILES is SET1 - SET2.
SET2=( $(cut -d':' -f1 clang_warnings.txt | sort -u | rev | cut -d'/' -f1 | rev | xargs) )
#echo ${SET2[*]}
SET1=( $(find src/ -name "*.[ch]" | cut -d'/' -f2) )
OLDIFS="$IFS"
IFS=$'\n'
IGNORE_FILES=( $(grep -Fxv "${SET1[*]}" <<< "${SET2[*]}" ) )
IFS="$OLDIFS"

# Remove the warnings generated due to library files from the list
for i in "${IGNORE_FILES[@]}"
do
    sed -i "/${i}/d" ./clang_warnings.txt
done

# Sort all the warnings and keep only the unique ones.
sort -u -o ./clang_warnings.txt ./clang_warnings.txt
