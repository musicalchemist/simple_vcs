# Simple Version Control System

This project is a Python-based simple version control system (VCS) designed to demonstrate the basics of file manipulation, hashing, and data serialization to track and revert changes in a directory. It's an educational tool for understanding how version control systems like Git work at a fundamental level.

## Features

- **Initialize VCS**: Set up the version control system for a specified directory.
- **Create Snapshots**: Capture the current state of the directory, including all files, and generate a unique snapshot based on the content.
- **Revert to Snapshot**: Revert the directory to a previous state represented by a specific snapshot.

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. Clone this repository to your local machine using:

   ```sh
   git clone https://github.com/musicalchemist/simple_vcs.git

   ```

2. Navigate into the cloned directory:

   ```sh
   cd simple_vcs
   ```

### Usage

1. Initialize the VCS on a directory:

   `python vcs.py init`

2. Create a snapshot of the current state of the directory:

   `python vcs.py snapshot`

3. Revert to a specific snapshot using its hash:

   `python vcs.py revert <snapshot_hash>`

### How It Works

- The snapshot function walks through the directory, creating a hash of all files and storing their content. Each snapshot is uniquely identified by a hash of its contents.

- The revert function uses the saved snapshot data to restore the directory to its previous state, including deleting files not present in the snapshot.
