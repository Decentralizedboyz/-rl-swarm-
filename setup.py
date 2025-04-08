from setuptools import setup, find_packages

setup(
    name="client_dashboard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.68.1",
        "uvicorn==0.15.0",
        "sqlalchemy==1.4.23",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.5",
        "python-dotenv==0.19.0",
        "aiohttp==3.8.1"
    ],
) 