from os.path import join, expanduser

def create_netrc(username: str, password: str):
    """
    Create a .netrc file in the user's home directory with the provided EARTHDATA LOGIN credentials.
    """
    try:
        home_dir = expanduser("~")
        netrc_path = join(home_dir, ".netrc")
        with open(netrc_path, "w") as f:
            f.write(f"machine urs.earthdata.nasa.gov login {username} password {password}\n")
        print(f".netrc file created successfully at {netrc_path}")
    except OSError as e:
        print(f"Failed to create .netrc file: {e}")