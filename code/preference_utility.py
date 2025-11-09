import sys
import os

def show_help():
    print("""
Usage:
  preference_utility.exe -path="<folder_path>"

Description:
  This program expects a folder path where 'preference.xml' resides.

Arguments:
  -file   Specify the folder path.
  -h, -help   Show this help message.
Example:
  preference_utility.exe -path="C:\\Users\\Documents"

Note:
  Folder structure should be like this.
      
  preference
    ├── group
    │   ├── merge
    │   │   └── DBA_pref_merge.xml   ( Group and role name should be exact match eg. dba_pref_merge.xml not work. )
    │   └── override
    │       └── DBA_pref_over.xml
    ├── ootb
    │   ├── merge
    │   │   └── ootb_pref_merge.xml
    │   └── override
    │       └── ootb_pref_over.xml
    ├── role
    │   ├── merge
    │   │   └── DBA_pref_merge.xml  ( Group and role name should be exact match eg. dba_pref_merge.xml not work. )
    │   └── override
    │       └── DBA_pref_over.xml
    └── site
        ├── merge
        │   └── site_pref_merge.xml
        └── override
            └── site_pref_over.xml

""")

def main():
    folder_path = None

    # Parse command line arguments
    for arg in sys.argv[1:]:
        if arg in ("-h", "-help","-HELP"):
            show_help()
            return
        elif arg.startswith("-path="):
            folder_path = arg.split("=", 1)[1].strip('"')

    # If folder path missing, show error
    if not folder_path:
        print("Error: folder path needed where preference.xml resides")
        print('Use "-h" or "-help" for more information.')
        return

    # Validate folder path
    if os.path.isdir(folder_path):
        print(f"Folder path: {os.path.abspath(folder_path)}")
    else:
        print(f"Error: '{folder_path}' is not a valid folder path.")

if __name__ == "__main__":
    main()
