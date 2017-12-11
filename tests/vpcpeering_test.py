# pylint: disable=missing-docstring, line-too-long, protected-access, E1101, C0202, E0602, W0109
import unittest
from runner import Runner


class TestE2E(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.snippet = """

            provider "aws" {
              region = "eu-west-2"
              skip_credentials_validation = true
              skip_get_ec2_platforms = true
            }

            provider "aws" {
              alias = "APPS"
              region = "eu-west-2"
              skip_credentials_validation = true
              skip_get_ec2_platforms = true
            }

            provider "aws" {
              alias = "MOCK"
              region = "eu-west-2"
              skip_credentials_validation = true
              skip_get_ec2_platforms = true
            }

            resource "aws_vpc" "source" {
              provider   = "aws.APPS"
              cidr_block = "10.0.0.0/16"

              tags {
                  Name = "sourcevpc"
                }
            }

            resource "aws_vpc" "dest" {
              provider   = "aws.MOCK"
              cidr_block = "10.2.0.0/16"

               tags {
                 Name = "destvpc"
               }
             }

            module "vpcpeering" {
              source = "./mymodule"

              providers = {
                aws.source = "aws.APPS"
                aws.dest = "aws.MOCK"
              }
            vpc_dest_account_id = "12345"
            vpc_dest_vpc_id = "${aws_vpc.dest.id}"
            vpc_source_vpc_id = "${aws_vpc.source.id}"
            }
        """
        self.result = Runner(self.snippet).result

    def test_root_destroy(self):
        self.assertEqual(self.result["destroy"], False)

    def test_request_auto_accept(self):
        self.assertEqual(self.result['vpcpeering']["aws_vpc_peering_connection.request"]["auto_accept"], "false")

    def test_accept_auto_accept(self):
        self.assertEqual(self.result['vpcpeering']["aws_vpc_peering_connection_accepter.accept"]["auto_accept"], "true")



if __name__ == '__main__':
    unittest.main()
