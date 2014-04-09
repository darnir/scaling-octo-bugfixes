ng-octo-bugfixes
=====================

For want of a better name, 'scaling-octo-bugfixes' is a couple of simple
hackish scripts I wrote when beginning my spring cleaning work on GNU Wget.

What these scripts do is turn the warnings spewed by Clang into github issues.
While new projects should ideally just set a bunch of warning flags and use
-Werror, this isn't exactly possible on old and established projects. Hence, we
try and turn all warnings into issues. By running this script upon every
commit, we update the issues on GitHub and hence know who introduced bad coding
practices in which commit.

This project is comprised of two separate scripts:
   * clang-parse.sh: A shell script that compiles the project and parses the
warnings output by clang, storing them in a separate file called
clang\_warnings.txt. **IMPORTANT:** This script imports another config file
called issuerc. issuerc is also a bash script which defines most of the
work that is to be done. Please ensure that the variables that have
current;y been defined in issuerc remain since no error checking has
currently been implemented for missing variables.
   * githubissue.py: This is a small Python3 script which uses the pyGithub
library to interface with GitHub and create issues. This script too uses a
config file which is formatted like a INI file that can be ready by
Python's configparser module. The structure of the file is explained
below.

githubissuerc
-------------

This is a simple INI file which contains currently only the credentials for the
user's GitHub account in plaintext. It should look like the following:
```
[Credentials]

user = your_username
password = your_password
```

ToDo
====

    * Remove hardcoded variables from githubissue.py
    * Use only one script for both tasks. Or use a master script to handle both
        * Have a single config file for both
    * Allow creating a commit and formatting a patch using the staging area of
      git.

Authors
=======

Darshit Shah  <darnir@gmail.com>

License
=======

MIT License., If you face any licensing issues, please contact me directly.
