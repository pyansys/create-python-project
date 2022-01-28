from src.generator import copy_template, get_templates, \
    generate_project_folder, replace_word_in_file
from src.main import cli, __version__, create_parser


def create_x_many_templates(path, num):
    for i in range(num):
        new_path = path / f'dummy_template_dir_{i}/src'
        new_path.mkdir(parents=True)
        populate_template(new_path)


def create_one_template(path, name):
    new_path = path / name
    new_path.mkdir(parents=True)
    populate_template(new_path)


def populate_template(new_path):
    for folder in ['doc', 'src', 'tests']:
        new_folder = new_path / folder
        new_folder.mkdir(parents=True)
    for new_file in ['README.txt', 'LICENSE.txt', 'requirements.txt']:
        create_text_file_in_directory(new_path, new_file)


def create_text_file_in_directory(directory, filename):
    with open(directory / filename, 'w') as f:
        f.write(f'generic text in {filename}')
