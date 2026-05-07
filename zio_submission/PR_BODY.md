## 🐆 SHA-713 FiberMailbox Optimization

### Summary
Specialized MPSC Fiber Mailbox optimized for ZIO runloop.

### Core Design
- 4-slot fast-path array (cache-friendly)
- Atomic-free read index (single consumer assumption)
- MPSC overflow fallback queue

### Expected Benefit
- Reduced contention vs ConcurrentLinkedQueue
- Improved L1/L2 cache locality
- Faster fiber scheduling hot-path

### Notes
Designed for extremely small mailbox size (1–4 messages dominant case).
