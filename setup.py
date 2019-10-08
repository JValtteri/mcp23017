import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="RPi-MCP23017-Lite",
    version="0.0.1",
    author="JValtteri",
    author_email="46611993+JValtteri@users.noreply.github.com",
    description="Library to expand RPi GPIO with up to eight MCP23017 chips",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JValtteri/mcp23017",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 2 - Pre-Alpha",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)