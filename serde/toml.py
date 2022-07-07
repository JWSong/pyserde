"""
Serialize and Deserialize in TOML format. This module depends on [tomli](https://github.com/hukkin/tomli) and [tomli-w](https://github.com/hukkin/tomli-w) packages.
"""
from typing import Type

import tomli
import tomli_w

from .compat import T
from .core import Coerce, TypeCheck
from .de import Deserializer, from_dict
from .se import Serializer, to_dict

__all__ = ["from_toml", "to_toml"]


class TomlSerializer(Serializer):
    @classmethod
    def serialize(cls, obj, **opts) -> str:
        return tomli_w.dumps(obj, **opts)


class TomlDeserializer(Deserializer):
    @classmethod
    def deserialize(cls, s, **opts):
        return tomli.loads(s, **opts)


def to_toml(obj, se: Type[Serializer] = TomlSerializer, type_check: TypeCheck = Coerce, **opts) -> str:
    """
    Serialize the object into TOML.

    You can pass any serializable `obj`. If you supply keyword arguments other than `se`,
    they will be passed in `toml_w.dumps` function.

    If you want to use the other toml package, you can subclass `TomlSerializer` and implement your own logic.
    """
    return se.serialize(to_dict(obj, reuse_instances=False, type_check=type_check), **opts)


def from_toml(
    c: Type[T], s: str, de: Type[Deserializer] = TomlDeserializer, type_check: TypeCheck = Coerce, **opts
) -> T:
    """
    Deserialize from TOML into the object.

    `c` is a class obejct and `s` is TOML string. If you supply keyword arguments other than `de`,
    they will be passed in `toml.loads` function.

    If you want to use the other toml package, you can subclass `TomlDeserializer` and implement your own logic.
    """
    return from_dict(c, de.deserialize(s, **opts), reuse_instances=False, type_check=type_check)
