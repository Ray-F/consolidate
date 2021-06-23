from colorama import Style, Fore


# TODO: Change the implementation of this to a Logger that is instantiated in the application file and passed
#  to all controllers (and then to Repo's, etc).

def log_init(service: str):
    print(f"{Fore.YELLOW}[Server]{Style.RESET_ALL} {service.capitalize()} initialised")
