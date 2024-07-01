from setuptools import setup, find_packages

setup(
    name='DanishLaw',
    version='1.0.0',
    packages=find_packages(),
    py_modules=['DanishJura'],  # This should match the module name
    entry_points={
        'console_scripts': [
            'danishlaw=DanishJura:main',  # Adjust as needed
        ],
    },
    install_requires=[
        # List your project dependencies here
        # 'somepackage>=1.0',
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A description of your project',
    url='https://github.com/sakis070864/DanishLaw',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)


