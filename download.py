#!/usr/bin/python

from ftplib import FTP
import os

def download_ftp_files(ftp_url, destination_folder):
    # Connect to the FTP server
    ftp = FTP(ftp_url)
    ftp.login()

    # Change directory to the specified path
    ftp.cwd("/pub/release-111/regulation/homo_sapiens/")

    # List directories and files
    files_and_dirs = []
    ftp.dir(files_and_dirs.append)

    # Loop through the directories
    for item in files_and_dirs:
        tokens = item.split()
        # Check if it's a directory
        if tokens[0].startswith("d"):
            dirname = tokens[-1]
            # Create directory if not exists
            local_dir = os.path.join(destination_folder, dirname)
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            # Change directory to the subdirectory
            ftp.cwd(dirname)
            # List files in the subdirectory
            files_in_dir = []
            ftp.dir(files_in_dir.append)
            # Loop through files and download
            for file_info in files_in_dir:
                file_tokens = file_info.split()
                filename = file_tokens[-1]
                local_filename = os.path.join(local_dir, filename)
                with open(local_filename, "wb") as f:
                    ftp.retrbinary("RETR " + filename, f.write)
            # Move back to the parent directory
            ftp.cwd("..")

    # Close the FTP connection
    ftp.quit()

if __name__ == "__main__":
    ftp_url = "ftp.ensembl.org"
    destination_folder = "/mnt/ebs/jackal/FILER2/FILER2-production/Ensembl_regulation/Downloads"
    download_ftp_files(ftp_url, destination_folder)

