import memory.extract as extract
import memory.retrieve as retrieve

def db_memory(text):
    db_memory = extract.memory_set(text)
    return db_memory

def db_retrive(text):
    db_retrive = retrieve.retrive(text)
    return db_retrive