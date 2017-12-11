provider "aws" {
  alias = "source"
}

provider "aws" {
  alias = "dest"
}

resource "aws_vpc_peering_connection" "request" {
  provider = "aws.source"

  auto_accept   = "false"
  peer_owner_id = "${var.vpc_dest_account_id}"
  peer_vpc_id   = "${var.vpc_dest_vpc_id}"
  vpc_id        = "${var.vpc_source_vpc_id}"

  tags {
    Side = "Requester"
  }

  tags = {
    Name = "${format("%s - %s", var.vpc_source_name, var.vpc_dest_name)}"
  }
}

resource "aws_vpc_peering_connection_accepter" "accept" {
  provider = "aws.dest"

  auto_accept               = true
  vpc_peering_connection_id = "${aws_vpc_peering_connection.request.id}"

  tags {
    Side = "Accepter"
  }

  tags = {
    Name = "${format("%s - %s", var.vpc_dest_name, var.vpc_source_name)}"
  }
}
