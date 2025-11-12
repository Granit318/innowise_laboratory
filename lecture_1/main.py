from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform colored terminal output
init()

def print_colored_text():
    """
    Demonstration of using the colorama library for colored terminal output.

    This function prints multiple variations of 'Hello World!' text with different color schemes:
    - Red text on yellow background
    - Green text
    - Bright blue text
    - Magenta text on cyan background
    """
    print(f"{Fore.RED}{Back.YELLOW}Hello World!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Hello World in Green!{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{Style.BRIGHT}Hello World in Blue and Bright!{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{Back.CYAN}Hello World with Magenta text and Cyan background!{Style.RESET_ALL}")

if __name__ == "__main__":
    print_colored_text()