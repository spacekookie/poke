from setuptools import setup, find_packages

setup(
    name='poke',
    version='0.5.0',
    url='http://github.com/SpaceKookie/Poke/',
    license='Apache Software License',
    author='Katharina Sabel',
    author_email='katharina.sabel@2rsoftworks.de',
    description='SSH Connection Utility',
    entry_points={'console_scripts': ['poke = poke.Poke:run']},
    packages=['poke', 'poke.controllers'],
    include_package_data=True,
    platforms='any',
    zip_safe=False,
    package_data={
        'poke': ['controllers/**']
    }
)
