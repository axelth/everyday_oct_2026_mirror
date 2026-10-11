import os
import re
import stat

path_re = re.compile(r'^/[\w\d\u0020\u005f\u002e\u002f\u002d]+$')

def validate_path(path: str) -> bool:
    # could also be done with a combo of
    # `os.path.
    return path_re.match(path) is not None

def check_path_access(path: str) -> (bool, list[str], list[str]|None):
    stat_res, accessible_part = None, None
    can_access = False
    effective_user = os.geteuid()
    effective_group = os.getegid()

    res: list[str] = []
    
    try:
        stat_res = os.stat(path, follow_symlinks=False)
    except PermissionError as e:
        print(e)
        accessible_part, stat_res = find_access_breaking_point(path)       
    except FileNotFoundError as e:
        # This except clause isn't necessary, but serves as a memo
        # that we treat file not found differently higher up in the
        # call stack
        raise
    if accessible_part is not None:
        # we couldn't access the whole given path
        res.append("We couldn't access the whole given path.\nHere's the last element we can observe")
        res.append(accessible_part)
    else:
        can_access = can_i_see(stat_res, effective_user, effective_group)

    print(stat_res, effective_user, effective_group, can_access)
    print(repr(stat_res))
    res.append(repr(stat_res))

    if can_access and stat.S_ISDIR(stat_res.st_mode):
        return (can_access, res, os.listdir(path))
    else:
        return (can_access, res, None)
    

def find_access_breaking_point(path: str) -> (str, os.stat_result):
    parts = path.split(os.path.sep)
    # parts[0] is '""', but this is fine because we will insert a '/' between that element
    # and the next during each check

    for i in range(len(parts) - 1, 0, -1):
        try:
            curr_path = '/'.join(parts[:i])
            stat_res = os.stat(curr_path, follow_symlinks=False)
            return (curr_path, stat_res)
        except PermissionError:
                continue

def can_i_see(stat_res: os.stat_result, euid: int, egid: int):
    if stat_res.st_uid == euid and stat_res.st_mode & stat.S_IRUSR:
        return True
    if stat_res.st_gid == egid and stat_res.st_mode & stat.S_IRGRP:
        return True
    if stat_res.st_mode & stat.S_IROTH and not stat.S_ISDIR(stat_res.st_mode):
        return True
    if (stat.S_ISDIR(stat_res.st_mode)
         and stat_res.st_mode & stat.S_IROTH
         and stat_res.st_mode & stat.S_IXOTH):
        return True
    return False
    
