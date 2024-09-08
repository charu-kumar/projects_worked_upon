provider "aws" {
  region = "ap-south-1"
  access_key = " "
  secret_key = " "
}

# VPC
resource "aws_vpc" "VPC-1" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Key = "Name"
    Name = "Demo"
  }
}


# Subnets
# Public
resource "aws_subnet" "Public" {
  vpc_id = aws_vpc.VPC-1.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "ap-south-1a"
  tags = {
    Key = "Name"
    Name = "Public"
  }
}



# Internet Gateway
resource "aws_internet_gateway" "IGW" {
  vpc_id = aws_vpc.VPC-1.id
  tags = {
    Key = "Name"
    Name = "gateway"
  }
}


# Route Table
# Public
resource "aws_route_table" "Public" {
  vpc_id = aws_vpc.VPC-1.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.IGW.id
  }
  tags = {
    Key = "Name"
    Name = "Public"
  }
}


# Route table Association
# Public
resource "aws_route_table_association" "RT_Aso" {
  route_table_id = aws_route_table.Public.id
  subnet_id = aws_subnet.Public.id
}


# Security Group
resource "aws_security_group" "SW-vpc" {
  name = "web-server"
  description = "allow traffic over the server"
  vpc_id = aws_vpc.VPC-1.id

  ingress {
    description = "http"
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "https"
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Network Interface
resource "aws_network_interface" "Interface-0" {
  subnet_id       = aws_subnet.Public.id
  private_ips     = ["10.0.1.150"]
  security_groups = [aws_security_group.SW-vpc.id]

  attachment {
    instance     = aws_instance.ec2-public.id
    device_index = 1
  }
}
resource "aws_eip" "EPI" {
  network_interface = aws_network_interface.Interface-0.id
  associate_with_private_ip = "10.0.1.150"
  depends_on = [aws_internet_gateway.IGW]
}

# EC2 Instances
# Public EC2
resource "aws_instance" "ec2-public" {
  ami = "ami-0522ab6e1ddcc7055"
  instance_type = "t2.micro"
  availability_zone = "ap-south-1a"
  subnet_id = aws_subnet.Public.id
  key_name = " "                                          # keypair
  associate_public_ip_address = true
  security_groups = [aws_security_group.SW-vpc.id]

  user_data = <<-EOF
                #!/bin/bash
                sudo apt update -y
                sudo apt install apache2 -y
                sudo systemctl enable apache2 && sudo systemctl start apache2
                sudo bash -c 'echo First web server > /var/www/html/index.html'
                EOF
  
  tags = {
    Key = "Name"
    Name = "Web Server"
  }
}
