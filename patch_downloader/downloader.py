#!/usr/bin/env python3
import requests
import base64
from subprocess import call
import time
import getpass
from pathlib import Path
from utils import CONS

name_matrix = {
    "4.2.0": "turing",
    "4.4.0": "wilkes"
}

configs = {
    "kernel": "4.4.0",
    "patch_list": "./patch.list"
}

PATCH_BASE = CONS["PATCH_BASE"]
UPDATE_BASE = CONS["UPDATE_BASE"]

def download(patch_number, session):
    if "WSO2-CARBON-PATCH" in patch_number:
        patch_name = patch_number
        patch_naming_segments = patch_name.split('-')
        patch_number = patch_naming_segments[-1]
        configs["kernel"] = patch_naming_segments[-2]
        kernel_name = name_matrix[configs["kernel"]]
    else:
        kernel_name = name_matrix[configs["kernel"]]
        patch_name = "WSO2-CARBON-PATCH-{kernel_version}-{patch_number}".format(kernel_version=configs["kernel"],
                                                                                patch_number=patch_number)
    file_name = "{patch_name}.zip".format(patch_name=patch_name)
    request_url = PATCH_BASE.format(kernel_name=kernel_name, patch_number=patch_number, kernel_version=configs["kernel"],
                                  file_name=file_name)
    current_file_path = './downloads/{file_name}'.format(file_name=file_name)
    current_file = Path(current_file_path)
    if not current_file.is_file():
        print("zip file not exists!")
        result = downloader(session, request_url, current_file_path)
        if not result:
            print("Retrying as update")
            file_name = file_name.replace("-PATCH-", "-UPDATE-")
            current_file_path = './downloads/{file_name}'.format(file_name=file_name)
            request_url = UPDATE_BASE.format(kernel_name=kernel_name, patch_number=patch_number, kernel_version=configs["kernel"],
                                  file_name=file_name)
            result = downloader(session, request_url, current_file_path)
            if not result:
                return False
    current_file = Path(current_file_path)
    if current_file.is_file():
        print("Unziping {}".format(file_name))
        call(["unzip", "./downloads/{}".format(file_name), "-d", "./downloads/"])
        call(["cp", "-R", "./downloads/{}/patch{}".format(patch_name,
                                                          patch_number), "./downloads/patches/"])
    return True


def downloader(session, request_url, current_file_path):
    print("Downloading {}".format(request_url))
    response = session.get(request_url)
    if response.ok:
        with open(current_file_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print("*** WARNING! Can't download {} \n Reason: {} <{}>".format(current_file_path,
                                                                   response.reason, response.status_code))
        return False


def connection():
    session = requests.Session()
    session.headers['Authorization'] = 'Basic ' + base64.b64encode(
        "{}:{}".format(configs["username"], configs["password"]).encode()).decode()
    return session


def main():
    if "username" not in configs:
        configs["username"] = input("Enter WSO2 OT username: ")
    configs["password"] = getpass.getpass("Enter password for {}: ".format(configs['username']))
    kernel = input(
        "Enter Carbon Kernel version number (Ignore if given the full patch name) (Default 4.4.0): ")
    patch_list_path = input(
        "Enter path to patch list file (Default ./patch.list): ")
    if kernel:
        configs["kernel"] = kernel
    if patch_list_path:
        configs["patch_list"] = patch_list_path
    connection_session = connection()
    patch_entries = {}
    with open(configs['patch_list'], 'r') as patch_list:
        for patch in patch_list.readlines():
            patch_number = patch.split("patch")[-1].strip()
            result = download(patch_number, connection_session)
            patch_entries[patch_number] = result
    print("Total patches = {}".format(len(patch_entries)))
    print("\tResults")
    failed = {}
    for patch_number in patch_entries:
        print("Patch name {}  =======> {}".format(patch_number,patch_entries[patch_number]))
        if not patch_entries[patch_number]:
            failed[patch_number] = patch_entries[patch_number]

    print("Failed count ====> {}".format(len(failed)))
    for patches in failed:
        print("!FAILED! Patch name {}  =======> {}".format(patches,failed[patches]))


if __name__ == '__main__':
    main()
