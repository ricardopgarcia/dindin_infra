# DinDin Infrastructure

This repository contains the infrastructure as code (IaC) for the DinDin application using Terraform and AWS.

## Infrastructure Components

- AWS Lambda Function
- API Gateway (HTTP API)
- IAM Roles and Policies

## Prerequisites

- AWS Account
- Terraform installed
- AWS CLI configured

## Getting Started

1. Clone this repository
2. Initialize Terraform:
   ```bash
   terraform init
   ```
3. Review the planned changes:
   ```bash
   terraform plan
   ```
4. Apply the infrastructure:
   ```bash
   terraform apply
   ```

## Architecture

The infrastructure consists of a Lambda function exposed through an HTTP API Gateway. The Lambda function has the necessary IAM roles and permissions to execute and be invoked by the API Gateway.

## Security

- IAM roles follow the principle of least privilege
- API Gateway is configured with HTTP API for better performance
- Lambda permissions are strictly scoped to API Gateway invocations 