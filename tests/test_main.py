from .common import cli, create_parser, get_builtin_templates_path, \
    add_project_name_to_files
import pytest
import sys
import pathlib
import os


class TestCLI:
    @pytest.mark.parametrize('flags', [[], ['--Name', 'thing'], ['--Template', 'classic']])
    def test_version_prefixes(self, flags):
        sys.argv = ['', '--version']
        sys.argv.extend(flags)
        with pytest.raises(SystemExit):
            cli()

    @pytest.mark.parametrize('flags', [[], ['--Name', 'thing'], ['--Template', 'classic']])
    def test_version_suffixes(self, flags):
        sys.argv = [''] + flags
        sys.argv.extend(['--version'])
        with pytest.raises(SystemExit):
            cli()

    @pytest.mark.parametrize('template', ['classic', 'package', 'gRPC-api', 'rest-api'])
    def test_generate_projects(self, template, destination_directory):
        sys.argv = ['', '--Name', 'my_proj', '--Template', template]
        cli(root_folder=destination_directory)

    def test_no_name_exits(self):
        sys.argv = ['', '--Template', 'classic']
        with pytest.raises(SystemExit):
            cli()

    @pytest.mark.parametrize('flags', [[], ['--Name', 'thing'], ['--Template', 'classic']])
    def test_templates_flag_exits(self, flags):
        sys.argv = ['', '--templates'] + flags
        with pytest.raises(SystemExit):
            cli()


class TestCreateParser:
    @pytest.mark.parametrize('flag', ['--Name', '-n'])
    def test_name(self, flag):
        sys.argv = ['', flag, 'my_proj']
        parser = create_parser()
        assert parser.parse_args().Name == 'my_proj'

    @pytest.mark.parametrize('flag', ['--Template', '-t'])
    def test_template(self, flag):
        sys.argv = ['', flag, 'classic']
        parser = create_parser()
        assert parser.parse_args().Template == 'classic'


class TestGetTemplatesPath:
    def test_builtin_path(self):
        tests_directory = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        expected_templates_directory = tests_directory.parent / 'src' / 'templates'
        actual_templates_directory = get_builtin_templates_path()
        assert actual_templates_directory == expected_templates_directory


class TestApplyTemplate:
    @pytest.mark.parametrize('proj_name', ['new', 'new2', '2new', '22',
                                           'new two', ' new '])
    def test_project_name_rename(self, proj_name, tmp_path):
        s = '$project_name'
        test_files = [tmp_path / f'test{suffix}'
                      for suffix in ['.py', '.txt', '.md']]
        for test_file in test_files:
            with open(test_file, 'w') as f:
                f.write(s)
        add_project_name_to_files(test_files, proj_name)
        for test_file in test_files:
            with open(test_file, 'r') as f:
                s = f.read()
            assert proj_name in s

    @pytest.mark.parametrize('proj_name', ['new-2', 'new', 'new_2'])
    def test_project_name_rename_removes_hyphens_in_setup_dot_py(self,
                                                                 proj_name,
                                                                 tmp_path):
        s = '$project_name'
        test_files = [tmp_path / f'setup{suffix}'
                      for suffix in ['.py', '.txt', '.md']]
        for test_file in test_files:
            with open(test_file, 'w') as f:
                f.write(s)
        add_project_name_to_files(test_files, proj_name)
        for test_file in test_files:
            with open(test_file, 'r') as f:
                s = f.read()
            if test_file.suffix == '.py':
                assert proj_name.replace('-', '_') in s
            else:
                assert proj_name in s
