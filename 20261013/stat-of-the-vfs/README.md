# Stat of the VFS
## Overview
Let's stat some filesystems.
That is, let's put the results of `os.statvfs` on a web page

## Plan
Call `os.statvfs('/')`
```sh
$ pydoc3 os.statvfs
Help on built-in function statvfs in os:

os.statvfs = statvfs(path)
    Perform a statvfs system call on the given path.

    path may always be specified as a string.
    On some platforms, path may also be specified as an open file descriptor.
      If this functionality is unavailable, using it raises an exception.
```

This returns an `os.statvfs_result`.
```sh
$ pydoc3 os.statvfs_result
Help on class statvfs_result in os:

os.statvfs_result = class statvfs_result(builtins.tuple)
 |  os.statvfs_result(iterable=(), /)
 |
 |  statvfs_result: Result from statvfs or fstatvfs.
 |
 |  This object may be accessed either as a tuple of
 |    (bsize, frsize, blocks, bfree, bavail, files, ffree, favail, flag, namemax),
 |  or via the attributes f_bsize, f_frsize, f_blocks, f_bfree, and so on.
... snip ...
```

Display `bsize`, `blocks`, `bfree`, `bavail`. The three latter values are displayed multiplied by `bsize`


