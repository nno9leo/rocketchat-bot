# LLMProxy

This repository contains example code written in Python that demonstrates how to use the `LLMProxy`. The `LLMProxy` provides access to LLMs and the ability to upload documents that may be useful for additional context (e.g., RAG).
The APIs exposed are:

1. `generate()`
2. `retrieve()`
3. `pdf_upload()`
4. `text_upload()`


The repository also contains example programs for agentic workflows.

---

## Getting Started

### Running a simple Example
1. Install Python 3.x and required dependencies by running the setup script:
    ```
    bash setup.sh
    ```
    If you already have Python and pip installed, you can directly install the requirements:
    `python3 -m pip install -r requirements.txt`

2. Add your API access key to config.json
3. Execute the example Python scripts:
    ```
    python3 example_generate.py
    ```


## API reference

### generate()
The `generate()` function sends a request to LLMProxy to generate a response based on the provided parameters.

#### Example Usage
```
response = generate(
    model="4o-mini",
    system="Answer my question",
    query="What is the capital of France?",
    temperature=0.7,
    lastk=0,
    session_id='GenericSession',
)
```

For the `model` parameter the following options are available:
1. `4o-mini`
2. `anthropic.claude-3-haiku-20240307-v1:0`
3. `azure-phi3`
---

### retrieve()
The `retrieve()` function takes in a query and returns relevant context associated with a particular `session_id`.
This can be useful if the caller wants to:
1. Supply context from one `session_id` to a subsequent `generate()` call for a different `session_id`
2. Modify how the the context is to be used


#### Example Usage
```
response = retrieve(
    query = 'Tell me about Orange Jim?',
    session_id='GenericSession',
    rag_threshold = 0.5,
    rag_k = 1)
```

The API provides two filtering parameters:

- `rag_threshold` **(float)**: Controls the required similarity between the query and returned context (higher values enforce stricter similarity).
- `rag_k` **(int)**: Limits the number of context results (higher values return more relevant context).

#### Return Value
Returns a list of dictionaries, each containing:

- `doc_id` **(str)**: Identifier of the source document.
- `summary` **(str)**: LLM-generated summary of the document.
- `chunks` **(List[str])**: Relevant document chunks matching the filters.

Since chunks may come from multiple documents, results are grouped by doc_id.

##### Example Return
```
response = [
    {
        "doc_id": "doc_123",
        "summary": "This document is about an industrialist named Orange Jim",
        "chunks": [
            "Orange Jim revolutionized the citrus industry with his innovative farming techniques.",
            "His work led to a 3X increase in orange yields across multiple regions."
        ]
    },
    {
        "doc_id": "doc_456",
        "summary": "This document is about an traveller named Orange Jim",
        "chunks": [
            "In many folk tales, Orange Jim is portrayed as a traveler who shares wisdom with villagers he meets as he travels around the world in 80 days.",
        ]
    }
]

```
---

### text_upload()
The `text_upload()` function adds the provided string to the provided session's context, to be used for future `generate()` calls if relevant.
It may take some time for the provided information to be added to the session's context.

#### Example Usage
```
response = text_upload(
    text = "The purple dinosaur lives in the yellow mountains",
    strategy = 'fixed',
    description = 'Information about where the purple dinosaur lives',
    session_id='GenericSession',
)
```

For the `strategy` parameter the following options are available:
1. `smart`
2. `fixed`

When the `smart` strategy is specified, the LLMProxy uses an LLM to chunk the provided information.
The `fixed` strategy chunks the information into fixed-sized chunks of a default length.

### pdf_upload()
The `pdf_upload()` function adds the provided document in PDF format to the provided session's context.

#### Example Usage
```
response = pdf_upload(
    path = "path/to/your/document.pdf",
    strategy = 'smart',
    description = 'The provided pdf contains some information about ABC',
    session_id='GenericSession',
)
```

When uploading PDFs, it is recommended to use the `smart` strategy, although it will take some time to add the document to the session's context.

## AI Agent Examples
1. To run the agent examples, you need to install additional packages:    
    `python3 -m pip install -r agent_requirements.txt`

2. Please look at `example_agent_refine.py` and `example_agent_tool.py`. These may need to be modified to your use-case and may not run as-is.


---

