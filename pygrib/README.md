## Docker Image
unusual Docker install:
  - pygrib needs to built locally with cmake3 and eccodes dependencies
  - run in this directory
  ```docker build -t pygrib-layer .```

## Layer Setup
1. Run the docker container<br>
```
docker run -ti \
  --env AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  --env AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  --env BUCKET_NAME=$BUCKET_NAME \
  eyam/pygrib-lambda-layer
```

2. Set upload ZIP from s3 to lambda layers

## Lambda Setup
- use `pygrib` lambda layer (includes `numpy` and `pyproj` dependencies) with **python3.7**
- copy code into the browser UI or upload as lambda function with `<pygrib layer arn>`
- make sure to set lambda function environment variables:

| Environment Variable Name | Value |
| ------------------------- | ----- |
| `LD_LIBRARY_PATH` | /var/lang/lib:/lib64:/usr/lib64:/var/runtime:/var/runtime/lib:/var/task:/var/task/lib:/opt/lib:/opt/python/lib/python3.7/site-packages/eccodes-2.17.0/lib |
| `ECCODES_DEFINITION_PATH` | /opt/python/lib/python3.7/site-packages/eccodes-2.17.0/share/eccodes/definitions |

## Additional Package Dependencies
If your function has additional package dependencies, follow the deployment README for how to package your code with them.


## References
Helpful guides used in making this:<br>
https://qrunch.net/@predora005/entries/seAWWAEiSmeVy7Xb?ref=qrunch<br>
https://github.com/difu/eccodes-lambda<br>
https://github.com/jswhit/pygrib
