# Copyright 2024 Amazon.com and its affiliates; all rights reserved.
# This file is AWS Content and may not be duplicated or distributed without permission

"""
This module contains a helper class for building and using Knowledge Bases for Amazon Bedrock.
The KnowledgeBasesForAmazonBedrock class provides a convenient interface for working with Knowledge Bases.
It includes methods for creating, updating, and invoking Knowledge Bases, as well as managing
IAM roles and OpenSearch Serverless. Here is a quick example of using
the class:

    >>> from knowledge_base import KnowledgeBasesForAmazonBedrock
    >>> kb = KnowledgeBasesForAmazonBedrock()
    >>> kb_name = "my-knowledge-base-test"
    >>> kb_description = "my knowledge base description"
    >>> data_bucket_name = "<s3_bucket_with_kb_dataset>"
    >>> kb_id, ds_id = kb.create_or_retrieve_knowledge_base(kb_name, kb_description, data_bucket_name)
    >>> kb.synchronize_data(kb_id, ds_id)

Here is a summary of the most important methods:

- create_or_retrieve_knowledge_base: Creates a new Knowledge Base or retrieves an existent one.
- synchronize_data: Syncronize the Knowledge Base with the
"""
import json
import boto3
import time
from botocore.exceptions import ClientError
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth, RequestError
import pprint
from retrying import retry
import random

valid_embedding_models = [
    "cohere.embed-multilingual-v3", "cohere.embed-english-v3", "amazon.titan-embed-text-v1",
    "amazon.titan-embed-text-v2:0"
]
pp = pprint.PrettyPrinter(indent=2)


def interactive_sleep(seconds: int):
    """
    Support functionality to induce an artificial 'sleep' to the code in order to wait for resources to be available
    Args:
        seconds (int): number of seconds to sleep for
    """
    dots = ''
    for i in range(seconds):
        dots += '.'
        print(dots, end='\r')
        time.sleep(1)


class KnowledgeBasesForAmazonBedrock:
    """
    Support class that allows for:
        - creation (or retrieval) of a Knowledge Base for Amazon Bedrock with all its pre-requisites
          (including OSS, IAM roles and Permissions and S3 bucket)
        - Ingestion of data into the Knowledge Base
        - Deletion of all resources created
    """
