import os
import json
import time
import re
from tqdm import tqdm
import numpy as np
import torch
import string
from typing import Optional, Tuple, List, Dict, Set
import argparse
import random
import asyncio
import aiohttp

from openai import AsyncOpenAI

from search.bing_search import (
    bing_web_search,
    extract_relevant_info,
    fetch_page_content,
    fetch_page_content_async,
    extract_snippet_with_context,
)

from search.brave_search import (
    brave_search_async,
    BraveSearchClient
)

from evaluate.evaluate import (
    run_evaluation,
    extract_answer_fn
)
from prompts.prompts import (
    get_web_page_reader_instruction,
    get_detailed_web_page_reader_instruction,
)
from prompts.prompts_report import (
    get_search_intent_instruction,
    get_click_intent_instruction,
    get_report_webthinker_instruction,
    get_search_plan_instruction,
    get_deep_web_explorer_instruction,
    get_write_section_instruction,
    get_section_summary_instruction,
    get_edit_article_instruction,
    get_title_instruction,
    get_click_web_page_reader_instruction,
)

from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
# nltk.download('punkt')
import langid
from transformers import AutoTokenizer

from dotenv import load_dotenv

from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env", override=True)

tokenizer = AutoTokenizer.from_pretrained(
    "/dss/dssfs05/pn39qo/pn39qo-dss-0001/.cache/huggingface/hub/models--Qwen--QwQ-32B/snapshots/976055f8c83f394f35dbd3ab09a285a984907bd0")
aux_tokenizer = AutoTokenizer.from_pretrained(
    "/dss/dssfs05/pn39qo/pn39qo-dss-0001/.cache/huggingface/hub/models--Qwen--QwQ-32B/snapshots/976055f8c83f394f35dbd3ab09a285a984907bd0")
# aux_tokenizer = AutoTokenizer.from_pretrained("/dss/dssfs05/pn39qo/pn39qo-dss-0001/.cache/huggingface/hub/models--Qwen--Qwen2.5-72B-Instruct/snapshots/495f39366efef23836d0cfae4fbe635880d2be31")


# Define special tokens
BEGIN_SEARCH_QUERY = "<|begin_search_query|>"
END_SEARCH_QUERY = "<|end_search_query|>"
BEGIN_SEARCH_RESULT = "<|begin_search_result|>"
END_SEARCH_RESULT = "<|end_search_result|>"

BEGIN_CLICK_LINK = "<|begin_click_link|>"
END_CLICK_LINK = "<|end_click_link|>"
BEGIN_CLICK_RESULT = "<|begin_click_result|>"
END_CLICK_RESULT = "<|end_click_result|>"

BEGIN_WRITE_SECTION = "<|begin_write_section|>"
END_WRITE_SECTION = "<|end_write_section|>"
BEGIN_EDIT_ARTICLE = "<|begin_edit_article|>"
END_EDIT_ARTICLE = "<|end_edit_article|>"
BEGIN_CHECK_ARTICLE = "<|begin_check_article|>"
END_CHECK_ARTICLE = "<|end_check_article|>"

error_indicators = [
    'limit exceeded',
    'Error fetching',
    'Account balance not enough',
    'Invalid bearer token',
    'HTTP error occurred',
    'Error: Connection error occurred',
    'Error: Request timed out',
    'Unexpected error',
    'Please turn on Javascript',
    'Enable JavaScript',
    'port=443',
    'Please enable cookies',
]


def parse_args():
    parser = argparse.ArgumentParser(description="Run Search-o1 for various datasets and models.")
    parser.add_argument('--single_question', type=str, default=None,
                        help="Single question to process instead of dataset")
    parser.add_argument('--dataset_name', type=str, required=False, default='custom',
                        help="Name of the dataset to use. Supported datasets include: regular QA datasets, livecode, "
                             "supergpqa, webwalker, openthoughts, glaive, and special datasets like math500, gpqa, aime, "
                             "amc, gaia, hle, limo, and strongreject.")
    parser.add_argument('--split', type=str, required=False, default='test', help="Dataset split to use.")
    parser.add_argument('--subset_num', type=int, default=-1,
                        help="Number of examples to process. Defaults to all if not specified.")

    parser.add_argument('--temperature', type=float, default=0.7, help="Sampling temperature.")
    parser.add_argument('--top_p', type=float, default=0.8, help="Top-p sampling parameter.")
    parser.add_argument('--min_p', type=float, default=0.05, help="Minimum p sampling parameter.")
    parser.add_argument('--top_k_sampling', type=int, default=20, help="Top-k sampling parameter.")
    parser.add_argument('--repetition_penalty', type=float, default=1.05,
                        help="Repetition penalty. If not set, defaults based on the model.")
    parser.add_argument('--max_tokens', type=int, default=20000,
                        help="Maximum number of tokens to generate. If not set, defaults based on the model and dataset.")

    # parser.add_argument('--max_search_limit', type=int, default=10, help="Maximum number of searches per question.")
    parser.add_argument('--top_k', type=int, default=5, help="Maximum number of search documents to return.")
    parser.add_argument('--keep_links', action='store_true', default=False,
                        help="Whether to keep links in fetched web content")
    parser.add_argument('--use_jina', action='store_true', help="Whether to use Jina API for document fetching.")
    parser.add_argument('--jina_api_key', type=str, default='None', help="Your Jina API Key to Fetch URL Content.")
    # parser.add_argument('--bing_subscription_key', type=str, required=True, help="Bing Search API subscription key.")
    # parser.add_argument('--bing_endpoint', type=str, default="https://api.bing.microsoft.com/v7.0/search", help="Bing Search API endpoint.")
    parser.add_argument('--eval', action='store_true', help="Whether to run evaluation after generation.")
    parser.add_argument('--seed', type=int, default=None,
                        help="Random seed for generation. If not set, will use current timestamp as seed.")
    parser.add_argument('--api_base_url', type=str, required=True, help="Base URL for the API endpoint")
    parser.add_argument('--aux_api_base_url', type=str, required=True,
                        help="Base URL for the auxiliary model API endpoint")
    parser.add_argument('--model_name', type=str, default="QwQ-32B", help="Name of the model to use")
    parser.add_argument('--aux_model_name', type=str, default="Qwen2.5-72B-Instruct",
                        help="Name of the auxiliary model to use")
    parser.add_argument('--concurrent_limit', type=int, default=32, help="Maximum number of concurrent API calls")
    parser.add_argument('--lora_name', type=str, default=None, help="Name of the LoRA adapter to load")
    parser.add_argument('--lora_path', type=str, default=None, help="Path to the LoRA weights")
    return parser.parse_args()


def extract_between(text, start_marker, end_marker):
    """Extracts text between two markers in a string."""
    try:
        pattern = re.escape(end_marker[::-1]) + r"(.*?)" + re.escape(start_marker[::-1])
        # Run pattern matching with timeout
        matches = re.findall(pattern, text[::-1], flags=re.DOTALL)
        if matches:
            return matches[0][::-1].strip()
        return None
    except Exception as e:
        print(f"---Error:---\n{str(e)}")
        print(f"-------------------")
        return None


def format_search_results(relevant_info: List[Dict]) -> str:
    """Format search results into a readable string"""
    formatted_documents = ""
    try:
        # 检查relevant_info是否为列表
        if not isinstance(relevant_info, list):
            print(f"Error: expected list but got {type(relevant_info)}")
            return f"Error formatting search results: unexpected type {type(relevant_info)}"
            
        for i, doc_info in enumerate(relevant_info):
            # 检查doc_info是否为字典
            if not isinstance(doc_info, dict):
                print(f"Warning: Expected dict for doc_info but got {type(doc_info)}: {doc_info}")
                continue
                
            # 安全地处理title字段
            if 'title' in doc_info and isinstance(doc_info['title'], str):
                doc_info['title'] = doc_info['title'].replace('<b>','').replace('</b>','')
            elif 'title' in doc_info:
                print(f"Warning: title is not a string: {type(doc_info['title'])}")
                
            # 安全地处理snippet字段
            if 'snippet' in doc_info and isinstance(doc_info['snippet'], str):
                doc_info['snippet'] = doc_info['snippet'].replace('<b>','').replace('</b>','')
            elif 'snippet' in doc_info:
                print(f"Warning: snippet is not a string: {type(doc_info['snippet'])}")
                
            formatted_documents += f"***Web Page {i + 1}:***\n"
            formatted_documents += json.dumps(doc_info, ensure_ascii=False, indent=2) + "\n"
    except Exception as e:
        print(f"Error in format_search_results: {e}")
        return f"Error formatting search results: {str(e)}"
    
    return formatted_documents


def extract_markdown_content(text):
    """Extract content between ```markdown and ``` tags."""
    pattern = r"```markdown\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    return text


def judge_zh(input_str: str):
    assert isinstance(input_str, str), input_str
    if len(input_str) == 0:
        return False
    detect_result = langid.classify(input_str)
    if detect_result[0] == 'zh':
        return True
    else:
        return False


async def generate_response(
        client: AsyncOpenAI,
        prompt: str,
        semaphore: asyncio.Semaphore,
        generate_mode: str = "chat",
        temperature: float = 0.0,
        top_p: float = 1.0,
        max_tokens: int = 20000,
        repetition_penalty: float = 1.0,
        top_k: int = 1,
        min_p: float = 0.0,
        model_name: str = "QwQ-32B",
        stop: List[str] = [END_SEARCH_QUERY],
        retry_limit: int = 3,
) -> Tuple[str, str]:
    """Generate a single response with retry logic"""
    for attempt in range(retry_limit):
        try:
            async with semaphore:
                if generate_mode == "chat":
                    messages = [{"role": "user", "content": prompt}]
                    if 'qwq' in model_name.lower():
                        formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False,
                                                                         add_generation_prompt=True)
                    else:
                        formatted_prompt = aux_tokenizer.apply_chat_template(messages, tokenize=False,
                                                                             add_generation_prompt=True)
                else:
                    formatted_prompt = prompt

                response = await client.completions.create(
                    model=model_name,
                    prompt=formatted_prompt,
                    temperature=temperature,
                    top_p=top_p,
                    max_tokens=max_tokens,
                    stop=stop,
                    extra_body={
                        'top_k': top_k,
                        'include_stop_str_in_output': True,
                        'repetition_penalty': repetition_penalty,
                    },
                    timeout=600,
                )
                return formatted_prompt, response.choices[0].text
        except Exception as e:
            print(f"Generate Response Error occurred: {e}, Starting retry attempt {attempt + 1}")
            print(prompt)
            if attempt == retry_limit - 1:
                print(f"Failed after {retry_limit} attempts: {e}")
                return formatted_prompt, ""
            await asyncio.sleep(1 * (attempt + 1))
    return formatted_prompt, ""


async def generate_deep_web_explorer(
        client: AsyncOpenAI,
        aux_client: AsyncOpenAI,
        question: str,
        search_query: str,
        document: str,
        search_intent: str,
        args: argparse.Namespace,
        search_cache: Dict,
        url_cache: Dict,
        semaphore: asyncio.Semaphore,
) -> Tuple[str, List[Dict], str]:
    """
    Generate deep web exploration with multiple search and click operations
    Returns the output, list of interaction records, and initial prompt
    """
    prompt = get_deep_web_explorer_instruction(search_query=search_query, search_intent=search_intent,
                                               search_result=document)
    original_prompt = ""
    output = ""
    total_tokens = len(prompt.split())  # Track total tokens including prompt
    MAX_TOKENS = 10000  # Reduced from 20000
    MAX_INTERACTIONS = 5  # Reduced from 10
    clicked_urls = set()  # Track clicked URLs
    executed_search_queries = set()  # Track executed search queries
    total_interactions = 0
    finished = False
    first_generation = True

    while True:
        # Generate next response
        formatted_prompt, response = await generate_response(
            client=client,
            prompt=prompt,
            semaphore=semaphore,
            generate_mode="chat" if first_generation else "completion",
            temperature=args.temperature,
            top_p=args.top_p,
            max_tokens=args.max_tokens,
            repetition_penalty=args.repetition_penalty,
            top_k=args.top_k_sampling,
            min_p=args.min_p,
            model_name=args.model_name,
            stop=[END_SEARCH_QUERY, END_CLICK_LINK],
        )

        if first_generation:
            original_prompt = formatted_prompt
            prompt = formatted_prompt

        output += response.replace('</think>\n', '')
        total_tokens = len(prompt.split()) + len(response.split())
        first_generation = False

        if total_tokens >= MAX_TOKENS or total_interactions >= MAX_INTERACTIONS:
            break

        # Check for search query
        if response.rstrip().endswith(END_SEARCH_QUERY):
            new_query = extract_between(response, BEGIN_SEARCH_QUERY, END_SEARCH_QUERY)
            if new_query:
                total_interactions += 1

                if new_query in executed_search_queries:
                    # If search query was already executed, append message and continue
                    search_result = f"\n{BEGIN_SEARCH_RESULT}\nYou have already searched for this query. Please use the previously found information.\n{END_SEARCH_RESULT}\n"
                    output += search_result
                    prompt += output
                    total_tokens += len(search_result.split())
                    continue

                executed_search_queries.add(new_query)  # Add query to executed set

                # Execute search
                if new_query in search_cache:
                    results = search_cache[new_query]
                else:
                    try:
                        results = await brave_search_async(new_query, args.brave_api_key, country='us', language='en', timeout=20)
                        # 检查结果是否有效
                        if results and isinstance(results, dict):
                            search_cache[new_query] = results
                        else:
                            print(f"Warning: Invalid results from Brave search API: {type(results)}")
                            results = {"web": {"results": []}}  # 提供一个空结果结构
                    except Exception as e:
                        print(f"Error during search query '{new_query}': {e}")
                        results = {"web": {"results": []}}  # 错误时提供空结果
                print('- Searched for:', new_query)

                try:
                    formatted_documents = format_search_results(BraveSearchClient.extract_search_results(results))
                except Exception as e:
                    print(f"Error formatting search results: {e}")
                    formatted_documents = "Error retrieving search results. Please try a different query."

                # Append search results
                search_result = f"\n{BEGIN_SEARCH_RESULT}\n{formatted_documents}\n{END_SEARCH_RESULT}\n"
                output += search_result
                prompt += output
                total_tokens += len(search_result.split())

        # Check for click link
        elif response.rstrip().endswith(END_CLICK_LINK):
            url = extract_between(response, BEGIN_CLICK_LINK, END_CLICK_LINK)
            # click_intent = extract_between(response, BEGIN_CLICK_INTENT, END_CLICK_INTENT)
            _, click_intent = await generate_response(
                client=aux_client,
                model_name=args.aux_model_name,
                prompt=get_click_intent_instruction(question, output),
                semaphore=semaphore,
                max_tokens=args.max_tokens // 2,
            )

            if url and click_intent:
                total_interactions += 1
                if url in clicked_urls:
                    # If URL was already clicked, append message
                    click_result = f"\n{BEGIN_CLICK_RESULT}\nYou have already clicked this URL.\n{END_CLICK_RESULT}\nOK, let me use the previously found information."
                    output += click_result
                    prompt += output
                    total_tokens += len(click_result.split())
                    continue

                clicked_urls.add(url)  # Add URL to clicked set
                print(f"- Clicking on URL: {url} with intent: {click_intent}")
                # Fetch and process page content
                if url not in url_cache:
                    try:
                        content = await fetch_page_content_async(
                            [url],
                            use_jina=args.use_jina,
                            jina_api_key=os.getenv('JINA_API_KEY'),
                            keep_links=args.keep_links
                        )
                        content = content[url]
                        # Only cache content if it doesn't contain error indicators
                        has_error = (any(
                            indicator.lower() in content.lower() for indicator in error_indicators) and len(
                            content.split()) < 64) or content == ''
                        if not has_error:
                            url_cache[url] = content
                    except Exception as e:
                        print(f"Error fetching URL {url}: {e}")
                        content = ""
                else:
                    content = url_cache[url]

                # Check if content has error indicators
                has_error = any(indicator.lower() in content.lower() for indicator in error_indicators) or content == ''

                if has_error:
                    # If content has error, use it directly as summary
                    summary = "Unable to fetch the page content. You can try other links."
                else:
                    # Use web page reader to summarize content
                    reader_prompt = get_click_web_page_reader_instruction(click_intent, content[:20000])
                    _, summary = await generate_response(
                        client=aux_client,
                        prompt=reader_prompt,
                        semaphore=semaphore,
                        max_tokens=8000,
                        model_name=args.aux_model_name,
                    )

                # Append click results
                click_result = f"\n{BEGIN_CLICK_RESULT}\n{summary}\n{END_CLICK_RESULT}\n"
                output += click_result
                prompt += output
                total_tokens += len(click_result.split())

        else:
            finished = True
            break

    # Add max limit message if needed
    if not finished and (total_tokens >= MAX_TOKENS or total_interactions >= MAX_INTERACTIONS):
        output += f"\n{BEGIN_CLICK_RESULT}\nYou have reached the limit for clicking links.\n{END_CLICK_RESULT}\n\nOK, I will now provide the final information based on my collected information.\n\n**Final Information:**"
        prompt += output
        _, final_response = await generate_response(
            client=client,
            prompt=prompt,
            semaphore=semaphore,
            generate_mode="completion",
            temperature=args.temperature,
            top_p=args.top_p,
            max_tokens=512,
            repetition_penalty=1.2,
            top_k=args.top_k_sampling,
            min_p=args.min_p,
            model_name=args.model_name,
        )
        output += final_response

    return output, original_prompt


async def process_single_sequence(
        seq: Dict,
        client: AsyncOpenAI,
        aux_client: AsyncOpenAI,
        semaphore: asyncio.Semaphore,
        args: argparse.Namespace,
        search_cache: Dict,
        url_cache: Dict,
        batch_output_records: List[Dict],
) -> Dict:
    """Process a single sequence through its entire reasoning chain with MAX_TOKENS limit"""

    # Generate search plan first
    print(f"Generating search plan...")
    question = seq['item']['Question']
    _, search_plan = await generate_response(
        client=aux_client,
        model_name=args.aux_model_name,
        prompt=get_search_plan_instruction(question),
        semaphore=semaphore,
        max_tokens=1024,  # Reduced from args.max_tokens // 2
    )

    print(f"---Search plan:---\n{search_plan}")

    # Generate the full instruction with the plan
    user_prompt = get_report_webthinker_instruction(question, search_plan)
    seq['prompt'] = user_prompt

    # Initialize token counter with prompt tokens
    MAX_TOKENS = 16000  # Reduced from 50000
    total_tokens = len(seq['prompt'].split())

    # Initialize web explorer interactions list and article-related variables
    seq['web_explorer'] = []
    article = ""
    summarized_article = ""
    document_memory = []  # Store all retrieved web page content

    # Initialize BM25 for document retrieval
    tokenized_docs = []
    bm25 = None

    # First response uses chat completion
    formatted_prompt, response = await generate_response(
        client=client,
        model_name=args.model_name,
        prompt=seq['prompt'],
        semaphore=semaphore,
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=6000,  # Reduced from args.max_tokens
        repetition_penalty=args.repetition_penalty,
        top_k=args.top_k_sampling,
        min_p=args.min_p,
        stop=[END_SEARCH_QUERY, END_WRITE_SECTION, END_EDIT_ARTICLE, BEGIN_CHECK_ARTICLE],
        generate_mode="chat"  # First generation in chat mode
    )

    # Update token count and sequence fields
    tokens_this_response = len(response.split())
    total_tokens += tokens_this_response

    seq['output'] += response.replace('</think>\n', '')
    seq['history'].append(response.replace('</think>\n', ''))
    seq['prompt'] = formatted_prompt + response.replace('</think>\n', '')
    seq['original_prompt'] = formatted_prompt

    while not seq['finished']:
        # Handle different response endings
        if response.rstrip().endswith(END_WRITE_SECTION):
            # Extract section information
            section_content = extract_between(response, BEGIN_WRITE_SECTION, END_WRITE_SECTION)
            print(f"---Writing section:---")
            if section_content:
                section_parts = section_content.strip('\n').strip().split('\n', 1)
                if len(section_parts) == 2:
                    section_name, task = section_parts
                    print(f"---Section name:---\n{section_name}")
                    print(f"---Task:---\n{task}")

                    # Prepare relevant documents using BM25
                    if not bm25 and document_memory:
                        tokenized_docs = [word_tokenize(doc.lower()) for doc in document_memory]
                        bm25 = BM25Okapi(tokenized_docs)

                    if bm25:
                        query = f"{section_name} {task}"
                        tokenized_query = word_tokenize(query.lower())
                        doc_scores = bm25.get_scores(tokenized_query)
                        top_indices = np.argsort(doc_scores)[-3:][::-1]  # Get top 3 relevant documents
                        relevant_documents = ""
                        for i, idx in enumerate(top_indices, 1):
                            relevant_documents += f"Document {i}:\n{document_memory[idx]}\n\n"
                    else:
                        relevant_documents = ""

                    # Generate section content
                    section_prompt = get_write_section_instruction(
                        question=question,
                        previous_thoughts=seq['output'],
                        relevant_documents=relevant_documents,
                        section_name=section_name,
                        task=task,
                        current_article=summarized_article
                    )

                    _, section_content = await generate_response(
                        client=aux_client,
                        prompt=section_prompt,
                        semaphore=semaphore,
                        model_name=args.aux_model_name,
                        max_tokens=args.max_tokens // 4,
                    )

                    # Update article
                    section_content = \
                    section_content.replace('## Section Name: ', '## ').split('### Conclusion')[0].split(
                        '### Conclusion')[0].strip('\n').strip()
                    section_content = re.sub(r'## Section \d+:', '##', section_content)
                    article += f"\n{section_content}\n\n"

                    """# Generate section summary
                    summary_prompt = get_section_summary_instruction(section_content)
                    _, section_summary = await generate_response(
                        client=aux_client,
                        prompt=summary_prompt,
                        semaphore=semaphore,
                        model_name=args.aux_model_name,
                        max_tokens=args.max_tokens // 2,
                    )

                    summarized_article += f"\n{section_summary}\n\n"""

                    # Extract outline by finding all headers
                    headers = re.findall(r'^#{1,4}\s+.*$', article, re.MULTILINE)
                    summarized_article = '\n'.join(headers) + '\n'

                    print(f"---Article:---\n{article}\n")
                    print(f"---Summarized article:---\n{summarized_article}\n")

        elif response.rstrip().endswith(END_EDIT_ARTICLE):
            # Handle edit article operation
            edit_instruction = extract_between(response, BEGIN_EDIT_ARTICLE, END_EDIT_ARTICLE)
            print(f"---Editing:---\n{edit_instruction}\n")
            if edit_instruction and article:
                edit_prompt = get_edit_article_instruction(edit_instruction, article)
                _, edit_response = await generate_response(
                    client=aux_client,
                    prompt=edit_prompt,
                    semaphore=semaphore,
                    model_name=args.aux_model_name,
                    max_tokens=args.max_tokens // 3,
                )
                # article = extract_modified_content(article, edit_response)
                article = extract_markdown_content(edit_response)
                print(f"---Article:---\n{article}\n")

        elif response.rstrip().endswith(BEGIN_CHECK_ARTICLE):
            # Handle check article operation
            print(f"Checking article...")
            # First, fold any existing check article content
            if "BEGIN_CHECK_ARTICLE" in seq['prompt'] and "END_CHECK_ARTICLE" in seq['prompt']:
                old_check = extract_between(seq['prompt'], BEGIN_CHECK_ARTICLE, END_CHECK_ARTICLE)
                if old_check and old_check != "folded":
                    print(f"Folded previous checked article")
                    seq['prompt'] = seq['prompt'].replace(
                        f"{BEGIN_CHECK_ARTICLE}{old_check}{END_CHECK_ARTICLE}",
                        f"{BEGIN_CHECK_ARTICLE}folded{END_CHECK_ARTICLE}"
                    )

            # Check and add title if needed
            if not article.strip('\n').strip().startswith("# "):
                title_prompt = get_title_instruction(question, article)
                _, title = await generate_response(
                    client=aux_client,
                    prompt=title_prompt,
                    semaphore=semaphore,
                    model_name=args.aux_model_name,
                    max_tokens=args.max_tokens // 4,
                )
                title = title.replace('\n', '').strip('"').strip("'").strip()
                article = f"# {title}\n\n{article}"
                summarized_article = f"# {title}\n\n{summarized_article}"

            # Append summarized article to prompt
            append_text = f"{summarized_article}{END_CHECK_ARTICLE}\n\n"
            seq['prompt'] += append_text
            seq['output'] += append_text
            seq['history'].append(append_text)
            total_tokens += len(append_text.split())

            print(f"---Summarized article:---\n{summarized_article}\n")
            # print(f"---Model prompt:---\n{seq['prompt']}\n")

        elif response.rstrip().endswith(END_SEARCH_QUERY):
            # Handle search query operation (existing logic)
            search_query = extract_between(response, BEGIN_SEARCH_QUERY, END_SEARCH_QUERY)

            if search_query is None or len(search_query) <= 5:  # Too short, invalid query
                continue

            if search_query in seq['executed_search_queries']:
                # If search query was already executed, append message and continue
                append_text = f"\n\n{BEGIN_SEARCH_RESULT}You have already searched for this query.{END_SEARCH_RESULT}\n\nOK, let me use the previously found information."
                seq['prompt'] += append_text
                seq['output'] += append_text
                seq['history'].append(append_text)
                seq['search_count'] += 1
                total_tokens += len(append_text.split())
                # continue

            _, search_intent = await generate_response(
                client=aux_client,
                model_name=args.aux_model_name,
                prompt=get_search_intent_instruction(question, seq['output']),
                semaphore=semaphore,
                max_tokens=args.max_tokens // 2,
            )

            # Execute search and subsequent operations (same as original logic)
            if search_query in search_cache:
                results = search_cache[search_query]
            else:
                try:
                    results = await brave_search_async(search_query, api_key=os.getenv('BRAVE_API_KEY'), country='us', language='en', timeout=20)
                    # 检查结果是否有效
                    if results and isinstance(results, dict):
                        search_cache[search_query] = results
                    else:
                        print(f"Warning: Invalid results from Brave search API: {type(results)}")
                        results = {"web": {"results": []}}  # 提供一个空结果结构
                except Exception as e:
                    print(f"Error during search query '{search_query}': {e}")
                    results = {"web": {"results": []}}  # 错误时提供空结果
            print(f'---Searched for:---\n{search_query}\n')

            try:
                relevant_info = BraveSearchClient.extract_search_results(results)
                if not isinstance(relevant_info, list):
                    print(f"Warning: extract_search_results returned non-list: {type(relevant_info)}")
                    relevant_info = []  # 确保是列表类型
            except Exception as e:
                print(f"Error extracting search results: {e}")
                relevant_info = []  # 出错时提供空列表

            # Process documents
            urls_to_fetch = []
            for doc_info in relevant_info:
                url = doc_info['url']
                if url not in url_cache:
                    urls_to_fetch.append(url)

            if urls_to_fetch:
                try:
                    contents = await fetch_page_content_async(
                        urls_to_fetch,
                        use_jina=args.use_jina,
                        jina_api_key=os.getenv('JINA_API_KEY'),
                        keep_links=args.keep_links
                    )
                    for url, content in contents.items():
                        # Only cache content if it doesn't contain error indicators
                        has_error = (any(
                            indicator.lower() in content.lower() for indicator in error_indicators) and len(
                            content.split()) < 64) or len(content) < 50 or len(content.split()) < 20
                        if not has_error:
                            url_cache[url] = content
                        # else:
                        #     print(f'---Fetching Error\n{content}')
                except Exception as e:
                    print(f"Error fetching URLs: {e}")

            # Get web page information for each result
            read_web_page = False
            for idx, doc_info in enumerate(relevant_info):
                url = doc_info['url']
                if url not in url_cache:
                    raw_content = ""
                else:
                    raw_content = url_cache[url]
                    if idx < 5:
                        if read_web_page:
                            context_chars = 6000  # Reduced from 10000
                        else:
                            context_chars = 4000
                    else:
                        context_chars = 2000
                    is_success, raw_content = extract_snippet_with_context(raw_content, doc_info['snippet'],
                                                                           context_chars=context_chars)

                # Check if content has error indicators
                has_error = any(
                    indicator.lower() in raw_content.lower() for indicator in error_indicators) or raw_content == ""

                if has_error:
                    # If content has error, use it directly as summary
                    doc_info['page_info'] = "Can not fetch the page content."
                else:
                    if idx < 5 and read_web_page:
                        # Use detailed web page reader to process content
                        reader_prompt = get_detailed_web_page_reader_instruction(search_query, search_intent,
                                                                                 raw_content)
                        _, page_info = await generate_response(
                            client=aux_client,
                            prompt=reader_prompt,
                            semaphore=semaphore,
                            max_tokens=8000,
                            model_name=args.aux_model_name,
                        )
                        doc_info['page_info'] = page_info
                    else:
                        doc_info['page_info'] = raw_content

            formatted_documents = format_search_results(relevant_info)

            # Generate deep web exploration with interactions
            analysis, explorer_prompt = await generate_deep_web_explorer(
                client=client,
                aux_client=aux_client,
                question=question,
                search_query=search_query,
                search_intent=search_intent,
                document=formatted_documents,
                args=args,
                search_cache=search_cache,
                url_cache=url_cache,
                semaphore=semaphore,
            )

            extracted_info = extract_answer_fn(analysis, mode='research')

            # Store web explorer input/output with all interactions
            seq['web_explorer'].append({
                "search_query": search_query,
                "Input": explorer_prompt,
                "Output": analysis,
                "Extracted_info": extracted_info
            })

            # Update sequence with search results
            append_text = f"\n\n{BEGIN_SEARCH_RESULT}{extracted_info}{END_SEARCH_RESULT}\n\n"
            seq['prompt'] += append_text
            seq['output'] += append_text
            seq['history'].append(append_text)

            seq['search_count'] += 1
            seq['executed_search_queries'].add(search_query)
            total_tokens += len(append_text.split())

            # Add retrieved content to document memory
            for doc_info in relevant_info:
                if 'page_info' in doc_info and doc_info['page_info'] != "Can not fetch the page content.":
                    document_memory.append(doc_info['page_info'])

            print(f"---Returned search results:---\n{extracted_info}\n")

        else:
            # If none of the above ending markers, EOS returned, ending generation
            print("---Returned EOS, generation finished.---")
            seq['finished'] = True
            break

        if total_tokens >= MAX_TOKENS:
            seq['finished'] = True
            break

        else:
            print('Calling generate_response...')
            # Subsequent responses use completion mode
            _, response = await generate_response(
                client=client,
                model_name=args.model_name,
                prompt=seq['prompt'],
                semaphore=semaphore,
                temperature=args.temperature,
                top_p=args.top_p,
                max_tokens=args.max_tokens,
                repetition_penalty=args.repetition_penalty,
                top_k=args.top_k_sampling,
                min_p=args.min_p,
                stop=[END_SEARCH_QUERY, END_WRITE_SECTION, END_EDIT_ARTICLE, BEGIN_CHECK_ARTICLE],
                generate_mode="completion"
            )

            # Update token count and sequence fields
            total_tokens += len(response.split())

            seq['output'] += response.replace('</think>\n', '')
            seq['history'].append(response.replace('</think>\n', ''))
            seq['prompt'] += response.replace('</think>\n', '')

    # Store final article in sequence
    seq['article'] = article
    seq['summarized_article'] = summarized_article
    return seq


async def load_lora_adapter(api_base_url: str, lora_name: str, lora_path: str) -> bool:
    """Load a LoRA adapter with the specified name and path"""
    try:
        lora_load_url = f"{api_base_url}/load_lora_adapter"
        lora_payload = {
            "lora_name": lora_name,
            "lora_path": lora_path
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(lora_load_url, json=lora_payload) as response:
                return response.status == 200
    except Exception as e:
        print(f"Error loading LoRA adapter: {e}")
        return False


async def unload_lora_adapter(api_base_url: str, lora_name: str) -> bool:
    """Unload a LoRA adapter with the specified name"""
    try:
        unload_url = f"{api_base_url}/unload_lora_adapter"
        unload_payload = {"lora_name": lora_name}
        async with aiohttp.ClientSession() as session:
            async with session.post(unload_url, json=unload_payload) as response:
                return response.status == 200
    except Exception as e:
        print(f"Error unloading LoRA adapter: {e}")
        return False


async def main_async():
    args = parse_args()

    # Set random seed
    if args.seed is None:
        args.seed = int(time.time())
    random.seed(args.seed)
    np.random.seed(args.seed)

    if args.jina_api_key == 'None':
        jina_api_key = None

    # Modified data loading section
    if args.single_question:
        # Create a single item in the same format as dataset items
        filtered_data = [{
            'Question': args.single_question,
        }]
        args.dataset_name = 'custom'  # Set dataset name to custom for single questions
    else:
        # Original dataset loading logic
        if args.dataset_name == 'livecode':
            data_path = f'./data/LiveCodeBench/{args.split}.json'
        elif args.dataset_name == 'supergpqa':
            data_path = f'./data/SuperGPQA/{args.split}.json'
        elif args.dataset_name == 'webwalker':
            data_path = f'./data/WebWalkerQA/{args.split}.json'
        elif args.dataset_name == 'openthoughts':
            data_path = f'./data/OpenThoughts/{args.split}.json'
        elif args.dataset_name == 'glaive':
            data_path = f'./data/Glaive/{args.split}.json'
        elif args.dataset_name in ['math500', 'gpqa', 'aime', 'amc', 'gaia', 'hle', 'limo']:
            data_path = f'./data/{args.dataset_name.upper()}/{args.split}.json'
        elif args.dataset_name == 'strongreject':
            data_path = f'./data/strongreject/{args.split}.json'
        else:
            data_path = f'./data/QA_Datasets/{args.dataset_name}.json'

        print('-----------------------')
        print(f'Using {args.dataset_name} {args.split} set.')
        print('-----------------------')

        with open(data_path, 'r', encoding='utf-8') as json_file:
            filtered_data = json.load(json_file)

        # Process special fields for strongreject dataset
        if args.dataset_name == 'strongreject':
            # Use forbidden_prompt field as Question field
            for item in filtered_data:
                if 'forbidden_prompt' in item and 'Question' not in item:
                    item['Question'] = item['forbidden_prompt']
            print('Note: The forbidden_prompt field in strongreject dataset has been processed as Question')

        if args.subset_num != -1:
            indices = list(range(len(filtered_data)))
            selected_indices = random.sample(indices, min(args.subset_num, len(indices)))
            filtered_data = [filtered_data[i] for i in selected_indices]

    # ---------------------- Caching Mechanism ----------------------
    cache_dir = './cache'
    search_cache_path = os.path.join(cache_dir, 'search_cache.json')
    if args.keep_links:
        url_cache_path = os.path.join(cache_dir, 'url_cache_with_links.json')
    else:
        url_cache_path = os.path.join(cache_dir, 'url_cache.json')

    os.makedirs(cache_dir, exist_ok=True)

    # Load existing caches
    search_cache = json.load(open(search_cache_path)) if os.path.exists(search_cache_path) else {}
    url_cache = json.load(open(url_cache_path)) if os.path.exists(url_cache_path) else {}

    def save_caches():
        with open(search_cache_path, 'w', encoding='utf-8') as f:
            json.dump(search_cache, f, ensure_ascii=False, indent=2)
        with open(url_cache_path, 'w', encoding='utf-8') as f:
            json.dump(url_cache, f, ensure_ascii=False, indent=2)

    # Define output directory and markdown directory
    if 'qwq' in args.model_name.lower():
        model_short_name = 'qwq'
    elif 'deepseek' in args.model_name.lower():
        if 'llama-8b' in args.model_name.lower():
            model_short_name = 'dpsk-llama-8b'
        elif 'llama-70b' in args.model_name.lower():
            model_short_name = 'dpsk-llama-70b'
        elif 'qwen-1.5b' in args.model_name.lower():
            model_short_name = 'dpsk-qwen-1.5b'
        elif 'qwen-7b' in args.model_name.lower():
            model_short_name = 'dpsk-qwen-7b'
        elif 'qwen-32b' in args.model_name.lower():
            model_short_name = 'dpsk-qwen-32b'
    elif 'sky-t1' in args.model_name.lower():
        model_short_name = 'sky-t1'
    else:
        model_short_name = args.model_name.split('/')[-1].lower().replace('-instruct', '')

    # Use special output directory for strongreject dataset
    if args.dataset_name == 'strongreject':
        # Add additional information for strongreject dataset
        output_dir = f'./outputs/strongreject.{model_short_name}.webthinker'
    else:
        output_dir = f'./outputs/{args.dataset_name}.{model_short_name}.webthinker'
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the OpenAI client
    client = AsyncOpenAI(
        api_key="token-abc123",
        base_url=args.api_base_url,
    )
    # Initialize auxiliary client
    aux_client = AsyncOpenAI(
        api_key="token-abc123",
        base_url=args.aux_api_base_url,
    )

    # Prepare sequences
    active_sequences = []
    for item in filtered_data:
        active_sequences.append({
            'item': item,
            'prompt': '',  # Will be set in process_single_sequence
            'output': '',
            'finished': False,
            'history': [],
            'search_count': 0,
            'executed_search_queries': set(),
        })

    # Initialize batch output records
    batch_output_records = []
    start_time = time.time()

    # Create semaphore for concurrent API calls
    semaphore = asyncio.Semaphore(args.concurrent_limit)

    # Load LoRA adapter if specified
    if args.lora_name and args.lora_path:
        print(f"Loading LoRA adapter '{args.lora_name}' from {args.lora_path}")
        success = await load_lora_adapter(args.api_base_url, args.lora_name, args.lora_path)
        if not success:
            print("Failed to load LoRA adapter")
            return
        else:
            print("LoRA adapter loaded successfully")

    try:
        # Process all sequences concurrently
        tasks = [
            process_single_sequence(
                seq=seq,
                client=client,
                aux_client=aux_client,
                semaphore=semaphore,
                args=args,
                search_cache=search_cache,
                url_cache=url_cache,
                batch_output_records=batch_output_records
            )
            for seq in active_sequences
        ]

        # Run all sequences concurrently with progress bar
        with tqdm(total=len(tasks)) as pbar:
            async def track_progress(task):
                result = await task
                pbar.update(1)
                return result

            tracked_tasks = [track_progress(task) for task in tasks]
            completed_sequences = await asyncio.gather(*tracked_tasks)

        t = time.localtime()
        random_num = str(random.randint(0, 99)).zfill(2)
        markdown_dir = os.path.join(output_dir,
                                    f'markdown.{args.split}.{t.tm_mon}.{t.tm_mday},{t.tm_hour}:{t.tm_min}.{random_num}')  # Add markdown directory
        os.makedirs(markdown_dir, exist_ok=True)  # Create markdown directory

        # Save markdown files for each completed sequence
        for i, seq in enumerate(completed_sequences):
            if seq['article'].strip():  # Only save if article is not empty
                markdown_filename = f'article_{i + 1}.md'

                # Add question as context at the top of the file
                question_context = f"Question: {seq['item']['Question']}\n\n"

                # Add additional information for strongreject dataset
                if args.dataset_name == 'strongreject' and 'category' in seq['item']:
                    question_context = f"Category: {seq['item']['category']}\n" + question_context

                with open(os.path.join(markdown_dir, markdown_filename), 'w', encoding='utf-8') as f:
                    f.write(question_context + seq['article'])

    finally:
        # Unload LoRA adapter if it was loaded
        if args.lora_name:
            print(f"Unloading LoRA adapter '{args.lora_name}'")
            await unload_lora_adapter(args.api_base_url, args.lora_name)
            print("LoRA adapter unloaded successfully")

    total_time = time.time() - start_time

    # Prepare output list and save results
    output_list = [seq['output'] for seq in completed_sequences]

    if args.eval:
        if args.dataset_name == 'strongreject':
            # Add special evaluation for strongreject dataset
            category_stats = {}

            # Count the number of items in each category
            for item in filtered_data:
                if 'category' in item:
                    cat = item.get('category', 'unknown')
                    if cat not in category_stats:
                        category_stats[cat] = {
                            'total': 0,
                            'articles': 0
                        }
                    category_stats[cat]['total'] += 1

            # Count the number of generated articles
            for i, seq in enumerate(completed_sequences):
                if seq['article'].strip() and 'category' in filtered_data[i]:
                    cat = filtered_data[i].get('category', 'unknown')
                    category_stats[cat]['articles'] += 1

            # Generate statistics report
            stats_report = "# StrongReject Dataset Statistics\n\n"
            stats_report += "| Category | Total | Articles Generated | Rate |\n"
            stats_report += "|----------|-------|-------------------|------|\n"

            total_all = 0
            articles_all = 0

            for cat, stats in category_stats.items():
                total = stats['total']
                articles = stats['articles']
                rate = f"{articles / total:.2%}" if total > 0 else "N/A"
                stats_report += f"| {cat} | {total} | {articles} | {rate} |\n"
                total_all += total
                articles_all += articles

            # Add totals
            total_rate = f"{articles_all / total_all:.2%}" if total_all > 0 else "N/A"
            stats_report += f"| **Total** | {total_all} | {articles_all} | {total_rate} |\n"

            # Save statistics report
            with open(os.path.join(output_dir, f'strongreject_stats_{args.split}.md'), 'w', encoding='utf-8') as f:
                f.write(stats_report)

            print(f"\n===== StrongReject Statistics =====")
            print(f"Total samples: {total_all}")
            print(f"Articles generated: {articles_all}")
            print(f"Generation rate: {total_rate}")

        # Original evaluation code
        run_evaluation(filtered_data, [seq['prompt'] for seq in completed_sequences], output_list, args.dataset_name,
                       output_dir, total_time, args.split)
    else:
        result_json_name = f'{args.split}.{t.tm_mon}.{t.tm_mday},{t.tm_hour}:{t.tm_min}.{random_num}.json'
        if 'DPO' in args.model_name:
            result_json_name = f'{args.split}.{t.tm_mon}.{t.tm_mday},{t.tm_hour}:{t.tm_min}.{random_num}.dpo.json'
        elif 'SFT' in args.model_name:
            result_json_name = f'{args.split}.{t.tm_mon}.{t.tm_mday},{t.tm_hour}:{t.tm_min}.{random_num}.sft.json'

        for item, seq in zip(filtered_data, completed_sequences):
            item['prompt'] = seq['original_prompt']
            item['Output'] = seq['output']
            item['WebExplorer'] = seq['web_explorer']  # Updated field name
            # For strongreject dataset, preserve original fields such as category for analysis
            if args.dataset_name == 'strongreject' and 'category' in item:
                # Keep original fields unchanged
                pass

        with open(os.path.join(output_dir, result_json_name), mode='w', encoding='utf-8') as json_file:
            json.dump(filtered_data, json_file, indent=4, ensure_ascii=False)

    # Save caches
    save_caches()
    print("Process completed.")


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()