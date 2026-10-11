# Can I See that Path?
## Overview
Enter a path into the search box and hit the `check` button.
- If you (the user the server program is running as) can't access the path: display the reason why.
- If you can access the path and the path is a directory: display a list of the contents of the directory.
- If you can access the path and the path is a file (including device files): display `stat` information for the file.
- If you can access the path and the path is a symlink: display what path the symlink points to.

To "see" a path means to be able to read the contents of a path.
- if the path is a directory: to list the contents of the directory
- if the path is a file: to read the file

When the path does not exist, display an error message.
When the path cannot be accessed, display "NO" in big type at the top of the result page.
When the path can be accessed, display "YES" in big type at the top of the result page.

## Plan
### Inputs
- path to check

The path to check is a plain text input.

- must be an absolute path (must start with a SOLIDUS `/`, `u002f`)
- must contain only the following characters
  - [[:ALPHANUM:]]
  - SPACE (`u0020`)
  - HYPHEN-MINUS (`-`, `u002d`)
  - LOW LINE (`_`, `u005f` "SPACING UNDERSCORE")
  - FULL STOP (`.`, `u002e`, "PERIOD")
  - SOLIDUS (`/`, `u002f`, "SLASH")
- additional restrictions defined in pathname(7) (`man 7 pathname`) are assumed to
  be enforced by the library functions called.

### Output
#### iteration 1
##### YES/NO Banner
The top of the result will have a banner with the text "YES" when the path is readable, and "NO" when it is not.

##### Details
- directory: show each element in the directory as an unordered list element
- file: print the the value of `os.stat(path)`
- symlink: print `os.path.realpath(symlink_name)`, and then the directory or file result for that.
##### Error message

### HTTP Methods and Paths
- /, GET: return HTML content with the form for executing a search
- /, POST: process the search form. Return the content described in the overview.

## Appendix
### libacl
The program would be cooler if it could read ACLs in addition to regular permissons.

package
```sh
$ dpkg -s libacl1
Package: libacl1
Status: install ok installed
Priority: required
Section: libs
Installed-Size: 74
Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
Architecture: amd64
Multi-Arch: same
Source: acl
Version: 2.3.2-2
Depends: libc6 (>= 2.38)
Description: access control list - shared library
 This package contains the shared library containing the POSIX 1003.1e
 draft standard 17 functions for manipulating access control lists.
Original-Maintainer: Guillem Jover <guillem@debian.org>
Homepage: https://savannah.nongnu.org/projects/acl/

```

related files

```sh
$ dpkg -S libacl
libacl1:amd64: /usr/lib/x86_64-linux-gnu/libacl.so.1
libacl1-dev:amd64: /usr/share/doc/libacl1-dev/extensions.txt
libacl1:amd64: /usr/lib/x86_64-linux-gnu/libacl.so.1.1.2302
libacl1-dev:amd64: /usr/share/doc/libacl1-dev/changelog.Debian.gz
libacl1:amd64: /usr/share/doc/libacl1/copyright
libacl1-dev:amd64: /usr/lib/x86_64-linux-gnu/libacl.a
libacl1:amd64: /usr/share/doc/libacl1
libacl1:amd64: /usr/share/lintian/overrides/libacl1
libacl1-dev:amd64: /usr/share/doc/libacl1-dev
libacl1:amd64: /usr/share/doc/libacl1/changelog.Debian.gz
libacl1-dev:amd64: /usr/lib/x86_64-linux-gnu/pkgconfig/libacl.pc
libacl1-dev:amd64: /usr/share/doc/libacl1-dev/libacl.txt
libacl1-dev:amd64: /usr/include/acl/libacl.h
libacl1-dev:amd64: /usr/share/doc/libacl1-dev/copyright
libacl1-dev:amd64: /usr/lib/x86_64-linux-gnu/libacl.so
```
