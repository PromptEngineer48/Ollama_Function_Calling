
import asyncio
from ollama import ChatResponse
import ollama


def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers
    """
    return a + b


def subtract_two_numbers(a: int, b: int) -> int:
    """
    Subtract two numbers
    """
    return a - b


def multiply_two_numbers(a: int, b: int) -> int:
    """
    Multiply two numbers
    """
    return a * b


def divide_two_numbers(a: int, b: int) -> float:
    """
    Divide two numbers
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

import requests
from typing import Optional


def stock_price_fetcher(stock_name: str) -> Optional[float]:
    """
    Fetch the post-market price of a given stock from the Yahoo Finance API.

    Parameters:
    ----------
    stock_name : str
        The stock symbol (e.g., "AAPL" for Apple Inc.).

    Returns:
    -------
    Optional[float]
        The post-market price of the stock if available, or `None` if the 
        price is not found or an error occurs.

    Raises:
    ------
    Exception
        If the API request fails or returns an error.
    """
    url = "https://yahoo-finance166.p.rapidapi.com/api/stock/get-price"
    querystring = {"region": "US", "symbol": stock_name}
    headers = {
        "x-rapidapi-key": "b6dc2081ccmsh282bec1ffdb6254p10b966jsn0c43c4330ada",
        "x-rapidapi-host": "yahoo-finance166.p.rapidapi.com",
    }

    try:
        # Sending a GET request to the Yahoo Finance API
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an error if the request fails

        # Extracting the post-market price
        data = response.json()
        post_market_price = (
            data['quoteSummary']['result'][0]['price'].get('postMarketPrice', {}).get('raw')
        )

        if post_market_price is not None:
            return post_market_price
        else:
            print(f"Post-market price not available for {stock_name}.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error parsing API response: {e}")
        return None


import requests
from typing import Optional

def get_chapter_summary(chapter_number: int) -> Optional[str]:
    """
    Fetch the summary of a specific chapter from the Bhagavad Gita API.

    Parameters:
    ----------
    chapter_number : int
        The chapter number of the Bhagavad Gita to fetch the summary for (e.g., 1 for Chapter 1).

    Returns:
    -------
    Optional[str]
        The summary of the specified chapter as a string if successful, or `None` if an error occurs.

    Raises:
    ------
    Exception
        If the API request fails or the response does not contain the expected data.
    
    Notes:
    ------
    - The Bhagavad Gita has 18 chapters. Ensure the `chapter_number` is between 1 and 18.
    - This function uses the RapidAPI Bhagavad Gita API to retrieve the chapter summary.
    
    Example:
    -------
    >>> get_chapter_summary(1)
    'Chapter 1 is titled "Arjuna's Dilemma". It sets the stage...'
    """
    
    url = f"https://bhagavad-gita3.p.rapidapi.com/v2/chapters/{chapter_number}/"
    headers = {
        "x-rapidapi-key": "b6dc2081ccmsh282bec1ffdb6254p10b966jsn0c43c4330ada",
        "x-rapidapi-host": "bhagavad-gita3.p.rapidapi.com",
    }

    try:
        # Sending a GET request to the Bhagavad Gita API
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error if the request fails

        # Extracting the chapter summary from the response
        data = response.json()
        chapter_summary = data.get('chapter_summary')

        if chapter_summary:
            return chapter_summary
        else:
            print(f"Chapter summary not found for Chapter {chapter_number}.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error parsing the response: {e}")
        return None



async def main():
    client = ollama.AsyncClient()

    available_functions = {
        "add_two_numbers": add_two_numbers,
        "subtract_two_numbers": subtract_two_numbers,
        "multiply_two_numbers": multiply_two_numbers,
        "divide_two_numbers": divide_two_numbers,
        "stock_price_fetcher": stock_price_fetcher,
        "get_chapter_summary":get_chapter_summary,
    }

    print("Type 'exit' or 'quit' to stop the program.\n")

    while True:
        # Take the prompt from the user
        prompt = input("\nEnter your question: ")

        # Exit the loop if the user wants to quit
        if prompt.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Send the prompt to the LLM
        response: ChatResponse = await client.chat(
            "llama3.2",
            messages=[{"role": "user", "content": prompt}],
            tools=list(available_functions.values()),  # Pass all available tools.
        )

        if response.message.tool_calls:
            for tool in response.message.tool_calls:
                if function_to_call := available_functions.get(tool.function.name):
                    print("Calling function:", tool.function.name)
                    print("Arguments before conversion:", tool.function.arguments)
                    
                    if function_to_call == stock_price_fetcher:
                        result0= function_to_call(**tool.function.arguments)
                        print("Stock Price>", result0)
                        
                    elif function_to_call == get_chapter_summary:
                        results1 = function_to_call(**tool.function.arguments)
                        print("Bhagwad Gita> ", results1)
                    
                    else:
                        # Check if arguments are numeric before proceeding
                        try:
                            # Convert arguments to integers
                            converted_arguments = {
                                key: int(value) for key, value in tool.function.arguments.items()
                            }
                            print("Arguments after conversion:", converted_arguments)

                            # Call the function and print the result
                            result = function_to_call(**converted_arguments)
                            print("Function output>", result)
                        except ValueError:
                            print("Error: Non-numeric arguments passed to a numerical function.")
                            
                else:
                    print("Function", tool.function.name, "not found")
        else:
            # If no tool is called, simply print the model's response
            print("Model Response:", response.message.content)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
