
import sys
import subprocess
import os

def run_script(script_name):
    """Runs a python script using the current python interpreter."""
    print(f"\n[Running {script_name}...]")
    try:
        subprocess.run([sys.executable, script_name], check=True)
        print(f"\n[Finished {script_name}]")
    except subprocess.CalledProcessError as e:
        print(f"\n[Error running {script_name}: {e}]")
    except FileNotFoundError:
        print(f"\n[Error: {script_name} not found]")
    
    input("\nPress Enter to continue...")

def main():
    while True:
        # Clear screen (optional, but nice)
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        print("==========================================")
        print("   PDF Splitter Tool for NotebookLM       ")
        print("==========================================")
        print("1. Generate Configuration")
        print("   (Scans 'Full_doc', creates 'split_config.py' with smart grouping)")
        print("")
        print("2. Split PDF")
        print("   (Reads 'split_config.py', output to 'Splitted_docs/<filename>')")
        print("")
        print("3. Check Word Counts (Optional)")
        print("   (Estimates word counts in 'Splitted_docs')")
        print("")
        print("4. Exit")
        print("==========================================")
        
        choice = input("Select an option (1-4): ").strip()
        
        if choice == '1':
            run_script(os.path.join("src", "generate_split_config.py"))
        elif choice == '2':
            run_script(os.path.join("src", "pdf_splitter.py"))
        elif choice == '3':
            run_script(os.path.join("src", "check_limits.py"))
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
