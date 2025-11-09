import sys
import os
import subprocess

EXECUTE = True  # set False if you only want to print                           


def show_help():
    print(r"""
──────────────────────────────────────────────────────────────────────────
                Preference Utility - Help Guide
──────────────────────────────────────────────────────────────────────────

Usage:
  preference_utility.exe -u="<user>" -p="<password>" -g="<group>" -path="<folder_path>"

Description:
  This utility reads user credentials and locates the '*.xml' files
  in the provided folder path. It validates the folder structure and ensures
  group and role names match exactly as required.

Arguments:
  -u        Specify username
  -p        Specify password
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
    └── site
    ├── merge
    │   └── site_pref_merge.xml
    └── override
    └── site_pref_over.xml

──────────────────────────────────────────────────────────────
Notes:
  • Folder and file names are case-sensitive.
  • Make sure the structure above exists under the given path.
  • Incorrect naming Group and Role name should be exact match in TC.
  • Incorrect naming (e.g., lowercase vs uppercase) will cause processing errors.
──────────────────────────────────────────────────────────────
""")


def extract_target_from_xml(xml_path: str) -> str | None:
    """Extracts target name from xml filename like 'DBA_pref_merge.xml' → 'DBA'.
       Returns None for 'ootb' or 'site' files (to skip them)."""
    filename = os.path.basename(xml_path)
    target = filename.split('_')[0] if '_' in filename else filename.replace('.xml', '')
    target = target.strip().upper()

    # Skip unwanted targets
    if target in ("OOTB", "SITE"):
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

def process_folder(base_folder: str, user: str, password: str, group: str ):
  """Walk through folders, find XML files, and print commands."""

  env1 = os.environ.copy()

  tc_root = os.environ.get("TC_ROOT")                                                 # CHANGE
  tc_data = os.environ.get("TC_DATA")                                                 # CHANGE
  print(f'"TC_ROOT": {tc_root}')
  print(f'"TC_DATA": {tc_data}')


  #tc_root = f'D:\\abhi'
  if not tc_root:
      print("Error: TC_ROOT environment variable not set.")
      return

  # ✅ Use os.path.join to safely build path
  root_path = os.path.join(tc_root, "bin")
  exe_path = os.path.join(root_path, "preferences_manager.exe")

  for folder_name in os.listdir(base_folder):
    folder_path = os.path.join(base_folder, folder_name)

    if not os.path.isdir(folder_path):
        continue  # skip files directly under base_folder

    print(f"\nImporting {folder_name.upper()} preferences...")

    for root, _, files in os.walk(folder_path):
      for file in files:
        if file.lower().endswith(".xml"):
            xml_path = os.path.join(root, file)
            scope = determine_scope(root)
            action = determine_action(root)
            target = extract_target_from_xml(xml_path)

            if target == "unknown":
              cmd = (
                f'{exe_path} -u={user} -p={password} -g={group} -mode=import -scope={scope} -action={action} -file="{xml_path}"'
              )
            else:
              cmd = (
                f'{exe_path} -u={user} -p={password} -g={group} -mode=import -scope={scope} -target={target} -action={action} -file="{xml_path}"'
              )
            
            if EXECUTE:
                subprocess.run(cmd, shell=True, env=env1)
            else:
                print(cmd)

def main():
    
    user = password = group = folder_path = None

    # Parse command-line arguments
    for arg in sys.argv[1:]:
        if arg in ("-h", "-help", "-HELP"):
            show_help()
            return
        elif arg.startswith("-u="):
            user = arg.split("=", 1)[1].strip('"')
        elif arg.startswith("-p="):
            password = arg.split("=", 1)[1].strip('"')
        elif arg.startswith("-g="):
            group = arg.split("=", 1)[1].strip('"')
        elif arg.startswith("-path="):
            folder_path = arg.split("=", 1)[1].strip('"')

    # Validate required arguments
    if not all([user, password, group, folder_path]):
        print("Error: Missing required arguments.")
        print('Usage: preference_utility.exe -u="<user>" -p="<password>" -g="<group>" -path="<folder_path>"')
        print('Use "-h" or "-help" for details.')
        return
    
    # Check if folder path is valid
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid folder path.")
        return
    
    # Display collected info
    print("User Info:")
    print(f"  Username   : {user}")
    print(f"  Password   : {password}")
    print(f"  Group      : {group}")
    print(f"  Folder path: {os.path.abspath(folder_path)}")

    process_folder(folder_path, user, password, group)

if __name__ == "__main__":
    main()
