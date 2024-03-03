好的资料
https://generalthink.github.io/tags/%E5%A4%9A%E7%BA%BF%E7%A8%8B/

##### mutex 和monitor的区别

语义不同：

Mutex：Mutex 是一种简单的同步原语，它提供了两种操作：lock（获取锁）和 unlock（释放锁）。当一个线程获得了 Mutex 后，其他线程必须等待该线程释放锁后才能获得锁。Mutex 并不提供其他附加的语义，如条件变量等。
Monitor：Monitor 是一种高级同步机制，它是一种包含了锁、条件变量和一些操作的抽象。除了提供类似 Mutex 的 lock 和 unlock 操作外，Monitor 还提供了等待和通知（wait 和 notify）机制，允许线程在某些条件下等待和唤醒其他线程。
关联性：

Mutex：Mutex 可以与任何数据结构或代码段一起使用，因为它是一种通用的同步原语。
Monitor：Monitor 通常与特定的类或对象关联，它提供了对这些对象的同步访问和控制。在 Java 中，每个对象都有一个关联的监视器，可以使用 synchronized 关键字来获取对象的监视器锁。
灵活性：

Mutex：Mutex 是一种低级同步原语，相对较为灵活，可以根据需要在任何地方使用。
Monitor：Monitor 是一种高级抽象，提供了更方便的等待和通知机制，但其使用受到限制，通常与特定的类或对象关联。
总的来说，Mutex 是一种简单的同步原语，而 Monitor 则是一种更高级的抽象，提供了更多的同步语义和操作，但其使用通常受到限制，适用于特定的类或对象。
 ***Monitor必须和锁一起用 不然会抛出异常 Thread.currency.wait（）没有使用场景直接是报错的 Thread.currency不能作为Monitor 每个线程中其实例都不同 Motitor只释放和自己绑定的锁***

#####   ReentrantLock唤醒机制 
ReentrantLock 在被unlock 的时候会唤醒所有的等待的线程还是唤醒一个 唤醒的规则是怎么样的

ChatGPT
ReentrantLock 类的 unlock() 方法会释放锁，并唤醒等待该锁的线程。但是，它并不会像 synchronized 块那样自动唤醒所有等待的线程。具体唤醒的规则是：

公平性设置：如果 ReentrantLock 是公平锁（通过构造函数设置为公平锁），则等待时间最长的线程将会被唤醒，保证线程获取锁的顺序与其等待的顺序一致，实现公平性。

非公平性设置：如果 ReentrantLock 是非公平锁（默认情况下是非公平锁），则等待锁的所有线程中的任何一个都有机会被唤醒，这取决于操作系统的调度和 JVM 的实现。通常情况下，JVM 偏向于唤醒等待时间较长的线程，但并不保证按照等待顺序唤醒。

总的来说，唤醒哪个线程是不确定的，这取决于 JVM 的实现和当前系统的状态。公平性设置影响了唤醒的顺序，但并不是绝对的，而是一个倾向性的特性。

##### interrupt()方法 InterruptedException
在Java中，interrupt() 方法是用来中断线程的。当你调用一个线程的 interrupt() 方法时，会设置该线程的中断状态为"中断"。但是，这并不意味着线程会立即停止执行。实际上，线程会继续执行，直到它检查到自己的中断状态，并且选择处理中断或者直接退出。

interrupt() 方法的行为会根据线程的不同状态而有所不同：
* 程序如果处于NEW 状态 那么调用interrupt() 方法相当于identity()

* 如果线程处于运行状态（即正在执行任务），那么调用 interrupt() 方法会将线程的中断状态设置为"中断"。但线程不会立即停止执行，而是会继续运行下去,也不会报错。

* 如果线程处于阻塞状态（例如，调用了 Object.wait()、Thread.sleep()、Thread.join() 等等），那么调用 interrupt() 方法会中断线程的阻塞状态，并抛出 InterruptedException 异常。这时你可以在异常处理中选择继续执行（进入catch段后线程状态设为RUNNIG，线程也进入RUNNING，继续执行catch代码段后的代码）或者退出线程(),没有处理直接抛的话直接结束。

如果线程处于非阻塞、非等待状态，但是检测到自己的中断状态为"中断"，那么线程可以选择在适当的时候终止执行，通常通过检查 Thread.currentThread().isInterrupted() 方法来判断中断状态并进行相应的处理。

