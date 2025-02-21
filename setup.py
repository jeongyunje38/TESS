from setuptools import setup, find_packages


setup(
    name="TESS",
    version="0.1.0",
    description="Team-based Elo Scoring System",
    author="Yunje Jeong",
    author_email="jeongyunje04@postech.ac.kr",
    url="https://github.com/jeongyunje38/TESS",  # Update with your repository URL
    packages=find_packages(where="tess"),  # Alternatively, if you renamed your package, adjust accordingly
    package_dir={"": "tess"},  # This tells setuptools to look for packages in the "tess" directory
    install_requires=[
        # List any external dependencies here, e.g.:
        # "numpy>=1.19.0",
    ],
    entry_points={
        # Optionally, you can create console scripts to run your examples:
        "console_scripts": [
            "tess-example1=exec.example1:main",
            "tess-example2=exec.example2:main",
            "tess-example3=exec.example3:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
