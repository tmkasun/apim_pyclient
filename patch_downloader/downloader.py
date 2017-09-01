import requests
import base64
from subprocess import call
import time

name_matrix = {
    "4.2.0": "turing",
    "4.4.0": "wilkes"
}

configs = {
    "kernel": "4.4.0",
    "patch_list": "./patch.list"
}

base_url = "https://svn.wso2.com/wso2/custom/projects/projects/carbon/{kernel_name}/patches/patch{patch_number}/{file_name}"


def download(patch_number, session):
    kernel_name = name_matrix[configs["kernel"]]
    patch_name = "WSO2-CARBON-PATCH-{kernel_version}-{patch_number}".format(kernel_version=configs["kernel"],
                                                                            patch_number=patch_number)
    file_name = "{patch_name}.zip".format(patch_name=patch_name)
    request_url = base_url.format(kernel_name=kernel_name, patch_number=patch_number, kernel_version=configs["kernel"],
                                  file_name=file_name)
    response = session.get(request_url)
    if response.ok:
        print("Downloading {}".format(file_name))
        with open('./downloads/{file_name}'.format(file_name=file_name), 'wb') as f:
            f.write(response.content)
        print("Unziping {}".format(file_name))
        call(["unzip", "./downloads/{}".format(file_name), "-d", "./downloads/"])
        call(["cp", "-R", "./downloads/{}/patch{}".format(patch_name, patch_number), "./downloads/patches/"])
    else:
        print("*** ERROR Downloading {}".format(file_name))

def connection():
    session = requests.Session()
    session.headers['Authorization'] = 'Basic ' + base64.b64encode(
        "{}:{}".format(configs["username"], configs["password"]).encode()).decode()
    return session


def main():
    if "username" not in configs:
        configs["username"] = input("Enter WSO2 OT username: ")
    configs["password"] = input("Enter password for {}: ".format(configs['username']))
    kernel = input("Enter Carbon Kernel version number (Default 4.4.0): ")
    patch_list = input("Enter path to patch list file (Default ./patch.list): ")
    if kernel:
        configs["kernel"] = kernel
    if patch_list:
        configs["patch_list"] = patch_list
    connection_session = connection()
    with open(configs['patch_list'], 'r') as f:
        for patch in f.readlines():
            patch_number = patch.split("patch")[-1].strip()
            download(patch_number, connection_session)


if __name__ == '__main__':
    main()
