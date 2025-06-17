**This is the first of two posts on this topic.**

## 📖 In this post, we’ll explore processes, threads, and the GIL in Python, and look at how to bypass it using the `multiprocessing` module.



Let’s start with a few basics:



1) **Processes** are like independent running programs. Each has its own memory space and resources. They’re isolated from one another, so to exchange data between them, we need inter-process communication (IPC).



2) **Threads** are lighter units of execution within a single process. They share the same memory and address space, which makes data exchange easy—but also means you need synchronization to avoid conflicts.



---



### GIL (Global Interpreter Lock)



To understand how all this works in Python, you need to start with the GIL.



The GIL is a mechanism in the CPython interpreter that ensures only one thread runs Python code at a time. This simplifies the interpreter’s internals and spares developers from some synchronization headaches—like two threads modifying the same object at once with unpredictable results.



But keep in mind that the GIL **does not eliminate** concurrency issues or race conditions—it just means only one thread can execute Python code at a time. We’re not limited to one thread when doing I/O operations or working with C libraries (which don’t use the GIL).



The GIL mainly affects **CPU-bound** tasks—computationally heavy tasks that need parallelism. It doesn’t block **I/O-bound** tasks (like file or network operations).



---



### `multiprocessing`



That’s where the `multiprocessing` module comes in.



This module lets you create and manage separate **processes**, each with its own GIL—so they don’t block each other. It supports parallel execution of CPU-bound tasks using separate processes, making it possible to take full advantage of multi-core systems.



Creating processes is resource-intensive, so `multiprocessing` is best used when:

* you have heavy computations (e.g. image processing, video rendering, matrix calculations),

* or you need true process isolation (e.g. model loading, socket communication).



Key features and classes of `multiprocessing` include:



1. `Process`: Creates and manages individual processes.

2. `Pool`: Manages a pool of worker processes and distributes tasks among them.

3. `Queue`: Enables safe data exchange between processes using queues.

4. `Manager`: Creates shared objects (lists, dicts, queues, etc.) between processes.

5. `Lock`, `Event`, `Condition`, `Semaphore`: Synchronization primitives to prevent race conditions when accessing shared resources.

6. `Pipe`: Two-way communication channel between two processes.

7. `cpu_count()`: Returns the number of available CPU cores.



`multiprocessing` lets you fully utilize multiple cores by actually running tasks in **parallel**. But you still need to manage synchronization, shared data, and avoid race conditions.



---



Let me know what you think and feel free to share your experience!