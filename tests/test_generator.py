import os
import pathlib
from .common import create_one_template, ProjectGenerator, \
    copy_directory_and_contents_to_new_location, ProjectTemplate, \
    get_builtin_templates_path
import pytest
import datetime


class TestCopyDirectory:
    def test_simple_copy(self, destination_directory, dummy_templates_path):
        name = f'my_new_template{datetime.datetime.now().microsecond}'
        create_one_template(dummy_templates_path, name)
        copy_directory_and_contents_to_new_location(source=dummy_templates_path / name,
                                                    target=destination_directory)
        assert len([i for i in destination_directory.iterdir()]) > 0

    def test_destination_does_not_exist_yet(self, destination_directory, dummy_templates_path):
        destination_directory = destination_directory / 'one_level_deeper'
        name = f'my_new_template{datetime.datetime.now().microsecond}'
        create_one_template(dummy_templates_path, name)
        copy_directory_and_contents_to_new_location(source=dummy_templates_path / name,
                                                    target=destination_directory)
        assert len([i for i in destination_directory.iterdir()]) > 0

    def test_just_copy_files(self, destination_directory, dummy_templates_path):
        name = f'my_new_template{datetime.datetime.now().microsecond}'
        create_one_template(dummy_templates_path, name)
        copy_directory_and_contents_to_new_location(source=dummy_templates_path / name,
                                                    target=destination_directory,
                                                    just_files=True)
        assert len([f for f in destination_directory.iterdir()]) == 3


class TestProjectTemplate:
    def test_constructs_correctly_with_default(self, dummy_templates_path):
        pt = ProjectTemplate(dummy_templates_path / 'my_template', dummy_templates_path / 'shared')
        assert pt.template_directory is not None
        assert pt.shared_files_directory is not None
        assert pt.cicd_type is not None

    def test_constructs_with_cicd(self, dummy_templates_path):
        pt = ProjectTemplate(dummy_templates_path / 'my_template', dummy_templates_path / 'shared', 'azure')
        assert pt.template_directory is not None
        assert pt.shared_files_directory is not None
        assert pt.cicd_type is not None


class TestGenerateProjectFolder:
    @pytest.mark.parametrize('name', ['classic', 'gRPC-api', 'package', 'rest-api'])
    def test_internal_templates(self, name, builtin_templates, destination_directory):
        pg = ProjectGenerator(builtin_templates[name])
        pg.generate_template_at_destination(destination_directory)

    def test_requirements_overwrites_in_rest_api(self,
                                                 builtin_templates,
                                                 destination_directory):
        pg = ProjectGenerator(builtin_templates['rest-api'])
        pg.generate_template_at_destination(destination_directory)
        dependencies = ['flask', 'flask-cors', 'flask-swagger-ui']
        with open(destination_directory / 'requirements.txt', 'r') as f:
            contents = f.read()
            assert all(item in contents for item in dependencies)

    def test_requirements_overwrites_in_grpc_api(self,
                                                 builtin_templates,
                                                 destination_directory):
        pg = ProjectGenerator(builtin_templates['gRPC-api'])
        pg.generate_template_at_destination(destination_directory)
        dependencies = ['grpcio', 'grpcio-tools']
        with open(destination_directory / 'requirements.txt', 'r') as f:
            contents = f.read()
            assert all(item in contents for item in dependencies)

    def test_shared_template_fails(self, builtin_templates_path, destination_directory):
        with pytest.raises(ValueError):
            pt = ProjectTemplate(builtin_templates_path / 'shared', builtin_templates_path / 'shared')
            pg = ProjectGenerator(pt)
            pg.generate_template_at_destination(destination_directory)

    def test_nonsense_template_fails(self, builtin_templates_path, destination_directory):
        with pytest.raises(NotADirectoryError):
            pt = ProjectTemplate(builtin_templates_path / '_____', builtin_templates_path / 'shared')
            pg = ProjectGenerator(pt)
            pg.generate_template_at_destination(destination_directory)

    def test_protobufs_exit_in_grpc_api(self,
                                        builtin_templates,
                                        destination_directory):
        pg = ProjectGenerator(builtin_templates['gRPC-api'])
        pg.generate_template_at_destination(destination_directory)

        assert len(os.listdir(destination_directory / 'protobufs')) != 0


class TestProjectTemplateAndDestinationChecker:
    def test_valid_shared_directory_happy(self, preloaded_checker):
        preloaded_checker.check_valid_shared_directory()

    def test_shared_directory_does_not_exist(self, preloaded_checker):
        preloaded_checker.template.shared_files_directory = pathlib.Path.cwd() / 'test.txt'
        with pytest.raises(NotADirectoryError):
            preloaded_checker.check_valid_shared_directory()

    def test_valid_template_happy(self, preloaded_checker):
        preloaded_checker.check_valid_template()

    def test_template_called_shared_errors(self, preloaded_checker):
        preloaded_checker.template.template_directory = get_builtin_templates_path() / 'shared'
        with pytest.raises(ValueError):
            preloaded_checker.check_valid_template()

    def test_template_not_a_directory_errors(self, preloaded_checker):
        preloaded_checker.template.template_directory = get_builtin_templates_path() / 'test.txt'
        with pytest.raises(NotADirectoryError):
            preloaded_checker.check_valid_template()

    def test_destination_empty_happy(self, preloaded_checker):
        preloaded_checker.check_destination_empty()

    def test_destination_not_empty_errors(self, preloaded_checker):
        preloaded_checker.destination = get_builtin_templates_path() / 'classic'
        with pytest.raises(FileExistsError):
            preloaded_checker.check_destination_empty()
