"""
python-hcalendar is a basic hCalendar parser
"""

__version_info__ = {
    'major': 0,
    'minor': 1,
    'micro': 4,
    'releaselevel': 'final',
}

def get_version():
    """
    Return the formatted version information
    """
    vers = ["%(major)i.%(minor)i" % __version_info__, ]

    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final':
        vers.append('%(releaselevel)s' % __version_info__)
    return ''.join(vers)

__version__ = get_version()

try:
    from .hcalendar import hCalendar
except ImportError:
    pass

__all__ = ['hCalendar']
