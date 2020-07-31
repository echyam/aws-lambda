# Packaging for Lambda Deployment Built Locally

### 1. Figure out which packages are not provided in the Lambda environment
Save those packages and their versions in a `requirements.txt` file
Make sure your Python version (FROM base image tag) matches with what will be running on Lambda.

### 2. Install extra packages to a ZIP
```bash
mkdir package
pip install --target ./package -r requirements.txt
cd package
zip -r9 ./function.zip .
```

### 3. Add code to package
Make a local copy of all required code (main file, any configs, local modules)
```bash
mv function.zip ../function.zip
cd ..
zip -g function.zip code_file.py
zip -g function.zip util.py
zip -g function.zip config.yaml
```
Make sure any code is in the same relative directory structure
check:
```bash
unzip -l function.zip
```

### 4. Upload ZIP to s3

### 5. Create/Update Lambda function to point to uploaded ZIP

### 6. Setup triggers etc.

<hr>

# Packaging for Lambda Deployment Using `lambci/lambda` Docker Image
### 1. Pick a base image to build from
Available images are on https://hub.docker.com/r/lambci/lambda/tags.  Pick one based on what runtime you need to use.
Make sure to grab the image with the right tag: e.g. [python3.7](https://hub.docker.com/layers/lambci/lambda/build-python3.7/images/sha256-3760581362b98ace7670571a2e314bc43fe2765b52d85b8aec5ca255947de736?context=explore)
You can either just run a container off of that directly and compile your libraries and push in that environment, or you can follow the instructions [here](https://github.com/lambci/docker-lambda#build-examples) to build your own docker image and automate installing your packages, creating a ZIP with your code, and uploading the ZIP to lambda/s3.  The rest of the instructions are for the latter.

### 2. Find requirements.txt file
example:
```
numpy==1.18.5
pandas==1.0.5
geopandas==0.8.1
```

### 3. Find aws-login.py file
This is assuming you cannot get an `AWS ACCESS KEY`.  If you can, feel free to set the KEY ID and SECRET KEY as environment variables and pass them as runtime arguments when running the container.
Add these lines to the end of dockerfile:
```
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
RUN mkdir ~/.aws && \
    touch ~/.aws/credentials && \
    echo [saml] >> ~/.aws/credentials && \
    echo aws_access_key_id=$AWS_ACCESS_KEY_ID >> ~/.aws/credentials && \
    echo aws_secret_access_key=$AWS_SECRET_ACCESS_KEY >> ~/.aws/credentials
```

### 4. Build Docker Image
Make sure `requirements.txt`, `function_code.py`, and `aws-login.py` are in the same file directory as `Dockerfile`.
Build the image!
```docker build -t lambda-deployment .```

### 5. Run the Docker Container
```docker run -it lambda-deployment bash```

If you have the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from (3), pass them as run arguments here:
```docker run -ti --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} lambda-deployment bash```

### 6. Login to AWS (inside container)
If you didn't have an AWS ACCESS KEY, you need to login using the `aws-login.py` script that was copied in.
Run the script, login with LDAP credentials, and select the role you need.
```python aws-login.py```

### 7. Upload Lambda Code (inside container)
Run the upload script!
```./upload.sh```


## Dockerfile Example
**Make sure to rename `function_code.py` and `function_name.zip` for your function!**<br>
**If using a different s3 bucket/path, replace `bucket-name` and the `/deployments` path!**
```
FROM lambci/lambda:build-python3.7
USER root
ENV AWS_DEFAULT_REGION us-west-2

# copy in requirements
COPY ./requirements.txt .

# install package dependencies
RUN pip install -r requirements.txt --target .
RUN rm -r *.dist-info __pycache__

# copy in source file
COPY ./function_code.py .

# create ZIP
RUN zip -9yr lambda.zip .

# install packages for running aws login script
RUN pip install boto requests bs4

RUN mkdir /.aws
COPY ./aws-login.py .

# RUN echo "aws lambda update-function-code --function-name function-name --zip-file fileb://lambda.zip --profile saml" >> update.sh
RUN echo "aws s3 cp lambda.zip s3://bucket-name/deployments/function_name.zip --profile saml" >> upload.sh
RUN chmod u+x upload.sh
```