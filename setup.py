from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='mousetrap',
      version='3.0.5',
      description='An X11 utility that hides the mouse pointer after a specified interval of time',
      long_description=readme(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Topic :: Utilities'
      ],
      keywords='hide mouse cursor pointer x11 xlib',
      url='https://github.com/eazar001/mousetrap',
      author='Ebrahim Azarisooreh',
      author_email='ebrahim.azarisooreh@gmail.com',
      license='MIT',
      packages=['mousetrap'],
      entry_points={"console_scripts" : ["mousetrap = mousetrap.mousetrap:main",]},
      install_requires=['python-xlib'],
      include_package_data=True,
      zip_safe=False)
