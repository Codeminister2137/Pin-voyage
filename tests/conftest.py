import os


DEFAULT_TEST_ENV = {
    "POSTGRES_HOST": "localhost",
    "POSTGRES_PORT": "5432",
    "POSTGRES_DB": "pin_voyage_test",
    "POSTGRES_USER": "test_user",
    "POSTGRES_PASSWORD": "test_password",
}


for key, value in DEFAULT_TEST_ENV.items():
    os.environ.setdefault(key, value)
