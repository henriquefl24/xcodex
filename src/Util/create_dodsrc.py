from os.path import join, expanduser


def create_dodsrc():
    """
    Create a .dodsrc file in the user's home directory.
    """
    home_dir = expanduser("~")
    dodsrc_path = join(home_dir, ".dodsrc")
    with open(dodsrc_path, "w") as f:
        f.write("HTTP.COOKIEJAR = ~/.urs_cookies\n")
        f.write("HTTP.NETRC = ~/.netrc\n")
