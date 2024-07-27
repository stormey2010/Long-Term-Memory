import memory.extract as extract
import memory.retrieve as retrieve
import memory.db_handler as db_handler
import memory.db as db
import threading

def run_example():
    # Example for memory setting
    text_to_set = "Remember my dog's birthday is July 25, 2024."
    set_memories = extract.memory_set(text_to_set)
    print(set_memories)

    # Example for memory retrieval
    text_to_retrive = "What is the birthday of my dog?"
    retrieved_data = retrieve.retrive(text_to_retrive)
    print(retrieved_data)

    # Start Memory UI
    memory_ui_thread = threading.Thread(target=lambda: db.app.run(debug=False, threaded=True), daemon=True)
    memory_ui_thread.start()

if __name__ == "__main__":
    run_example()
