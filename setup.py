from setuptools import setup

version = {}
with open("./src/_version.py") as fp:
    exec(fp.read(), version)

CLASSIFIERS = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
]

setup(name='ansys-create-python-project',
      python_requires='>3.7',
      version=version['__version__'],
      url='',
      author='ANSYS, Inc.',
      maintainer='Babacar Fall',
      maintainer_email='babacar.fall@ansys.com',
      license='MIT',
      description='Ansys Python Project Creator',
      keywords=['python', 'ansys', 'ace'],
      packages=['ansys_create_python_project'],
      package_dir={'ansys_create_python_project': 'src'},
      entry_points={
          'console_scripts': [
              'ansys-create-python-project=ansys_create_python_project:cli',
              'acpp=ansys_create_python_project:cli',
          ]
      },
      install_requires=['coloredlogs~=15.0.1','emoji~=1.6.3'],
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      include_package_data=True,
      package_data={'src.templates': ['../*']},
      zip_safe=False,
      classifiers=CLASSIFIERS,
 )
