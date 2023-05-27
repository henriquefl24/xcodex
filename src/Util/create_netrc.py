def create_netrc(username: str, password: str):
    """
    This method creates a .netrc file with the provided Earthdata credentials.
    """
    from os.path import expanduser
    # Determine the path to the user's home directory
    home_dir = expanduser("~")

    # Create the .netrc file with the provided credentials
    with open(f"{home_dir}/.netrc", "w") as f:
        f.write(f"machine urs.earthdata.nasa.gov\n")
        f.write(f"login {username}\n")
        f.write(f"password {password}\n")