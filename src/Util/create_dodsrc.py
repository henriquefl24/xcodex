def create_dodsrc():
    """
    This method creates a .dodsrc file with the specified options.
    """
    from os.path import expanduser
    # Determine the path to the user's home directory
    home_dir = expanduser("~")

    # Create the .dodsrc file with the specified options
    with open(f"{home_dir}/.dodsrc", "w") as f:
        f.write("check-certificate=off\n")