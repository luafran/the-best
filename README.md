# Tornado Skeleton Service

Skeleton for web services implemented using tornado.

Clone this repo.

Install OS dependencies.
(May be some dependency is missing since setup.sh was not tested in a clean environment yet)

```shell
$ sudo ./install_os_dependencies.sh
`````


Run service using tox

```shell
$ tox -e runservice
```````````

Use service locally

```shell
$ curl --proxy '' 'http://localhost:10001/health?include_details=true' 
```````````

Send a request to service health

```shell
$ curl --proxy '' 'http://localhost:10001/health?include_details=true' 
```````````

Build docker image

```shell
$ sudo docker build -t quay.io/luafran/the-best . 
```````````

Run docker image

```shell
$ sudo docker run -p 10001:10001 -d -e TB_ENV=test --name the-best quay.io/luafran/the-best
```````````

Run pylint (static analysis)
Report: ci/reports/pylint/index.html

```shell
$ tox -e pylint
`````

Run flake8 (static analysis)
Report: ci/reports/flake8/index.txt

```shell
$ tox -e flake8
`````

Run unit tests
Coverage report in ci/reports/unit-tests/coverage/index.html
Test results in xunit format in ci/reports/unit-tests/nosetests.xml

```shell
$ tox -e unit-tests
`````

Regenerate environment

```shell
$ tox -r -e <env>
`````
