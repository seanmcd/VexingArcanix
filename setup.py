import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'pyramid_beaker',
    'scipy',
    ]

setup(name='VexingArcanix',
      version='0.0',
      description='VexingArcanix',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Sean M',
      author_email='sean@stronglyemergent.com',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='vexingarcanix',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = vexingarcanix:main
      [console_scripts]
      populate_VexingArcanix = vexingarcanix.scripts.populate:main
      """,
      )
