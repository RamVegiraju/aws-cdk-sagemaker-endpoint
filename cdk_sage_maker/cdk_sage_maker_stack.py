from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_sagemaker as sagemaker)

class CdkSageMakerStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        #Model data: s3://sagemaker-us-east-1-474422712127/model.tar.gz
        sklearn_model = core.CfnParameter(
            self,
            "model",
            type="String",
            default=None,
        ).value_as_string

        sklearn_data = core.CfnParameter(
            self,
            "data",
            type="String",
            default=None,
        ).value_as_string


        image_uri = "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:0.23-1-cpu-py3"
        env = {"SAGEMAKER_PROGRAM": "inference.py", "SAGEMAKER_SUBMIT_DIRECTORY": "s3://sagemaker-us-east-1-474422712127/model.tar.gz"}
        container = sagemaker.CfnModel.ContainerDefinitionProperty(model_data_url=sklearn_data, image=image_uri, environment=env)

        # creates SageMaker Model Instance
        model = sagemaker.CfnModel(
            self,
            "sklearn_model",
            execution_role_arn="arn:aws:iam::474422712127:role/sagemaker-role-BYOC",
            primary_container=container,
            model_name=f'model-{sklearn_model.replace("_","-").replace("/","--")}',
        )
        
        endpoint_configuration = sagemaker.CfnEndpointConfig(
            self,
            "sklearn_endpoint_config",
            endpoint_config_name=f'config-{sklearn_model.replace("_","-").replace("/","--")}',
            production_variants=[
                sagemaker.CfnEndpointConfig.ProductionVariantProperty(
                    initial_instance_count=1,
                    instance_type="ml.c5.xlarge",
                    model_name=model.model_name,
                    initial_variant_weight=1.0,
                    variant_name=model.model_name,
                )
            ],
        )

        # Creates Real-Time Endpoint
        endpoint = sagemaker.CfnEndpoint(
            self,
            "sklearn_endpoint",
            endpoint_name=f'endpoint-{sklearn_model.replace("_","-").replace("/","--")}',
            endpoint_config_name=endpoint_configuration.endpoint_config_name,
        )
