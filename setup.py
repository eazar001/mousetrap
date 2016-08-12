from setuptools import setup

setup(name='mousetrap',
      version='3.0.2',
      description='An X11 utility that hides the mouse pointer after a specified interval of time',
      url='https://github.com/eazar001/mousetrap',
      author='Ebrahim Azarisooreh',
      author_email='ebrahim.azarisooreh@gmail.com',
      license='MIT',
      install_requires=['python-xlib'],
      scripts=['mousetrap/mousetrap.py'],
      zip_safe=False)
