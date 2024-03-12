import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-privacy-policy-tools",
    version="0.1.2",
    author="Josef Wachtler",
    author_email="josef.wachtler@gmail.com",
    description="This is a highly configurable Django app to manage privacy policies and confirmations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wachjose88/django-privacy-policy-tools",
    packages=setuptools.find_packages(),
    python_requires='>=3.4',
    install_requires=[
        'django>=4.2.0,<4.3',
        'django-ckeditor',
        'django-tinymce'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
