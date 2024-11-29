import asyncio
from ollama import ChatResponse
import ollama


def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers

    Args:
      a (int): The first number
      b (int): The second number

    Returns:
      int: The sum of the two numbers
    """
    return a + b


def subtract_two_numbers(a: int, b: int) -> int:
    """
    Subtract two numbers

    Args:
      a (int): The first integer number
      b (int): The second integer number

    Returns:
      int: The difference of the two integer numbers
    """
    return a - b


async def main():
    client = ollama.AsyncClient()

    available_functions = {
        "add_two_numbers": add_two_numbers,
        "subtract_two_numbers": subtract_two_numbers,
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
            tools=[add_two_numbers, subtract_two_numbers],  # Pass available tools.
        )

        # if response.message.tool_calls:
        #     # There may be multiple tool calls in the response
        #     for tool in response.message.tool_calls:
        #         # Ensure the function is available, and then call it
        #         if function_to_call := available_functions.get(tool.function.name):
        #             print("Calling function:", tool.function.name)
        #             print("Arguments:", tool.function.arguments)
        #             print(
        #                 "Function output:", function_to_call(**tool.function.arguments)
        #             )
        #         else:
        #             print("Function", tool.function.name, "not found")
        # else:
        #     print("Model Response:", response.message.content)


        # Check if the model made any tool calls (e.g., calling a math function)
        if response.message.tool_calls:
            # There may be multiple tool calls in the response
            for tool in response.message.tool_calls:
                # Ensure the function is available, and then call it
                if function_to_call := available_functions.get(tool.function.name):
                    print("Calling function:", tool.function.name)
                    print("Arguments before conversion:", tool.function.arguments)
        
                    # Convert arguments to integers before calling the function
                    try:
                        converted_arguments = {
                            key: int(value) for key, value in tool.function.arguments.items()
                        }
                        print("Arguments after conversion:", converted_arguments)
                        # Call the function with converted arguments
                        result = function_to_call(**converted_arguments)
                        print("Function output:", result)
                    except ValueError as e:
                        print("Error converting arguments to integers:", e)
                else:
                    print("Function", tool.function.name, "not found")



if __name__ == "__main__":
    try:
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\nGoodbye!")
