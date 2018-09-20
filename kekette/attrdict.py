'''Attribute Dictionary and Lock Extensions.

Uses addict [https://github.com/mewwts/addict/].
Lock Extension from @ohjeah [https://git.io/fAQtK]
'''
from addict import Dict as Addict


class LockedDict(dict):
  """Just a helper to lock addict.Dict to prevent attribute/item lookup creating empty dictionaries instead.
  """
  def __getattr__(self, item):
    try:
      return self[item]
    except KeyError:
      raise AttributeError

  def __setattr__(self, attr, value):
    raise TypeError("Dictionary is locked.")

  def __setitem__(self, key, value):
    raise TypeError("Dictionary is locked.")

  def __hash__(self):
    return hash(frozenset(self.items()))

  @classmethod
  def lock(cls, d):
    """Recurse nested addict.Dicts and lock them.
    """
    base = {}
    for key, value in d.items():
      if isinstance(value, Addict):
        base[key] = cls.lock(value)
      elif isinstance(value, (list, tuple)):
        base[key] = type(value)(cls.lock(item) if isinstance(item, Addict) else item for item in value)
      else:
        base[key] = value
    return cls(base)


class AttrDict(Addict):
  @classmethod
  def immutable(cls, d):
    '''If d is not an instance of Addict, turn it into Addict and lock it.

    This is useful for configs and other static declarations.
    '''
    if not isinstance(d, Addict):
      return LockedDict.lock(Addict(d))
    return LockedDict.lock(d)
