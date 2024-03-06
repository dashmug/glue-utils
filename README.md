# glue-utils

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

Reusable utilities for working with Glue PySpark jobs

## Installation

### As a runtime (or production) dependency...

```sh
pip install glue-utils
```

### For development...

This library does not include `pyspark` and `aws-glue-libs` as 
dependencies as they are already pre-installed in Glue's runtime 
environment.

To help in developing your Glue jobs locally in your IDE, it is helpful 
to install `pyspark` and `aws-glue-libs`. Unfortunately, `aws-glue-libs` 
is not available through PyPI so we can only install it from its git 
repository.

```sh
pip install pyspark==3.3.0
pip install git+https://github.com/awslabs/aws-glue-libs.git@master
```

To make your local environment as close to Glue's runtime as possible, 
use the versions specified in [this document](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html#glue-modules-provided).

## Documentation

For more details on what you can use this library for, check out the 
[project wiki](https://github.com/dashmug/glue-utils/wiki).