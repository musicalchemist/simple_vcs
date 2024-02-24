import os
import hashlib
import pickle

def init_vcs():
    os.makedirs('.vcs_storage', exist_ok=True)
    print("VCS initialized.")

def snapshot(directory):
    # Initialize a SHA-256 hash object to compute the snapshot's unique hash
    snapshot_hash = hashlib.sha256()
    # Prepare a dictionary to hold snapshot data, including a sub-dictionary for file contents
    snapshot_data = {'files': {}}

    # Walk through the directory, capturing the directory tree and files
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Skip files within the .vcs_storage directory to avoid self-referencing
            if '.vcs_storage' in os.path.join(root, file):
                continue
            # Construct the full path to the file
            file_path = os.path.join(root, file)
            # Open and read the file's content in binary mode
            with open(file_path, 'rb') as f:
                content = f.read()
                # Update the snapshot's hash with the file content
                snapshot_hash.update(content)
                # Store the file content in the snapshot data
                snapshot_data['files'][file_path] = content

    # Finalize the hash calculation for the snapshot
    hash_digest = snapshot_hash.hexdigest()
    # Save the list of files in the snapshot for later reference
    snapshot_data['file_list'] = list(snapshot_data['files'].keys())
    # Serialize and save the snapshot data to a file named after the snapshot's hash
    with open(f'.vcs_storage/{hash_digest}', 'wb') as f:
        pickle.dump(snapshot_data, f)

    # Print a confirmation with the unique hash of the created snapshot
    print(f"Snapshot created with hash {hash_digest}")

def revert_to_snapshot(hash_digest):
    # Construct the path to the snapshot file based on its hash
    snapshot_path = f'.vcs_storage/{hash_digest}'
    # Check if the snapshot exists; if not, print a message and exit the function
    if not os.path.exists(snapshot_path):
        print("Snapshot does not exist.")
        return

    # Load the snapshot data from the file
    with open(snapshot_path, 'rb') as f:
        snapshot_data = pickle.load(f)

    # Iterate over each file in the snapshot
    for file_path, content in snapshot_data['files'].items():
        # Ensure the directory for the file exists, creating it if necessary
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Write the file content back, restoring it to its snapshot state
        with open(file_path, 'wb') as f:
            f.write(content)

    # Prepare to identify and delete files not part of the snapshot
    current_files = set()
    # Walk through the current directory structure
    for root, dirs, files in os.walk('.', topdown=True):
        # Skip the .vcs_storage directory
        if '.vcs_storage' in root:
            continue
        # Add each file to the set of current files
        for file in files:
            current_files.add(os.path.join(root, file))

    # Create a set of files that were part of the snapshot
    snapshot_files = set(snapshot_data['file_list'])
    # Determine which files currently exist but weren't in the snapshot
    files_to_delete = current_files - snapshot_files

    # Delete each file that should not exist based on the snapshot
    for file_path in files_to_delete:
        os.remove(file_path)
        # Print a message for each file removed
        print(f"Removed {file_path}")

    # Print a confirmation of reverting to the specified snapshot
    print(f"Reverted to snapshot {hash_digest}")

if __name__ == "__main__":
    import sys
    command = sys.argv[1]

    if command == "init":
        init_vcs()
    elif command == "snapshot":
        snapshot('.')
    elif command == "revert":
        revert_to_snapshot(sys.argv[2])
    else:
        print("Unknown command.")
