from setuptools import setup, find_packages

DESCRIPTION = """
Provides template tags that simplify and enhance form rendering in Django
from within your template.

https://github.com/prestontimmons/djformtags
"""

setup(
    name="djformtags",
    version="1.0",
    author="Preston Timmons",
    author_email="prestontimmons@gmail.com",
    url="https://github.com/prestontimmons/djformtags",
    description="Simplifies and enhance form rendering in Django templates.",
    long_description=DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
