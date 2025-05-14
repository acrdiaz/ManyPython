import time
from dr_service.prompt_service import PromptService

def main():
    """
    Main function to run the prompt service in the background
    until the user decides to exit.
    """
    print("Starting Prompt Service...")
    
    # Initialize and start the service
    service = PromptService()
    service.start()
    
    print("Prompt Service is running in the background.")
    print("You can add prompts to the queue and check their status.")
    
    try:
        while True:
            print("\n" + "="*50)
            print("Prompt Service Menu:")
            print("1. Add a new prompt")
            print("2. Check status of a prompt")
            print("3. Show queue size")
            print("4. Show all prompts")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == '1': # 1. Add a new prompt
                # Add a new prompt
                prompt_text = input("Enter your prompt: ")
                priority = input("Enter priority (optional, press Enter to skip): ")
                
                metadata = {}
                if priority.strip():
                    try:
                        metadata['priority'] = int(priority)
                    except ValueError:
                        metadata['priority'] = priority
                
                prompt_id = service.add_prompt(prompt_text, metadata)
                print(f"Prompt added with ID: {prompt_id}")
                
            elif choice == '2': # 2. Check status of a prompt
                # Check status of a prompt
                prompt_id = input("Enter prompt ID: ")
                status = service.get_status(prompt_id)
                
                if status:
                    print(f"Status: {status['status']}")
                    if status['status'] == 'completed':
                        print(f"Result: {status['result']}")
                    elif status['status'] == 'error':
                        print(f"Error: {status['result']}")
                else:
                    print(f"No prompt found with ID: {prompt_id}")
                    
            elif choice == '3': # 3. Show queue size
                # Show queue size
                queue_size = service.get_queue_size()
                print(f"Current queue size: {queue_size}")
                
            elif choice == '4': # 4. Show all prompts
                # Show all prompts
                statuses = service.get_all_statuses()
                if not statuses:
                    print("No prompts have been added yet.")
                else:
                    print(f"Total prompts: {len(statuses)}")
                    for prompt_id, status in statuses.items():
                        print(f"ID: {prompt_id}, Status: {status['status']}")
                        print(f"  Prompt: {status['prompt'][:50]}...")
                        if status['status'] == 'completed':
                            print(f"  Result: {status['result'][:50]}...")
                        print()
                
            elif choice == '5': # 5. Exit
                # Exit
                print("Stopping service and exiting...")
                break
                
            else:
                print("Invalid choice. Please try again.")
                
            # Small delay to prevent CPU hogging
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nInterrupted by user. Shutting down...")
    finally:
        # Make sure to stop the service before exiting
        service.stop()
        print("Service stopped. Goodbye!")

if __name__ == "__main__":
    main()