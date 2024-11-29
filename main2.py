
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


async def main():
    client = ollama.AsyncClient()

    available_functions = {
        "add_two_numbers": add_two_numbers,
        "subtract_two_numbers": subtract_two_numbers,
        "multiply_two_numbers": multiply_two_numbers,
        "divide_two_numbers": divide_two_numbers,
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

                    # Check if arguments are numeric before proceeding
                    try:
                        # Convert arguments to integers
                        converted_arguments = {
                            key: int(value) for key, value in tool.function.arguments.items()
                        }
                        print("Arguments after conversion:", converted_arguments)

                        # Call the function and print the result
                        result = function_to_call(**converted_arguments)
                        print("Function output:", result)
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
