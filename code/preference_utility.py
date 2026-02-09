import sys
import os
import subprocess

EXECUTE = True  # set False if you only want to print                           
# EXECUTE = False  # set False if you only want to print                           


def show_help():
    print(r"""
  ──────────────────────────────────────────────────────────────────────────
                  Preference Utility - Help Guide
  ──────────────────────────────────────────────────────────────────────────

  Usage:
    preference_utility.exe -u="<user>" -p="<password>" -pf="<password_file_path>" -g="<group>" -path="<folder_path>"

  Description:
    This utility reads user credentials and locates the '*.xml' files
    in the provided folder path. It validates the folder structure and ensures
    group and role names match exactly as required.

  Arguments:
    -u        Specify username
    -p        Specify password
    -pf       Specify password file path (alternative to -p)
    -g        Specify group name
    -path     Specify the folder path where 'preference.xml' resides
    -h, -help, -HELP   Show this help message

  Example:
    preference_utility.exe -u="admin" -p="1234" -g="DBA" -path="C:\Users\Documents"

  ────────────────────────────────────────────────────────────────────────
                  Expected Folder Structure:
  ────────────────────────────────────────────────────────────────────────

  preference
      ├── group
      │   ├── merge
      │   │   └── DBA_pref_merge.xml      ← Group and role names must match exactly.
      │   └── override
      │       └── DBA_pref_over.xml
      │
      ├── ootb
      │   ├── merge
      │   │   └── ootb_pref_merge.xml
      │   └── override
      │       └── ootb_pref_over.xml
      │
      ├── role
      │   ├── merge
      │   │   └── DBA_pref_merge.xml      ← Ensure correct case (e.g., 'DBA', not 'dba').
      │   └── override
      │       └── DBA_pref_over.xml
      │
      ├── site
      │   ├── merge
      │   │   └── site_pref_merge.xml      
      │   └── override
      │       └── site_pref_over.xml
      │
      └── user
          ├── merge
          │   └── user_pref_merge.xml
          └── override
              └── user_pref_over.xml

  ──────────────────────────────────────────────────────────────
  Notes:
    • Folder and file names are case-sensitive.
    • Make sure the structure above exists under the given path.
    • Incorrect naming Group and Role name should be exact match in TC.
    • Incorrect naming (e.g., lowercase vs uppercase) will cause processing errors.
  ──────────────────────────────────────────────────────────────
""")


def extract_target_from_xml(scope: str, xml_path: str) -> str:
    """
    Extracts target name from XML filename like 'DBA_pref_merge.xml' → 'DBA'.
    Works only for scope 'group' or 'role'. Returns 'unknown' for others.
    """
    # Only process group or role scopes
    if scope.lower() not in ("group", "role"):
        return "unknown"

    filename = os.path.basename(xml_path)
    name, _ = os.path.splitext(filename)

    # Extract the part before first underscore (e.g., DBA_pref_merge → DBA)
    target = name.split('_')[0].strip()

    # Return 'unknown' if blank (e.g., malformed filename)
    if not target:
        return "unknown"

    return target




def determine_scope(folder_path: str) -> str:
    """Determine scope from folder name (group, role, site, ootb)."""
    parts = folder_path.lower().split(os.sep)
    for scope in ["group", "role", "site", "ootb", "user"]:
        if scope in parts:
            return "site" if scope == "ootb" else scope
    return "unknown"

def determine_action(folder_path: str) -> str:
  """Determine action (merge/override) from folder name."""
  parts = folder_path.lower().split(os.sep)
  for action in ["merge", "override"]:
      if action in parts:
          return action.upper()
  return "unknown"

def process_folder(base_folder: str, user: str, password: str, password_file: str, group: str):
    """Walk through folders, find XML files, and print commands."""
    env1 = os.environ.copy()
    tc_root = os.environ.get("TC_ROOT")
    tc_data = os.environ.get("TC_DATA")
    
    check_password_file = "Yes" if password_file else "No"
    # print(f"Password provided via file: {check_password_file}")

    # print(f'"TC_ROOT": {tc_root}')
    # print(f'"TC_DATA": {tc_data}')

    if not tc_root:
        print("Error: TC_ROOT environment variable not set.")
        return

    exe_path = os.path.join(tc_root, "bin", "preferences_manager.exe")

    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if not os.path.isdir(folder_path):
            continue  # skip any files
        print("-------------------------------------------------------------")
        print(f"\nImporting {folder_name.upper()} preferences...")
        print("-------------------------------------------------------------")

        # ✅ Only go inside merge/override subfolders
        for action_folder in ["merge", "override"]:
            subfolder = os.path.join(folder_path, action_folder)
            if not os.path.isdir(subfolder):
                continue

            for root, _, files in os.walk(subfolder):
                for file in files:
                    if not file.lower().endswith(".xml"):
                        continue

                    xml_path = os.path.join(root, file)
                    scope = determine_scope(root)
                    action = determine_action(root)
                    target = extract_target_from_xml(scope, xml_path)

                    # ✅ Add -target only for group/role scopes
                    if scope in ("group", "role"):
                        if check_password_file == "Yes":
                            cmd = (
                                f'{exe_path} -u={user} -pf="{password_file}" -g={group} '
                                f'-mode=import -scope={scope} -target={target} '
                                f'-action={action} -file="{xml_path}"'
                            )
                        else:
                            cmd = (
                                f'{exe_path} -u={user} -p={password} -g={group} '
                                f'-mode=import -scope={scope} -target={target} '
                                f'-action={action} -file="{xml_path}"'
                            )
                    else:
                        if check_password_file == "Yes":
                            cmd = (
                                f'{exe_path} -u={user} -pf="{password_file}" -g={group} '
                                f'-mode=import -scope={scope} -action={action} '
                                f'-file="{xml_path}"'
                            )
                        else:
                            cmd = (
                                f'{exe_path} -u={user} -p={password} -g={group} '
                                f'-mode=import -scope={scope} -action={action} '
                                f'-file="{xml_path}"'
                            )

                    if EXECUTE:
                        print(f'==> Importing: {cmd}')
                        subprocess.run(cmd, shell=True, env=env1)
                    else:
                        print(cmd)


def main():
    
    user = password = password_file = group = folder_path = None
    password_provided = False
    password_file_provided = False

    # Parse command-line arguments
    for arg in sys.argv[1:]:
        if arg in ("-h", "-help", "-HELP"):
            show_help()
            return
        elif arg.startswith("-u="):
            user = arg.split("=", 1)[1].strip('"')
        elif arg.startswith("-p="):
            password = arg.split("=", 1)[1].strip('"')
            password_provided = True
        elif arg.startswith("-pf="):
            password_file = arg.split("=", 1)[1].strip('"')
            password_file_provided = True
            if os.path.isfile(password_file):
                with open(password_file, 'r') as f:
                    password = f.read().strip()
            else:
                print(f"Error: Password file '{password_file}' not found.")
                return
        elif arg.startswith("-g="):
            group = arg.split("=", 1)[1].strip('"')
        elif arg.startswith("-path="):
            folder_path = arg.split("=", 1)[1].strip('"')

    # Mutually exclusive check
    if password_provided and password_file_provided:
        print("Error: Provide either -p or -pf, not both.")
        return

    # Require at least one authentication method
    if not password and not password_file:
        print("Error: Either -p or -pf must be provided.")
        return

    # Validate remaining required arguments
    if not all([user, group, folder_path]):
        print("Error: Missing required arguments.")
        print('Usage: preference_utility.exe -u="<user>" (-p="<password>" | -pf="<password_file_path>") -g="<group>" -path="<folder_path>"')
        print('Use "-h" or "-help" for details.')
        return

    
    # Check if folder path is valid
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid folder path.")
        return
    
    # Display collected info
    # print("User Info:")
    # print(f"  Username   : {user}")
    # print(f"  Password   : {password}")
    # print(f"  Password File: {password_file if 'password_file' in locals() else 'N/A'}")
    # print(f"  Group      : {group}")
    # print(f"  Folder path: {os.path.abspath(folder_path)}")

    process_folder(folder_path, user, password, password_file, group)

if __name__ == "__main__":
    main()
