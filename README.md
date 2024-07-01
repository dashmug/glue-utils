# glue-utils

[![PyPI - Version](https://img.shields.io/pypi/v/glue-utils)](https://pypi.org/project/glue-utils/)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/glue-utils)](https://pypi.org/project/glue-utils/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=dashmug_glue-utils&metric=ncloc)](https://sonarcloud.io/summary/overall?id=dashmug_glue-utils)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dashmug_glue-utils&metric=alert_status)](https://sonarcloud.io/summary/overall?id=dashmug_glue-utils)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=dashmug_glue-utils&metric=coverage)](https://sonarcloud.io/summary/overall?id=dashmug_glue-utils)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=dashmug_glue-utils&metric=reliability_rating)](https://sonarcloud.io/summary/overall?id=dashmug_glue-utils)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=dashmug_glue-utils&metric=security_rating)](https://sonarcloud.io/summary/overall?id=dashmug_glue-utils)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=dashmug_glue-utils&metric=sqale_rating)](https://sonarcloud.io/summary/overall?id=dashmug_glue-utils)

## Description

Reusable utilities for working with Glue PySpark and Python Shell jobs.

Enhance your AWS Glue development experience with utilities to minimize
boilerplate, boost type safety, and improve IDE auto-completion.
Streamline your workflows and reduce errors effortlessly with
`glue-utils`.

Turn the following boilerplate...

```python
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# The rest of your job's logic.

job.commit()
```

into...

```python
from glue_utils.pyspark import GluePySparkJob

job = GluePySparkJob()
sc = job.sc
glue_context = job.glue_context
spark = job.spark

# The rest of your job's logic.

job.commit()
```

## Usage in AWS Glue

To use it this library in AWS Glue, it needs to added as an
[additional python module](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html#addl-python-modules-support)
in your Glue job.

You can do this by adding an `--additional-python-modules` job parameter
with the value, `glue_utils==0.6.0`. For more information about setting
job parameters, see [AWS Glue job parameters](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html).

## Installation for local testing

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
pip install glue-utils
```
