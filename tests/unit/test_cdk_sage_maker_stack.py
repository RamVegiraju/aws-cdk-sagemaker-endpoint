import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_sage_maker.cdk_sage_maker_stack import CdkSageMakerStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_sage_maker/cdk_sage_maker_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkSageMakerStack(app, "cdk-sage-maker")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
