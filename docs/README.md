# A11ySpider

## Docker

The A11ySpider can be run in a Docker container using the following environment variables to configure the database connection:

- `DB_HOST` (default: `"localhost"`): the hostname or IP address of the database server
- `DB_PORT` (default: `8432`): the port number of the database server
- `DB_USER` (default: `"a11yPython"`): the username to use for authentication
- `DB_PASSWORD` (default: `"SnakeInTheWeb"`): the password to use for authentication
- `DB_NAME` (default: `"a11y"`): the name of the database to connect to

## API

[API Docs](API.md)
