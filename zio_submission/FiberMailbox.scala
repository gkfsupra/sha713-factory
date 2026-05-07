package sha713

import java.util.concurrent.atomic.AtomicInteger
import java.util.concurrent.ConcurrentLinkedQueue

final class FiberMailbox[A] {

  // 🔥 FAST PATH (4 slots cache-friendly)
  private[this] val size = 4
  private[this] val buffer = new Array[AnyRef](size)

  @volatile private[this] var writeIdx: Int = 0
  @volatile private[this] var readIdx: Int = 0

  // 🔥 overflow fallback
  private[this] val overflow = new ConcurrentLinkedQueue[A]()

  // =========================
  // OFFER (MULTI PRODUCER)
  // =========================
  def offer(a: A): Unit = {
    val w = writeIdx
    val next = (w + 1) % size

    if (next != readIdx) {
      buffer(w) = a.asInstanceOf[AnyRef]
      writeIdx = next
    } else {
      overflow.offer(a)
    }
  }

  // =========================
  // POLL (SINGLE CONSUMER)
  // =========================
  def poll(): A = {
    val r = readIdx

    if (r != writeIdx) {
      val v = buffer(r)
      readIdx = (r + 1) % size
      v.asInstanceOf[A]
    } else {
      overflow.poll()
    }
  }
}
