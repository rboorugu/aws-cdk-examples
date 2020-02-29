from aws_cdk import(
    aws_ecs as ecs,
    aws_ec2 as ec2,
    core
)

class FargateService(core.Stack):

     def __init__(self, scope: core.Construct, id: str,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #initialize all the required parameters
        vpc_id = '[fill in VPC ID]'
        security_group_id = '[fill in sg id]'
        #existing subnetids for two availiability zones which 
        subnet_id_1a = '[fill in subnetid]'
        subnet_id_1b = '[fill in subnetid]'
        #name of the existing ecs cluster where the fargate service needs to be deployed 
        ecs_cluster_name = '[fill in name for cluster]'
        #get an instance of existing vpc
        vpc = ec2.Vpc.from_lookup(self, 'vpc', vpc_id=vpc_id)
        #get handle for existing security group
        security_group = ec2.SecurityGroup.from_security_group_id(self, "SG", security_group_id,
            mutable=True
        )
        #get handle for existing subnets
        subnet1a = ec2.Subnet.from_subnet_attributes(self,'subnet1a', availability_zone = 'us-east-1a', subnet_id = subnet_id_1a)
        subnet1b = ec2.Subnet.from_subnet_attributes(self,'subnet1b', availability_zone = 'us-east-1b', subnet_id = subnet_id_1b)
        vpc_subnets_selection = ec2.SubnetSelection(subnets = [subnet1a, subnet1b])
        #get handle for existing ecs cluster
        cluster = ecs.Cluster.from_cluster_attributes(self, 'test-cluster', cluster_name=ecs_cluster_name, vpc=vpc, security_groups=[security_group])
        #create fargate task definition
        task_definition = ecs.FargateTaskDefinition(self,
            "test-with-cdk",
            cpu=256, 
            memory_limit_mib=512)
        #add a container to task definition using a sample image
        container = task_definition.add_container(
            "test-with-cdk", 
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
            memory_limit_mib=256)
        #expose required ports
        port_mapping = ecs.PortMapping(
            container_port=80,
            protocol=ecs.Protocol.TCP
        )
        #adding port mappings to container
        container.add_port_mappings(port_mapping)
        #creating fargate service with all required inputs
        fargateService = ecs.FargateService(self, "test-with-cdk-service", cluster=cluster, task_definition=task_definition,vpc_subnets=vpc_subnets_selection, security_group=security_group)