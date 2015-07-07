from setuptools import setup

setup(name='tasty_rest_framework',
      version='0.2',
      description='A TastyPie compatibility layer for projects migrating to Django Rest Framework.',
      url='http://github.com/erikcw/tasty_rest_framework.git',
      author='Erik Wickstrom',
      author_email='erik@erikwickstrom.com',
      license='MIT',
      packages=['tasty_rest_framework'],
      zip_safe=False,
      classifiers=[
          'Development Status :: 1 - Development/Alpha',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP',
          ])
