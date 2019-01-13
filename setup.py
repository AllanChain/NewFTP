import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NewFTP",
    version="0.0.1",
    author="AllanChain",
    author_email="txsmlf@gmail.com",
    description="A GUI program to login the FTP system and a background program to manage FTP file downloading",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AllanChain/NewFTP",
    packages=setuptools.find_packages(),
    package_data={
        '':['*.pyw','data/*','data/Styles/*','data/Styles/Img/*']},
    install_requires=["PyYAML","python-box","pygame","tqdm","pywin32"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Development Status :: 3 - Alpha",
    ],
)
