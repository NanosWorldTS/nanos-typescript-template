import json
import os


def setup():
    print("Hi :) I'm the Setup Wizard! Please fill in the following few questions so I can setup your project!")

    name = read_input("Name of the Project: ")
    author = read_input("Who are you (Author): ")
    version = read_input("Version of the Project (def: 1.0.0): ", True, "1.0.0")
    proj_type = read_input_range("Type of Project (1=script,2=game-mode,3=loading-screen; def: script): ", 1, 3, 1)
    type_str = "script"
    if proj_type == 2:
        type_str = "game-mode"
    elif proj_type == 3:
        type_str = "loading-screen"

    script_create = read_input_range("Start Script Creation (1=all,2=server,3=client,4=shared; def: all): ", 1, 4, 1)

    print("Configuring package.json...")
    packagejson = read_packagejson()

    packagejson["name"] = name
    packagejson["author"] = author
    packagejson["version"] = version
    write_packagejson(packagejson)

    print("Creating Package.toml...")
    toml_lines = [
        "[package]",
        "    name = \"" + name + "\"",
        "    author = \"" + author + "\"",
        "    version = \"" + version + "\"",
        "    image = \"\"",
        "    type = \"" + type_str + "\"",
        "    force_no_map_script = false",
        "    auto_cleanup = true",
        "    packages_requirements = []",
        "    assets_requirements = []"
    ]
    write_packagetoml(toml_lines)

    print("Creating Index files...")

    if script_create == 2 or script_create == 1:
        create_dirs_and_file("src/Server/Index.ts")
    if script_create == 3 or script_create == 1:
        create_dirs_and_file("src/Client/Index.ts")
    if script_create == 4 or script_create == 1:
        create_dirs_and_file("src/Shared/Index.ts")

    print("Finished :) Have fun!")
    print()
    print("Please run \"npm install\" or \"yarn install\"!")


def create_dirs_and_file(path):
    basedir = os.path.dirname(path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)

    with open(path, 'a'):
        os.utime(path, None)


def write_packagetoml(lines):
    with open('Package.toml', 'w') as f:
        for item in lines:
            f.write("%s\n" % item)


def write_packagejson(data):
    with open('package.json', 'w') as file:
        file.write(json.dumps(data, sort_keys=True, indent=4))


def read_packagejson():
    with open('package.json', 'r') as file:
        return json.loads(file.read().replace('\n', ''))


def read_input(prompt, allow_empty=False, default=""):
    while True:
        value = input(prompt)

        if not value:
            if allow_empty:
                return default
        else:
            return value


def read_input_range(prompt, min_val=0, max_val=10, default=-1):
    while True:
        value = -1
        try:
            value = int(input(prompt))
        except ValueError:
            if default != -1:
                value = default
            else:
                continue

        if min_val <= value <= max_val:
            return value


if __name__ == '__main__':
    setup()
