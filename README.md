# Box AI workshop - Managing property leases

Welcome to the Box AI Workshop! This repository contains a comprehensive guide for developers to utilize the Box AI endpoints through the Box Python Next Gen SDK. In this workshop, you'll learn how to interact with various Box AI capabilities, including document processing and conversational interactions with a language model.

## Workshop Overview

In this workshop, we will cover the following Box AI endpoints:

1. **`/ai/ask`**: Engage with single and multiple documents to retrieve information
2. **`/ai/text_gen`**: Facilitate conversational interactions with a language model (LLM) across one or multiple documents
3. **`/ai/extract`**: Extract data from documents in an intuitive manner
4. **`/ai/extract_structured`**: Utilize a formal description for output structure to enhance data extraction accuracy

## Use case and context

Imagine yourself creating an application to help a user manage leases for 50 properties. You have a set of lease documents in your Box account, and your application will help users to answer questions about a single or multiple documents, as wel as extract data from those documents.

The properties vary from a single communal bed room to a three bedroom apartment. The lease documents are in Word format and contain information about the property, the tenant, the landlord, and the lease terms.

## Guides

- [Getting started](getting-started.md): Set up your environment and generate sample data.
- [Ask questions](ask-questions.md): Learn how to ask questions about documents.
- [Generate text](generate-text.md): Generate text using a language model.
- [Extract data](extract-data.md): Extract data from documents.
- [Extract structured data](extract-data-structured.md): Extract structured data from documents.
- [Box metadata extraction](extract-metadata.md): Extract data using a Box metadata template.

## Summary

This Box AI workshop demonstrates how to use Box AI's powerful features to streamline and enhance document processing. 
With endpoints like `/ai/ask`, you can quickly retrieve answers from single or multiple documents, making it easy to extract key information. 
The `/ai/extract` endpoints allows for efficient data extraction, whether in freeform or structured formats, enabling users to pull important details from unstructured documents. 
These AI capabilities help automate repetitive tasks, reduce errors, and provide deeper insights, ultimately transforming how you handle and manage documents using AI.
