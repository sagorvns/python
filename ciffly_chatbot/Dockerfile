# Ciffly Chatbot - container image for AWS Lambda or ECS
FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r requirements.txt
COPY . ${LAMBDA_TASK_ROOT}/

# Lambda expects handler = lambda_function.handler
CMD [ "lambda_function.handler" ]
