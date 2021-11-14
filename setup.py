from setuptools import find_packages, setup

install_requires = [
    "requests"
]

setup(
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
)
