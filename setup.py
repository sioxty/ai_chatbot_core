from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="ai_chatbot_core",  # Library name                                  
    version= "0.2.0",  # Version
    
    install_requires=[
        "aiohttp"
    ],
    description="A lightweight AI  library for building chatbot applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    author="sioxty",
    author_email="maksymslushayev@gmail.com",
    
    packages=[
        "ai_chatbot_core",
    ],
    url="https://github.com/sioxty/ai_chatbot_core", 
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version
)
