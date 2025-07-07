
#### ❓Question #1:

The default embedding dimension of `text-embedding-3-small` is 1536, as noted above. 

1. Is there any way to modify this dimension?
No..the dimensions are fixed for a given model, and depending on the size of the model may change across different models. Though the dimensions are fixed, the openai api allows requesting a subset of the dimensions (e.g. using fewer of the numbers in the vector form the embedding.

2. What technique does OpenAI use to achieve this?
According to their documentation OpenAI has an optional input for dimensions. This is a request for the desired number of dimensions from the total number the embedding model provides.  The api truncates the vector but does not do any additional processing. 


#### ❓Question #2:

What are the benefits of using an `async` approach to collecting our embeddings?

Async vs. Sync:
Synchronous (sync): Each API call waits for the previous one to finish before starting the next. 
Asynchronous (async): Multiple API calls can be sent out at the same time, without waiting for each one to finish before starting the next. 

If 10 documents have 50 chunks that may be manageable, but an enterprise that may do embeddings on a large history of documents may find this unsustainable without using non-blocking requests for embeddings. This may be even more significant if there's analysis on data that continually updated at scale... like analysis for customer support emails or recordings from technical support calls. 

#### ❓ Question #3:
When calling the OpenAI API - are there any ways we can achieve more reproducible outputs?

- Consistent prompt formatting - stay consistent with formatting such as whitespace, punctuation, system vs. user message boundaries
- pinning applications to specific model snapshots - consistent request to the same model snapshot should provide similar results
- Temperature - The temperature parameter controls randomness. Lowering the value reduces randomness, however to make results more reproduciable it may be good to set temperature to a fixed value (e.g. 0)


#### ❓ Question #4:

What prompting strategies could you use to make the LLM have a more thoughtful, detailed response?

What is that strategy called?
The strategy is called "Chain of Thought". Using this strategy the LLM is instructed to  "think step by step" or "explain your reasoning". The model generates intermediate reasoning steps leading to more thoughtful and detailed answers.
