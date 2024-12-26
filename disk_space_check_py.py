#!/usr/bin/env python3.8

import subprocess

'''
This program checks the disk usage of the current directory.
If the used disk space exceeds 80%, it sends an email alert.
Version 1: Basic functionality to check and report disk usage.
Version 2: Enhanced error handling and email notification.
'''

def check_disk_usage():
    try:
        # Run the 'df' command to get disk usage in human-readable format
        process = subprocess.run(['df', '-h', '.'], capture_output=True, text=True, timeout=5)
        process.check_returncode()  # Raise an error if the command fails
        output = process.stdout
        return output

    except subprocess.CalledProcessError as e:
        msg = f"Error occurred: {e}"
        return msg

    except subprocess.TimeoutExpired:
        msg = "The command timed out."
        return msg

    except Exception as e:
        msg = f"An unexpected error occurred: {e}"
        return msg

def process_text(output):
    lines = output.splitlines()
    if len(lines) < 2:
        return None  # Not enough lines to process

    # Extract the relevant disk space information from the second line
    b = lines[1].split()  
    if len(b) < 6:
        return None  # Not enough columns to process

    disk_space = b[4].rstrip('%')  # Get the used space percentage
    return int(disk_space)  # Convert to integer

def insufficient_prompt(disk_space):
    if disk_space is not None:
        if disk_space > 80:
            # Send an email alert if disk usage exceeds 80%
            current_usage = disk_space
            process2 = subprocess.run(
                ["mail", "-s", "Disk Alert!", "jyma_x@oppstar.com.my"],
                input=f"Max usage exceeded. Disk usage at {current_usage}%",
                text=True
            )
            print("OH NO!!! Disk space is critically low!")
        else:
            print("Disk space is sufficient.")
    else:
        print("Could not determine disk space.")

# Main execution
output = check_disk_usage()
disk_space = process_text(output)
insufficient_prompt(disk_space)


