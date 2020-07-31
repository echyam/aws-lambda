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