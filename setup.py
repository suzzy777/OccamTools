from setuptools import setup

setup(
    name='occamtools',
    packages=['occamtools'],
    url='https://github.com/mortele/OccamTools',
    version='0.0.0',
    license='GPL-3',
    description='Analysis and synthesis tools for OCCAM hPF simulations',
    tags=['occammd', 'hpf', 'md'],
    author='Morten Ledum',
    author_email='morten.ledum@gmail.com',
    install_requires=[
        'pytest>=4.3.0',
        'pytest-cov>=2.6.1',
        'scikit-learn>=0.20.2',
        'scipy>=1.2.1',
        'numpy>=1.16.1',
        'numba>=0.42.1',
        'matplotlib>=3.0.2',
        'flake8>=3.7.7',
        'coverage>=4.5.2',
        'tqdm>=4.31.1'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.7'
)
