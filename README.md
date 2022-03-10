# kartoza-full-stack-assessment
Technical assessment to implement a noise reduction on a polygon geopackage file.

The spike reduction technique implemented makes use of:
    - ramer-douglas-peucker algorithm.
    - Standard deviation.
    - Linear interpolation.

ramer-douglas-peucker algorithm is used to reduce the number of data points improving performance
with a settable tolerance depending on the accuracy required.
Using standard deviation (stdDev) the coordinates out side of the tolerence (coefficient * stdDev)
are replace with dummy values `*` which are later filled by using linear interpolation.

### Prerequiset:
    - docker
    - docker-compose
    - gnuMake (or os similar to execute makefile targets)


## Development setup:
    To get up and running just run from a bash terminal `make start` (ensure you are in the root directory of the project.)
    Then run `make migrations`.  open the url http://0.0.0.0:8000

    To display the help menu for the make targets run:
    `make help`

    To setup a local development environment run the following command:
    `make start`

    To stop all running containers run the following:
    `make stop`

    To ensure a restart of the container environments run:
    `make restart`

    To view the container logs run:
    `make logs`

    To run pre-commits:
    `make pre-commit`

    To make and run django migrations run:
    `make migrations`
