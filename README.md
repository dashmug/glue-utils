# glue-utils

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

Reusable utilities for working with Glue PySpark jobs

## Installation

```
pip install glue-utils
```

## Usage

```python
from glue_utils.context import ManagedGlueContext

options = getResolvedOptions(sys.argv, [])
with ManagedGlueContext(options=options) as glue_context:
    dyf = extract(
        glue_context=glue_context,
        path="s3://awsglue-datasets/examples/us-legislators/all/persons.json",
    )
    dyf.printSchema()
```

## License

This project is licensed under the [MIT License](LICENSE).