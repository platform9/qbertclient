#  Copyright 2019 Platform9
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Utility functions for converting a list of objects to dictionaries keyed by 'path'
"""


def _get_val_at_path(dct, path):
    for key in path.split('.'):
        dct = dct[key]
    return dct


def keyed_list_to_dict(lst, path):
    """
    Utility function for converting a list to a dictionary keyed by 'path'
    :param lst: The list to convert to a dictionary
    :param path: The key to use for the list to dictionary conversion
    :return: a dictionary version of the list keyed by 'path'
    """
    return {_get_val_at_path(elem, path): elem
            for elem in lst}
