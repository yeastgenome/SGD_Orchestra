""" Create EC2 instance(s)

This scripts automates the process of creating EC2 instances. It could be added to AWs lambda :)

"""

import os, sys, stat
import boto3

EC2 = boto3.resource('ec2')

def create_key_pair():
    """ Creates key-value pair to ssh into aws """

    # create a file to store the key locally
    outfile = open('ec2-es7.pem', 'w')

    # use boto ec2 function to create pair key
    key_pair = EC2.create_key_pair(KeyName='ec2-es7')

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)

    # change mode
    #os.chmod('./ec2-keypair', stat.S_IROTH)

    print(KeyPairOut)

    outfile.write(KeyPairOut)


def create_ec2_instance(image_id, number_of_instances=1,
                        instance_type='t2.micro', keyname=None):

    """ Create ec2 instance(s)

    Parameters
    ----------
    image_id: str
        Amazon Machine Image(AMI).
        You can use this to reference an existing machine on AWS. Windows,
        Linux, whatever
    number_of_instances: int
        Number of instance to be launched.
    instance_type: str
        t2.micro is default but you can specify other machine types.
    keyname: str
        pem key value pair

    Notes
    -----
    

    """

    if number_of_instances > 0:
        instances = EC2.create_instances(ImageId=image_id, MinCount=1,
                                         MaxCount=number_of_instances,
                                         InstanceType=instance_type,
                                         KeyName=keyname)
        
        import pdb ; pdb.set_trace()

if __name__ == '__main__':
    #create_key_pair()
    create_ec2_instance("ami-02dc1fdb3b109c2fb", 4, "z1d.2xlarge", "ec2-es7")
    # ec2_client = boto3.client('ec2')
    # images = ec2_client.describe_images(Owners=['self'])
    # print(images)
    #ec2 = boto3.client('ec2')

    # Retrieves all regions/endpoints that work with EC2
    #response = ec2.describe_regions()
    #print('Regions:', response['Regions'])

    # Retrieves availability zones only for region of the ec2 object
    
    # response = ec2.describe_availability_zones()
    # print('Availability Zones:', response['AvailabilityZones'])
````
