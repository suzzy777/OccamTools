from setuptools import setup

setup(
    name='occamtools',
    version='0.0.1',
    description='Analysis and synthesis tools for OCCAM hPF simulations',
    author='Morten Ledum',
    author_email='morten.ledum@gmail.com',
    packages=['occamtools'],
    install_requires=['pytest>=4.3.0',
                      'pytest-cov>=2.6.1',
                      'scikit-learn>=0.20.2',
                      'scipy>=1.2.1',
                      'numpy>=1.16.1',
                      'numba>=0.42.1',
                      'matplotlib>=3.0.2',
                      'flake8>=3.7.7',
                      'coverage>=4.5.2',
                      'codecov>=2.0.15'],
)
