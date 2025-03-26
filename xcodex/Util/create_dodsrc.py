from os.path import join, expanduser

def create_dodsrc():
    """
    Create a .dodsrc file in the user's home directory.
    """
    try:
        home_dir = expanduser("~")
        dodsrc_path = join(home_dir, ".dodsrc")
        with open(dodsrc_path, "w") as f:
            f.write("HTTP.COOKIEJAR = ~/.urs_cookies\n")
            f.write("HTTP.NETRC = ~/.netrc\n")
        print(f".dodsrc file created successfully at {dodsrc_path}")
    except OSError as e:
        print(f"Failed to create .dodsrc file: {e}")
