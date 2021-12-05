import setuptools

setuptools.setup(
    name="ooutils",
    version="0.0.2",
    author="KyuzoM",
    author_email="99549950+kyuzom@users.noreply.github.com",
    description="OO utils",
    long_description="GOO utils - Collection of Onion Omega python scripts.",
    url="https://github.com/kyuzom/ooutils",
    license="MIT",
    packages=[
        "ooutils",
    ],
    package_data={
        "ooutils": ["**/*"],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7",
)
