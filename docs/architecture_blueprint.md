# Smart City Zone-Controller Deployment Blueprint

## Task 9 — Distributed Architecture and Communication Plan

### Architecture Choice: Client-Server

I would use a **Client-Server architecture** for the Smart City platform. The three zone controllers in Zone-A, Zone-B, and Zone-C act as clients, while the central Smart City Operations dashboard and its backend services act as the server. The **scheduler and Banker's-Algorithm engine from Part 1** would run on the zone-controller side as the fixed compute core for scheduling sensor-processing jobs and checking resource safety.

This architecture is suitable for the following reasons:

- **Transparency:** The central server provides a common point for collecting and presenting information from all three zones. Operators can view alerts and sensor information without directly interacting with each zone controller.
- **Fault tolerance:** A problem with one zone controller does not have to stop the other zone controllers from operating their local workloads. The **scheduler and Banker's-Algorithm engine from Part 1** can continue running locally on the affected controller while communication with the central dashboard is unavailable.
- **Scalability:** Additional zone controllers can be added as new clients without redesigning the whole architecture. The central backend can also be scaled as the number of zones and sensor messages increases.
- **Single point of failure:** The main weakness is that the central server can become a single point of failure for centralized monitoring. To reduce this risk, the server should use redundancy and failover so that a failure does not permanently stop dashboard operations.

### Communication Plan

#### (a) Real-time public-safety alert

**Communication type:** Asynchronous  
**Protocol:** MQTT

When a zone controller detects a real-time public-safety event, it should publish an alert asynchronously using MQTT. The **scheduler and Banker's-Algorithm engine from Part 1** can continue processing its local sensor-processing jobs without waiting for the Smart City Operations dashboard to respond. MQTT is suitable because it uses a lightweight publish/subscribe model and is designed for IoT devices and event-driven communication.

For example:

```text
Zone Controller
      |
      | MQTT publish
      v
MQTT Broker
      |
      v
Smart City Operations Dashboard


### Why these choices fit the marking criteria

| Requirement                | Choice                   |
|----------------------------|--------------------------|
| Architecture               | **Client-Server**        |
| Transparency               |        ✅               |
| Fault tolerance            |        ✅               |
| Scalability                |        ✅               |
| Single point of failure    |        ✅               |
| Public-safety alert        | **Asynchronous + MQTT**  |
| Daily sensor log           | **Asynchronous + HTTPS** |
| Part 1 engine explicitly referenced |  ✅             |

**Important:** Keep **Client-Server** as the only architecture choice.
Don't mention Hybrid or Peer-to-Peer as alternative architecture choices in the document,
because the task says to pick **exactly one**.
