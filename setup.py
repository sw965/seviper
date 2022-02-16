import setuptools
import seviper.path as path


setuptools.setup(
    name="seviper",
    version="0.0.1",
    data_files=[         # is the important part
        (path.BASE_DIRECTORY, [
            "all_poke_names.txt"
        ])               
    ],
    packages=setuptools.find_packages()
)
