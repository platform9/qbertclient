# Copyright 2019 Platform9
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qbertclient",
    version="0.0.12",
    author="Vann Teves",
    author_email="vann@platform9.com",
    license="Apache License 2.0",
    description="Platform9 Qbert client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/platform9/qbertclient",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=[
        'requests',
    ],
)
