"""
(c)  Copyright  [2018-2023]  OpenText  or one of its
affiliates.  Licensed  under  the   Apache  License,
Version 2.0 (the  "License"); You  may  not use this
file except in compliance with the License.

You may obtain a copy of the License at:
http://www.apache.org/licenses/LICENSE-2.0

Unless  required  by applicable  law or  agreed to in
writing, software  distributed  under the  License is
distributed on an  "AS IS" BASIS,  WITHOUT WARRANTIES
OR CONDITIONS OF ANY KIND, either express or implied.
See the  License for the specific  language governing
permissions and limitations under the License.
"""
from typing import Literal, Optional, Union


def bool_validator(val: bool) -> Literal[True]:
    if isinstance(val, bool):
        return True
    else:
        raise ValueError("The option must be a boolean.")


def in_validator(values: list) -> Literal[True]:
    def in_list(val: str):
        if isinstance(val, str) and val in values:
            return True
        else:
            raise ValueError(f"The option must be in [{'|'.join(values)}].")

    return in_list


def optional_bool_validator(val: Optional[bool]) -> Literal[True]:
    if isinstance(val, bool) or val == None:
        return True
    else:
        raise ValueError("The option must be a boolean or None.")


def optional_positive_int_validator(val: Optional[int]) -> Literal[True]:
    if (isinstance(val, int) and val >= 0) or val == None:
        return True
    else:
        raise ValueError("The option must be positive.")


def str_validator(val: str) -> Literal[True]:
    if isinstance(val, str):
        return True
    else:
        raise ValueError("The option must be a string.")


def st_positive_int_validator(val: int) -> Literal[True]:
    if isinstance(val, int) and val > 0:
        return True
    else:
        raise ValueError("The option must be strictly positive.")