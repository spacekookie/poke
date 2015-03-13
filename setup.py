from setuptools import setup, find_packages

execfile('src/version.py')

setup(
    name='poke',
    version=__version__,
    url='http://github.com/SpaceKookie/poke/',
    license='GNU General Public License v3.0',
    author='Katharina Sabel',
    author_email='katharina.sabel@2rsoftworks.de',
    description='SSH Connection Utility',
    entry_points={'console_scripts': ['poke = poke.poke:run', 'add-poke-server = poke.add_poke_server:run']},
    packages=['poke'],
    include_package_data=True,
    platforms='any',
    zip_safe=False,
    install_requires=[
          'advoptparse',
      ],
)
