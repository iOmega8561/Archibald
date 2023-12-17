#!/usr/bin/python3

"""This is meant to be Archibald's entrypoint
   This file should therefore be executed as a script"""

import sys
from functions import console, linux, setup
from profiles import load as load_profiles

def main():

    """This is the main function
       Archibald checks if the runnning system is Arch Linux
       and presents the user a menu to select the desired profile"""

    # Ensure this is running on Arch Linux
    with open("/etc/os-release", "r", encoding="utf-8") as release:

        if not "Arch Linux" in release.read():

            # Exit if system is not Arch Linux
            console.log("This is not Arch Linux.", "err")
            sys.exit(1)

    username, p_dict = linux.whoami(), load_profiles()

    console.log(f"Welcome {username}, select a profile:")

    for i, profile in enumerate(p_dict):
        console.log(f"{i+1}) {p_dict[profile].name}", "nof")

    try:

        # intGet makes sure this is an integer input
        consoleinput = console.intget(1, len(p_dict), "Answer: ")

        # Configure selected profile
        if not setup.resolve(p_dict, consoleinput-1, username):
            console.log("A problem occurred, check log files!", "err")
            sys.exit(1)

        # Conclusion
        console.log("All operations completed, please reboot!", "suc")

    except KeyboardInterrupt:

        # Just quit if ctrl+c
        console.log("Detected keyboard interrupt, terminating.", "wrn")
        sys.exit(1)

if __name__ == "__main__":
    main()
