import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iitbbscliupdates",
    version="0.0.1",
    author="Atharva Kulkarni",
    author_email="amk11@iitbbs.ac.in",
    description="CLI for IIT Bhubaneswar updates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/IronVenom/IIT-Bhubaneswar-CLI',
    packages=setuptools.find_packages(),
    install_requires  = ['Click','requests','bs4','prettytable','setuptools','lxml'],
    entry_points = '''
    [console_scripts]
    iitbbscli  = iitbbscli.app:main
    '''
)