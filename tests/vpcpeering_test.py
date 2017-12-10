# pylint: disable=missing-docstring, line-too-long, protected-access, E1101, C0202, E0602, W0109
import unittest
from runner import Runner


class TestE2E(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.snippet = """

            provider "aws.source" {
              region = "eu-west-2"
              skip_credentials_validation = true
              skip_get_ec2_platforms = true
            }

            provider "aws.dest" {
              region = "eu-west-2"
              skip_credentials_validation = true
              skip_get_ec2_platforms = true
            }

            module "vpcpeering" {
              source = "./mymodule"

              providers = {
                source = "aws.source"
                dest = "aws.dest"
              }
            vpc_dest_account_id = "1234"
            vpc_source_account_id = "1234"
            vpc_dest_vpc_id = "1234"
            vpc_source_vpc_id = "1234"
            vpc_source_name = "foo"
            vpc_dest_name = "bar"
            }
        """
        self.result = Runner(self.snippet).result

    def test_root_destroy(self):
        self.assertEqual(self.result["destroy"], False)

    def test_name_prefix_request(self):
        self.assertEqual(self.result['vpcpeering']["aws_vpc_peering_connection.request"]["tags.Side"], "Requester")

    def test_name_prefix_accept(self):
        self.assertEqual(self.result['vpcpeering']["aws_vpc_peering_connection_accepter.accept"]["tags.Side"], "Accepter")

    def test_request_auto_accept(self):
        self.assertEqual(self.result['vpcpeering']["aws_vpc_peering_connection.request"]["auto_accept"], "false")

    def test_accept_auto_accept(self):
        self.assertEqual(self.result['vpcpeering']["aws_vpc_peering_connection_accepter.accept"]["auto_accept"], "true")



if __name__ == '__main__':
    unittest.main()
