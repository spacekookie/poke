from setuptools import setup, find_packages

execfile('poke/version.py')

setup(
    name='poke',
    version=__version__,
    url='http://github.com/SpaceKookie/poke/',
    license='GNU General Public License v3.0',
    author='Katharina Sabel',
    author_email='katharina.sabel@2rsoftworks.de',
    description='SSH Connection Utility',
    entry_points={'console_scripts': ['poke = poke.poke:run', 'poke-config-manager = poke.poke_config_manager:run']},
    packages=['poke'],
    include_package_data=True,
    platforms='any',
    zip_safe=False,
    install_requires=[
          'advoptparse',
      ],
    package_data={
        'poke': ['controllers/**']
    }
)
